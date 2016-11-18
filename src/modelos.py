#!/usr/bin/env python
# -*- coding: utf-8 -*
'''
Created on 06/02/2011

@author: sergio
'''

import os
import urllib2
import tweepy #Librería para twitter.
import bitlyapi #Librería para bitly.
import twitpic.twitpic2 #Librería para twitpic.
import clavesConstantes
import simplejson
import urllib

class Comunes(object):
    
    def conectarATwitter(self):
        '''
        Realiza la conexión a twitter del usuario y devuelve los objetos auth y api.
        '''
        self.PATH_APP = ''
        const = clavesConstantes.clavesConstantes()
        auth = tweepy.OAuthHandler(const.CONSUMER_KEY, const.CONSUMER_SECRET)
        auth.set_access_token(const.ACCESS_KEY, const.ACCESS_SECRET)
        api = tweepy.API(auth)
        
        return auth, api
    
    def verTrendingTopics(self):
        auth, api = self.conectarATwitter()
        #for TT in api.trends_available():
        #    print TT['name'], TT['woeid'] #Spain 23424950
        todoTT = api.trends_location(23424950)[0]['trends']
        res = []
        for tt in todoTT:
            res = res + [(tt['name'],tt['url'])]
        return res
    
    def verListaMeHanBorrado(self, usuario):
        res=[]
        print usuario
        usuario = ""
        print usuario
        auth, api = self.conectarATwitter()
        idsSeguidores=api.followers_ids(screen_name=usuario)#Seguidores
        #idsSeguidores = idsSeguidores[0]
        idsSigo=api.friends_ids(screen_name=usuario)#Gente a la que sigo
        #idsSigo = idsSigo[0]
        meHaBloqueado = []
        for ids in idsSigo:
            if idsSeguidores.count(ids)<1:
                meHaBloqueado = meHaBloqueado + [ids]
        #Saco excepciones de la lista de excepciones.
        fich1 = open(self.PATH_APP + "listaExcepcionEliminar", "Ur")
        listaExcepciones = map(lambda lineaa: lineaa.replace("\n",""), fich1.readlines())
        fich1.close()
        #Ahora quiero los nombres de los que me han bloqueado.
        for ids in meHaBloqueado:
            arrobaNick = api.get_user(user_id=ids).screen_name
            if listaExcepciones.count("@"+arrobaNick)<1:
                res = res + [arrobaNick]
        return res
    
    def enviarTweetATimeline(self, texto):
        '''
        Actualiza el timeline con un estado (vamos, el tuitear de toda la vida).
        '''
        auth, api = self.conectarATwitter()
        api.update_status(texto[0:140])
    
    def extraerTweetsDeUsuario(self, usuario, limite=600):
        resLista = []
        resCuenta = 0
        auth, api = self.conectarATwitter()
        iterador = 0
        #for status in tweepy.cursor.Cursor(api.home_timeline).items(limite): #user_timeline para ver mis tuits
        tuits = api.user_timeline(screen_name=usuario, count=limite)
        fin = len(tuits)
        while (iterador<limite and iterador<fin):
            status=tuits[iterador]
            #try:
            #    status = tuits.next()
            #except StopIteration:
            #    return resLista
            #Preparar mensaje.
            msg = Mensaje()
            msg.setMensaje(status)
            #AQUÍ FALTA POR AÑADIR EL RESTO.
            #Añadir a lista.
            resLista = resLista+[msg] #Lista de objetos mensaje.
            iterador = iterador + 1
            resCuenta = resCuenta + 1
        return resLista#, resCuenta

    
    def extraerTweetsDeFlujo(self, flujo, hastaID=-1, limite=-1):
        '''
        Extrae un número de tuits de un flujo (p.e.:api.home_timeline), pasado por parámetro.
        Si limite es igual a -1 extraerá un número ilimitado de tuits hasta llegar a la 
        hastaID.
        '''
        resLista = []
        resCuenta = 0
        #auth, api = self.conectarATwitter()
        mostrar = True
        iterador = 0
        #for status in tweepy.cursor.Cursor(api.home_timeline).items(limite): #user_timeline para ver mis tuits
        tuits = tweepy.cursor.Cursor(flujo).items(limite)
        while (mostrar and iterador<limite):
            try:
                status = tuits.next()
            except StopIteration:
                return resLista
            if mostrar:
                #Preparar mensaje.
                msg = Mensaje()
                msg.setMensaje(status)
                #AQUÍ FALTA POR AÑADIR EL RESTO.
                #Añadir a lista.
                resLista = resLista+[msg] #Lista de objetos mensaje.
                iterador = iterador + 1
                resCuenta = resCuenta + 1
            
            if hastaID == status.id:
                #Si es la id => mostrar = False (dejar de mostrar estados, incluído éste)
                mostrar = False
        return resLista#, resCuenta
    
    def listaTuplasRutaImagenNickEstadoID(self, flujoLista, esDM):
        '''
        Devuelve una lista de tuplas que contienen (rutaImagenPerfil, @Nick, Estado, ID)
        '''
        #La idea es mirar la lista de contactos y descargar una especie de
        #caché con las imágenes de los mismos, la ruta de la imagen que se 
        #guardará en la lista será la que esté en el ordenador y no en internet 
        #(hay que recordar que todo el proceso de petición es muy lento).
        res = []
        for elem in flujoLista:
            status = elem.getMensaje()
            fotoPerfil = self.__guardarImagen(status.sender.profile_image_url if (esDM) else status.user.profile_image_url) #0
            #print fotoPerfil
            usuario = ("@"+status.sender.screen_name + "("+status.sender.name+")") if (esDM) else ("@"+status.user.screen_name + "("+status.user.name+")") #1
            estado = status.text #2
            id = status.id #3
            fecha = "Fecha: " + str(status.created_at) #4
            res = res+ [(fotoPerfil,usuario,estado,id, fecha)]
        return res
        
    def contestarTweetConTweet(self, texto, id_estado_reply):
        '''
        Hacemos un reply nativo.
        '''
        auth, api = self.conectarATwitter()
        api.update_status(texto[0:140], in_reply_to_status_id=id_estado_reply)
    
    def enviarMensajePrivado(self, usuario, texto):
        '''
        Enviar un DM a un usuario.
        '''
        auth, api = self.conectarATwitter()
        msg = api.send_direct_message(screen_name = usuario, text = texto[0:140])
    
    def hacerRetweet(self, id):
        '''
        Hace un RT nativo.
        '''
        auth, api = self.conectarATwitter()
        api.retweet(id)
        
    def hacerFavorito(self, id):
        auth, api = self.conectarATwitter()
        api.create_favorite(id)
        
    def quitarDeFavoritos(self, id):
        auth, api = self.conectarATwitter()
        api.destroy_favorite(id)
        
    def acortarUrl(self, url):
        const = clavesConstantes.clavesConstantes()
        resultado = ""
        try:
            #Me conecto con mi usuario y clave a bit.ly
            b = bitlyapi.BitLy(const.BIT_LY_USERNAME, const.BIT_LY_API_KEY)
            #Acorto la url de google
            res = b.shorten(longUrl=url)
            #Devuelvo la url acortada.
            resultado = res['url']
        except:
            resultado = url
        return resultado
    
    def enviarImagenATimeline(self, rutaImagen, texto):
        '''
        Actualiza el timeline con una imagen subida a Twitpic (sube a twitpic y escribe
        estado en timeline ¡cuídado con más de 140 carácteres!).
        '''
        const = clavesConstantes.clavesConstantes()
        auth, api = self.conectarATwitter()
        #Creo objeto.
        tp = twitpic.twitpic2.TwitPicOAuthClient()
        #Asigno valores
        tp.set_service_key(const.TWITPIC_SERVICE_KEY) #service_key
        tp.set_access_token(str(auth.access_token)) #access_token
        tp.set_comsumer(const.CONSUMER_KEY, const.CONSUMER_SECRET) #consumer_key y consumer_secret
        #Preparo imagen y pie de imagen (mensaje).
        parametros = {'media': rutaImagen,
                      'message': texto}
        #Subo a TwitPic la imagen y pie de imagen (mensaje).
        response = tp.create('upload', parametros) #METHOD_CALL='upload', PARAMS=parametros
        #Parámetros importantes devueltos de la llamada: response['url'], response['text']
        #TUITEAR IMAGEN Y ESTADO
        api.update_status((response['url']+" - "+response['text'])[0:140])
    
    def __guardarImagen(self, url):
        '''
        Guarda la imagen en directorio temporal y luego devuelve la ruta.
        '''
        res = self.PATH_APP + "temp/"+url.replace(":","_").replace("/","_")
        if not os.path.exists(res):
            f = urllib2.urlopen(url)
            fich = open(res, 'w')
            fich.write(f.read())
            fich.close()
            f.close()
        return res
    
    def descargaImagen(self, url):
        '''
        Dada una url terminada en .jpg, .png, .gif o .bmp, descarga la imagen a la carpeta
        cache y devuelve la ruta.
        '''
        formato = url[-4:]
        res = ""
        #if formato==".jpg" or formato==".png" or formato==".gif" or formato==".bmp":
        res = self.PATH_APP + "cache/"+(url.split("/")[-1])
        if os.path.exists(res):
            #Si ya existía en la caché un fichero con el mismo nombre, borrarlo.
            os.remove(res)
        f = urllib2.urlopen(url)
        fich = open(res, 'w')
        fich.write(f.read())
        fich.close()
        f.close()
        return res
    
class Mensaje(object):
    '''
    Trata los mensajes (tuits, DM, replies,...) de twitter.
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.mensaje = None #Objeto devuelto por twitter.
        self.leido = False #Dice si el objeto ha sido leído o no.
        self.hayRetuit = False #Si ha sido retuiteado contiene True, si no False (si es DM siempre será False).
        self.contestado = False #Dice si el mensaje ha sido contestado o no. 
    
    def setMensaje(self, mensaje):
        self.mensaje = mensaje
    
    def getMensaje(self):
        return self.mensaje
    
    def setLeido(self, leido):
        self.leido = leido
        
    def isLeido(self):
        return self.leido
    
    def setHayRetuit(self, hayRetuit):
        self.hayRetuit = hayRetuit
    
    def isHayRetuit(self):
        return self.hayRetuit
    
    def setContestado(self, contestado):
        self.contestado = contestado
        
    def isContestado(self):
        return self.contestado


class TraductorGoogleTranslate(object):
    '''
    Una API sencilla del traductor de google para Python.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.baseUrl = "http://ajax.googleapis.com/ajax/services/language/translate"
    
    def getSplits(self, text, splitLength=4500):
        '''
        Translate Api has a limit on length of text(4500 characters) that can be translated at once, 
        '''
        return (text[index:index+splitLength] for index in xrange(0,len(text),splitLength))
     
     
    def translate(self, text, src='', to='en'):
        '''
        A Python Wrapper for Google AJAX Language API:
        * Uses Google Language Detection, in cases source language is not provided with the source text
        * Splits up text if it's longer then 4500 characters, as a limit put up by the API
        '''
     
        params = ({'langpair': '%s|%s' % (src, to),
                 'v': '1.0'
                 })
        retText=''
        for text in self.getSplits(text):
                params['q'] = text
                resp = simplejson.load(urllib.urlopen('%s' % (self.baseUrl), data = urllib.urlencode(params)))
                try:
                        retText += resp['responseData']['translatedText']
                except:
                        raise
        return retText


class Timeline(Comunes):
    '''
    Trata la lista de cronología (home) que se va actualizando.
    '''
    
    def __init__(self, limite = -1):
        '''
        Constructor.
        '''
        #Variables del objeto: self.listaDeMensajes, self.numeroTweetNoLeidos y 
        #                      self.indiceUltimoTweetLeido
        self.PATH_APP = '/home/sergio/Escritorio/Todo/programas/prTwittpyth/src/'
        self.__inicializarListaDeMensajes(600 if (limite==-1) else limite)
        
    def tuitsQueMePerdi(self):
        fich2 = open (self.PATH_APP + "ultimoTuit", 'r')
        idDelUltimo = long(fich2.read())
        fich2.close()
        return self.__extraer(idDelUltimo, 600)[0]
        
        
    def __estaEnPCImagenPerfil(self):
        '''
        Comprueba si está la imagen del perfil en el pc (al guarderse la imagen
        se sustituyen los : y las / por el símbolo *)
        '''
        return True
        
    def __guardarImagen(self, url):
        '''
        Guarda la imagen en directorio temporal y luego devuelve la ruta.
        '''
        res = self.PATH_APP + "temp/"+url.replace(":","_").replace("/","_")
        if not os.path.exists(res):
            f = urllib2.urlopen(url)
            fich = open(res, 'w')
            fich.write(f.read())
            fich.close()
            f.close()
        return res
        
    def listaTuplasRutaImagenNickEstadoID(self):
        '''
        Devuelve una lista de tuplas que contienen (rutaImagenPerfil, @Nick, Estado, ID)
        '''
        #La idea es mirar la lista de contactos y descargar una especie de
        #caché con las imágenes de los mismos, la ruta de la imagen que se 
        #guardará en la lista será la que esté en el ordenador y no en internet 
        #(hay que recordar que todo el proceso de petición es muy lento).
        res = []
        for elem in self.listaDeMensajes:
            status = elem.getMensaje()
            fotoPerfil = self.__guardarImagen(status.user.profile_image_url) #0
            #print fotoPerfil
            usuario = "@"+status.user.screen_name + "("+status.user.name+")" #1
            estado = status.text #2
            id = status.id #3
            res = res+ [(fotoPerfil,usuario,estado,id)]
        return res
    
    def __extraerReforzado(self, hastaID1=-1, hastaID2=-1, hastaID3=-1, limite=-1):
        resLista = []
        resCuenta = 0
        auth, api = self.conectarATwitter()
        mostrar = True
        iterador = 0
        
        #for status in tweepy.cursor.Cursor(api.home_timeline).items(limite): #user_timeline para ver mis tuits
        tuits = tweepy.cursor.Cursor(api.home_timeline).items(limite)
        while (mostrar and iterador<limite):
            status = tuits.next()
            if mostrar:
                #Preparar mensaje.
                msg = Mensaje()
                msg.setMensaje(status)
                #AQUÍ FALTA POR AÑADIR EL RESTO.
                #Añadir a lista.
                resLista = resLista+[msg] #Lista de objetos mensaje.
                iterador = iterador + 1
                resCuenta = resCuenta + 1
            #Usamos una medida de seguridad por si se ha borrado la última id.
            #Es raro que se borre hasta 3 tuits seguidos, así que la condición
            #que buscamos es que la id sea una de las tres ids para dejar de
            #mostrar.
            if mostrar and (hastaID1 == status.id or hastaID2 == status.id or hastaID3 == status.id):
                #Si es la id => mostrar = False (dejar de mostrar estados, incluído éste)
                mostrar = False
        return resLista, resCuenta
    
    def actualizar(self, limite=-1):
        '''
        Actualiza la lista, añadiendo todos los tweets que faltan a la lista.
        Actualiza por tanto self.listaDeMensajes y self.numeroTweetNoLeidos.
        Usa self.__anyadirNuevoMensaje(self, mensaje) y self.__conectarATwitter(self)
        '''
        resLista, resCuenta = self.__extraerReforzado(self.listaDeMensajes[0].getMensaje().id, self.listaDeMensajes[1].getMensaje().id, self.listaDeMensajes[2].getMensaje().id, limite)
        self.listaDeMensajes = resLista[:-1] + self.listaDeMensajes
        self.numeroTweetNoLeidos = (resCuenta - 1) + self.numeroTweetNoLeidos 
        #Devolver lo nuevo al estilo listaTuplasRutaImagenNickEstadoID
        res = []
        for elem in resLista[:-1]:
            status = elem.getMensaje()
            fotoPerfil = self.__guardarImagen(status.user.profile_image_url) #0
            #print fotoPerfil
            usuario = "@"+status.user.screen_name + "("+status.user.name+")" #1
            estado = status.text #2
            id = status.id #3
            res = res+ [(fotoPerfil,usuario,estado,id)]
        return res
        
        
    def extraerMensaje(self, id):
        '''
        Dada la id de un tweet, devuelve toda la información correspondiente en un objeto
        Mensaje.
        '''
        cont = 0
        res = None
        fin = len(self.listaDeMensajes)
        while (cont<fin and id!=self.listaDeMensajes[cont].getMensaje().id):
            cont = cont + 1
        if cont<fin:
            res = self.listaDeMensajes[cont]
        return res
    
    def marcarComoLeido(self, indice):
        '''
        Marca un mensaje como leído (indice es el indice correspondiente a la lista no la id).
        '''
        self.listaDeMensajes[indice].setLeido(True)
        self.numeroTweetNoLeidos = self.numeroTweetNoLeidos -1
        if indice < self.indiceUltimoTweetLeido:
            self.indiceUltimoTweetLeido = indice
    
    def __del__(self):
        '''
        Destructor
        '''
        #Guardar id del último Tweet leído.
        fich = open ("primerTuit", 'w')
        fich.write(str(self.listaDeMensajes[self.indiceUltimoTweetLeido].getMensaje().id))
        fich.close()
        fich2 = open ("ultimoTuit", 'w')
        fich2.write(str(self.listaDeMensajes[0].getMensaje().id))
        fich2.close()
        
    def __str__(self):
        res = ""
        for elem in self.listaDeMensajes:
            status = elem.getMensaje()
            res = res + "@"+status.user.screen_name + "("+status.user.name+")\n"
            res = res + "Fecha: " + str(status.created_at) + ", ID DEL TUIT: "+str(status.id)
            res = res + "\nEstado: "+status.text
            res = res + "\n------------------------------------------------------------------\n"
        return res
    
    def __inicializarListaDeMensajes(self, limite=-1):
        '''
        Inicializa la lista de mensajes.
        '''
        if os.path.exists(self.PATH_APP + "primerTuit"):
            #Protocolo para una vez que no sea la primera que se usa:
            #1. Estará creado fichero y contiene una id de un tuit.
            fich = open (self.PATH_APP + "primerTuit", 'Ur')
            miId = long(fich.readline())
            fich.close()
            #2. Añadir tuits a la lista hasta encontrar dicho tuit.
            self.listaDeMensajes, self.numeroTweetNoLeidos = self.__extraer(miId, limite)
            self.indiceUltimoTweetLeido = len(self.listaDeMensajes) - 1
        else:
            #1. Extraer primeros 'limite' tuits.
            self.listaDeMensajes, self.numeroTweetNoLeidos = self.__extraer(limite=limite)
            #2. Si no existe crear fichero que contendrá la id del primer tuit.
            fich = open (self.PATH_APP + "primerTuit", 'w')
            fich.write(str(self.listaDeMensajes[0].getMensaje().id))
            fich.close()
            self.indiceUltimoTweetLeido = limite - 1
    
    def __extraer(self, hastaID=-1, limite=-1):
        '''
        Extrae un número de tuits de home.
        Si limite es igual a -1 extraerá un número ilimitado de tuits hasta llegar a la 
        hastaID.
        '''
        resLista = []
        resCuenta = 0
        auth, api = self.conectarATwitter()
        mostrar = True
        iterador = 0
        
        #for status in tweepy.cursor.Cursor(api.home_timeline).items(limite): #user_timeline para ver mis tuits
        tuits = tweepy.cursor.Cursor(api.home_timeline).items(limite)
        while (mostrar and iterador<limite):
            status = tuits.next()
            if mostrar:
                #Preparar mensaje.
                msg = Mensaje()
                msg.setMensaje(status)
                #AQUÍ FALTA POR AÑADIR EL RESTO.
                #Añadir a lista.
                resLista = resLista+[msg] #Lista de objetos mensaje.
                iterador = iterador + 1
                resCuenta = resCuenta + 1
            
            if hastaID == status.id:
                #Si es la id => mostrar = False (dejar de mostrar estados, incluído éste)
                mostrar = False
        return resLista, resCuenta
