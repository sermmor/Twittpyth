#!/usr/bin/env python
# -*- coding: utf-8 -*

import wx
import wx.lib.agw.hyperlink
import vista
import UltimateVisualizador
import subirImagenATwitpic
import sys
import modelos
import pyaspell.pyaspell
import urllib2

class ControladorPrincipal(vista.VentanaPrincipal):
    '''
    classdocs
    '''
    
    def __init__(self, *args, **kwds):
        '''
        Constructor
        '''
        vista.VentanaPrincipal.__init__(self, *args, **kwds)
        
        #Variables
        self.contestarTweetActivado = False
        self.contestarTweetIDTuit = ""
        self.sugerenciasOrtografia = {}
        self.primeraVezClickDerecho = True
        self.idsPorLink = {}
        self.miVisualizador = None
        self.visualizadorEstaCerrado = True
        self.terminado = False
        self.timer = wx.Timer(self, -1) #Creo mi timer.
        #Pre-uso de variables.
        self.timer.Start(self.MILISEGUNDOS_PARA_ACTUALIZAR) #Provocar evento cada 30000ms = 30segundos.
        #Evento del timer.
        self.Bind(wx.EVT_TIMER, self.reflescarTL)
        #Eventos menú.
        wx.EVT_MENU(self, self.toolbarImagen, self.subirImagenUsandoTwitPic)
        wx.EVT_MENU(self, self.toolbarRecargar, self.reflescarTL)
        wx.EVT_MENU(self, self.toolbarPerdidos, self.verPerdidos)
        #wx.EVT_MENU(self, self.toolbarRT, self.retweetNativoEstado)
        #wx.EVT_MENU(self, self.toolbarReplies, self.contestarTweet)
        #wx.EVT_MENU(self, self.toolbarFavorito, self.favoritearTweet)
        wx.EVT_MENU(self, self.toolbarOrtografia, self.corregirOrtografiaEnTuit)
        wx.EVT_MENU(self, self.toolbarTumblr, self.irATumblr)
        wx.EVT_MENU(self, self.toolbarTrendingTopics, self.verTrendingTopics)
        #Eventos botones.
        self.btTweet.Bind(wx.EVT_BUTTON, self.enviarTweet)
        self.btDM.Bind(wx.EVT_BUTTON, self.enviarDM)
        #Otros eventos.
        self.treeCtrlIrAZona.Bind(wx.EVT_TREE_SEL_CHANGED, self.seleccionaElementoArbol)
        self.listCtrlListaTweets.Bind(wx.EVT_LIST_ITEM_SELECTED, self.casillaSeleccionada)
        wx.EVT_LIST_ITEM_RIGHT_CLICK(self, self.listCtrlListaTweets.GetId(), self.clicDerechoEstado)
        self.tCtrlEscribir.Bind(wx.EVT_KEY_DOWN, self.decrementaOIncrementaContador)
        wx.EVT_TEXT_PASTE(self.tCtrlEscribir, self.pegaTexto)
        wx.EVT_CLOSE(self, self.salir)
        #wx.EVT_RIGHT_DOWN(self.tCtrlEscribir, self.clicDerechoTexto)
        #self.tCtrlEscribir.Bind(wx.ID_COPY, self.copiaTexto)
        #self.tCtrlEscribir.Bind(wx.ID_PASTE, self.pegaTexto)
        #self.listCtrlListaTweets.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.casillaDeseleccionada)
    
    def irATumblr(self, evento=None):
        abreLinks = wx.lib.agw.hyperlink.HyperLinkCtrl(self, wx.NewId())
        abreLinks.GotoURL("http://www.tumblr.com/", True, True)
    
    def abrirVisualizador(self):
        self.miVisualizador = UltimateVisualizador.Visualizador(None, -1, "")
        self.miVisualizador.setPtrPrincipal(self)
        self.miVisualizador.Show()
        self.visualizadorEstaCerrado = False
        #PROBAR IMAGENES
        ##url = "/home/sergio/workspacePython/prTwittpyth/src/misTabs/Calvin.JPG"
        #url = "http://4.bp.blogspot.com/_1QfuM0R-rVE/TMC8LPfRdKI/AAAAAAAAaR8/PU7sen-AFt0/s1600/sueno.jpg"
        #co = modelos.Comunes()
        #self.miVisualizador.abrirPestanyaDeImagen(url.split("/")[-1], co.descargaImagen(url))
    
    def verTrendingTopics(self, evento=None):
        co = modelos.Comunes()
        listaPares=co.verTrendingTopics()
        texto = ""
        for par in listaPares:
            texto = texto + par[0] + " : " + par[1] + "\n"
        if self.visualizadorEstaCerrado:
            self.abrirVisualizador()
        self.miVisualizador.abrirPestanyaDeTexto("Temas del momento", texto)
    
    def verImagenEnVisualizador(self, ruta):
        #La ruta puede ser la ruta real, la ruta a twitpic o a yfrog.
        formato = ruta[-4:]
        if (ruta[0:16]=="http://yfrog.com"): #Imagen desde yfrog.
            #Si la ruta es de yfrog.
            f = urllib2.urlopen(ruta)
            todaLaPagina = f.read()
            f.close()
            cortaInicio = '''<link rel="image_src" href="'''
            todaLaPagina = todaLaPagina[(todaLaPagina.find(cortaInicio)+len(cortaInicio)):]
            todaLaPagina = todaLaPagina[:(todaLaPagina.find('''" />'''))]
            #En la variable todaLaPagina ya tenemos la ruta para descargar imagen!!
            co = modelos.Comunes()
            #Usar el UltimateVisualizador
            if self.visualizadorEstaCerrado:
                self.abrirVisualizador()
            self.miVisualizador.abrirPestanyaDeImagen(todaLaPagina.split("/")[-1], co.descargaImagen(todaLaPagina))
        elif ruta[0:14]=="http://twitpic":
            #Si la ruta es de twitpic.
            #Mostramos en una pestaña la imagen y en otra el texto.
            f = urllib2.urlopen(ruta)
            todaLaPagina = f.read()
            f.close()
            cortaInicio = '''<img class="photo" id="photo-display" src="'''
            cortaMedio='''" alt="'''
            cortaFin='''" />'''
            todaLaPagina = todaLaPagina[(todaLaPagina.find(cortaInicio)+len(cortaInicio)):]
            link = todaLaPagina[:(todaLaPagina.find(cortaMedio))]
            texto = todaLaPagina[(todaLaPagina.find(cortaMedio)+len(cortaMedio)):(todaLaPagina.find(cortaFin))]
            tituloTextoImagen = link.split("/")[-1][:7]
            co = modelos.Comunes()
            if self.visualizadorEstaCerrado:
                self.abrirVisualizador()
            self.miVisualizador.abrirPestanyaDeImagenYTexto(tituloTextoImagen, ruta, texto, co.descargaImagen(link))
            #self.miVisualizador.abrirPestanyaDeImagen(tituloTextoImagen, co.descargaImagen(link))
            #self.miVisualizador.abrirPestanyaDeTexto(tituloTextoImagen, texto)
        elif ruta[0:13]=="http://picplz":
            f = urllib2.urlopen(ruta)
            todaLaPagina = f.read()
            f.close()
            
            todaLaPagina = todaLaPagina[(todaLaPagina.find('''<div class="user-name small-follow">''')):]
            
            cortaInicio = '''<img src="'''
            todaLaPagina = todaLaPagina[(todaLaPagina.find(cortaInicio)+len(cortaInicio)):]
            todaLaPagina = todaLaPagina[:(todaLaPagina.find("\""))]
            #En la variable todaLaPagina ya tenemos la ruta para descargar imagen!!
            co = modelos.Comunes()
            #Usar el UltimateVisualizador
            if self.visualizadorEstaCerrado:
                self.abrirVisualizador()
            self.miVisualizador.abrirPestanyaDeImagen(todaLaPagina.split("/")[-1][:7], co.descargaImagen(todaLaPagina))
            
        elif formato==".jpg" or formato==".png" or formato==".gif" or formato==".bmp":
            #Si la ruta es normal y moliente.
            co = modelos.Comunes()
            if self.visualizadorEstaCerrado:
                self.abrirVisualizador()
            self.miVisualizador.abrirPestanyaDeImagen(ruta.split("/")[-1], co.descargaImagen(ruta))
    
    def verFlujoDeUsuarioEnVisualizador(self, usuario, co):
        def formatearLista(listaDeMensajes):
            res = ""
            for elem in listaDeMensajes:
                status = elem.getMensaje()
                res = res + "@"+status.user.screen_name + "("+status.user.name+")\n"
                res = res + "Fecha: " + str(status.created_at) + ", ID DEL TUIT: "+str(status.id)
                res = res + "\nEstado: "+status.text
                res = res + "\n------------------------------------------------------------------\n"
            return res
        #Usar el UltimateVisualizador
        if self.visualizadorEstaCerrado:
            self.abrirVisualizador()
        ############self.miVisualizador.abrirPestanyaDeTexto("Home", str(self.miTimeline))
        #self.miVisualizador.abrirPestanyaDeTexto("TL de "+usuario, formatearLista(co.extraerTweetsDeUsuario(usuario, limite=self.LIMITE_FLUJOS)))
        self.miVisualizador.abrirPestanyaDeTL("TL de "+usuario, co.extraerTweetsDeUsuario(usuario, limite=self.LIMITE_FLUJOS), self)
    
    def verFlujoEnVisualizador(self, nombreFlujo, flujo, co):
        def formatearLista(listaDeMensajes):
            res = ""
            for elem in listaDeMensajes:
                status = elem.getMensaje()
                if nombreFlujo=="DM":
                    res = res + "@"+status.sender.screen_name + "("+status.sender.name+")\n"
                else:
                    res = res + "@"+status.user.screen_name + "("+status.user.name+")\n"
                res = res + "Fecha: " + str(status.created_at) + ", ID DEL TUIT: "+str(status.id)
                res = res + "\nEstado: "+status.text
                res = res + "\n------------------------------------------------------------------\n"
            return res
        #Usar el UltimateVisualizador
        if self.visualizadorEstaCerrado:
            self.abrirVisualizador()
        #self.miVisualizador.abrirPestanyaDeTexto("Home", str(self.miTimeline))
        #self.miVisualizador.abrirPestanyaDeTexto(nombreFlujo, formatearLista(co.extraerTweetsDeFlujo(flujo, limite=self.LIMITE_FLUJOS)))
        self.miVisualizador.abrirPestanyaDeTL(nombreFlujo, co.extraerTweetsDeFlujo(flujo, limite=self.LIMITE_FLUJOS), self)
    
    def verTextoEnVisualizador(self, tituloTexto, texto):
        if self.visualizadorEstaCerrado:
            self.abrirVisualizador()
        self.miVisualizador.abrirPestanyaDeTexto(tituloTexto, texto)
    
    def seleccionaElementoArbol(self, evento=None):
        if not self.terminado:
            instruccion=self.treeCtrlIrAZona.GetItemText(evento.GetItem())
            if instruccion=="Home":
                co = modelos.Comunes()
                auth, api = co.conectarATwitter()
                self.verFlujoEnVisualizador(instruccion, api.home_timeline, co)
            elif instruccion=="@":
                co = modelos.Comunes()
                auth, api = co.conectarATwitter()
                self.verFlujoEnVisualizador(instruccion, api.mentions, co)
            elif instruccion=="Perfil":
                co = modelos.Comunes()
                self.verFlujoDeUsuarioEnVisualizador("@user", co)
            elif instruccion=="DM":
                co = modelos.Comunes()
                auth, api = co.conectarATwitter()
                self.verFlujoEnVisualizador(instruccion, api.direct_messages, co)
            elif instruccion=="Favoritos":
                co = modelos.Comunes()
                auth, api = co.conectarATwitter()
                self.verFlujoEnVisualizador(instruccion, api.favorites, co)
            elif instruccion=="De otros":
                co = modelos.Comunes()
                auth, api = co.conectarATwitter()
                self.verFlujoEnVisualizador(instruccion, api.retweeted_to_me, co)
            elif instruccion=="Mios":
                co = modelos.Comunes()
                auth, api = co.conectarATwitter()
                self.verFlujoEnVisualizador(instruccion, api.retweeted_by_me, co)
            elif instruccion=="Mis tweets":
                co = modelos.Comunes()
                auth, api = co.conectarATwitter()
                self.verFlujoEnVisualizador(instruccion, api.retweets_of_me, co)
            elif instruccion=="A eliminar":
                co = modelos.Comunes()
                lista=co.verListaMeHanBorrado("@user-name")
                texto = ""
                for elem in lista:
                    texto = texto + "@" + elem + " : " + "http://twitter.com/" + elem +"\n"
                self.verTextoEnVisualizador(instruccion, texto)
            elif instruccion=="Opciones":
                if self.visualizadorEstaCerrado:
                    self.abrirVisualizador()
                self.miVisualizador.abrirPestanyaDeOpciones()
            elif instruccion[0]=="@":
                co = modelos.Comunes()
                self.verFlujoDeUsuarioEnVisualizador(instruccion, co)
            evento.Skip()
    
    def verPerdidos(self, evento=None):
        def formatearLista(listaDeMensajes):
            res = ""
            for elem in listaDeMensajes:
                status = elem.getMensaje()
                res = res + "@"+status.user.screen_name + "("+status.user.name+")\n"
                res = res + "Fecha: " + str(status.created_at) + ", ID DEL TUIT: "+str(status.id)
                res = res + "\nEstado: "+status.text
                res = res + "\n------------------------------------------------------------------\n"
            return res
        #Usar el UltimateVisualizador
        if self.visualizadorEstaCerrado:
            self.abrirVisualizador()
        self.miVisualizador.abrirPestanyaDeTL("Tuits Atrasados", self.filtraTweets(self.miTimeline.tuitsQueMePerdi(), self.listaLosQueNoLeo, False), self)
        #self.miVisualizador.abrirPestanyaDeTexto("Tuits Atrasados", formatearLista(self.miTimeline.tuitsQueMePerdi()))
    
    def clicDerechoEstado(self, evento=None):
        if self.primeraVezClickDerecho:
            self.primeraVezClickDerecho = False
        else:
            indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
            estado=self.cronologia[indiceSeleccionado/2][2]
            self.primeraVezClickDerecho = True
            #print indiceSeleccionado 
            #print estado
            #Crearse lista de links con el estado.
            todosLosLinks = filter(lambda pal: pal[0:4]=="http",estado.split())
            #Ahora viene la paranoia del menú.
            menu = wx.Menu()
            
            #Añadir menú para copiar tuit.
            nuevaID = wx.NewId()
            menu.Append(nuevaID, "Copiar tuit")
            wx.EVT_MENU( menu, nuevaID, self.copiarTuit )
            
            #Añadir menú para @ (Reply).
            nuevaID = wx.NewId()
            menu.Append(nuevaID, "@ (Reply)")
            wx.EVT_MENU( menu, nuevaID, self.contestarTweet )
            
            #Añadir menú para Favorito.
            nuevaID = wx.NewId()
            menu.Append(nuevaID, "Favorito")
            wx.EVT_MENU( menu, nuevaID, self.favoritearTweet )
            
            #Añadir menú para Traducir tuit.
            nuevaID = wx.NewId()
            menu.Append(nuevaID, "Traducir tuit")
            wx.EVT_MENU( menu, nuevaID, self.TraduceTweet )
            
            #Añadir menú para RT nativo.
            nuevaID = wx.NewId()
            menu.Append(nuevaID, "RT nativo")
            wx.EVT_MENU( menu, nuevaID, self.retweetNativoEstado )
            
            #Añadir menú para hacer RT con comentario.
            nuevaID = wx.NewId()
            menu.Append(nuevaID, "RT con comentario")
            wx.EVT_MENU( menu, nuevaID, self.RTConComentario )
            
            #Por cada link hay un elemento del menú.
            self.idsPorLink = {}
            for link in todosLosLinks:
                nuevaID = wx.NewId()
                self.idsPorLink.update({nuevaID:link})
                menu.Append(nuevaID, link)
                wx.EVT_MENU( menu, nuevaID, self.MenuSelectionCb )
            
            #Por cada link que comience por "http://yfrog" o "http://twitpic" o acabe 
            #en .jpg, .png, .gif o .bmp => un elemento que apunte al visualizador.
            self.idsPorLinkVisualiza = {}
            for link in todosLosLinks:#+["http://twitpic.com/2j0919"]):
                esYfrog=(link[0:12]=="http://yfrog")
                esTwitpic=(link[0:14]=="http://twitpic")
                esPicplz=(link[0:13]=="http://picplz")
                formato = link[-4:]
                esImagen=(formato==".jpg" or formato==".png" or formato==".gif" or formato==".bmp")
                if esYfrog or esTwitpic or esImagen or esPicplz:
                    nuevaID = wx.NewId()
                    self.idsPorLinkVisualiza.update({nuevaID:link})
                    menu.Append(nuevaID, "visualiza: "+link)
                    wx.EVT_MENU( menu, nuevaID, self.MenuSeleccionVisualCb )
            #Todo arroba del twitt
            self.idsPorPerfilVisualiza = {}
            arrobas = filter(lambda elem: elem[0]=="@", (self.cronologia[indiceSeleccionado/2][1].split("("))+(estado.split()))
            for contacto in arrobas:
                nuevaID = wx.NewId()
                con = contacto[:-1] if(contacto[-1]==":") else contacto 
                self.idsPorPerfilVisualiza.update({nuevaID:con})
                menu.Append(nuevaID, con)
                wx.EVT_MENU( menu, nuevaID, self.MenuSeleccionVisualPerfilCb)
            
            #Ir a perfil en navegador.
            self.urlDePerfilSeleccionado = "http://twitter.com/"+arrobas[0][1:]
            nuevaID = wx.NewId()
            menu.Append(nuevaID, "Ver perfil en navegador")
            wx.EVT_MENU( menu, nuevaID, self.irAUrlPerfil )
            
            #Mostrar menú.
            self.listCtrlListaTweets.PopupMenu( menu, evento.GetPoint() )
            menu.Destroy()
    
    def irAUrlPerfil(self, evento=None):
        #Abrir link a perfil.
        abreLinks = wx.lib.agw.hyperlink.HyperLinkCtrl(self, wx.NewId())
        abreLinks.GotoURL(self.urlDePerfilSeleccionado, True, True)
    
    def MenuSelectionCb(self, evento=None):
        #Abrir link
        abreLinks = wx.lib.agw.hyperlink.HyperLinkCtrl(self, wx.NewId())
        abreLinks.GotoURL(self.idsPorLink[evento.GetId()], True, True)
    
    def MenuSeleccionVisualCb(self, evento=None):
        self.verImagenEnVisualizador(self.idsPorLinkVisualiza[evento.GetId()])
        
    def MenuSeleccionVisualPerfilCb(self, evento=None):
        co = modelos.Comunes()
        self.verFlujoDeUsuarioEnVisualizador(self.idsPorPerfilVisualiza[evento.GetId()], co)
    
    def TraduceTweet(self, evento=None):
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        texto = self.cronologia[indiceSeleccionado/2][2]
        
        tgt = modelos.TraductorGoogleTranslate()
        textoTraducido=tgt.translate(texto, to="es") #Uso autodeteción de idioma.
        
        if self.visualizadorEstaCerrado:
            self.abrirVisualizador()
        self.miVisualizador.abrirPestanyaDeTexto("Tuit traducido", "Texto original: \n"+texto+"\n\nTraducción automática: \n"+textoTraducido)
    
    def copiarTuit(self, evento=None):
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        #Guardar estado en portapapeles.
        datos = wx.TextDataObject()
        datos.SetText(self.cronologia[indiceSeleccionado/2][2])
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(datos)
            wx.TheClipboard.Close()
    
    def RTConComentario(self, evento=None):
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        usuario = self.cronologia[indiceSeleccionado/2][1].split("(")[0]
        estado = self.cronologia[indiceSeleccionado/2][2]
        self.tCtrlEscribir.SetValue("RT "+usuario+" "+estado)
    
    def enviarDM(self, evento=None):
        '''
        Envía un DM a un usuario.
        '''
        if self.tCtrlEscribir.GetValue()!="":
            #Quitar el @nosequien del mensaje y contar si hay menos o igual a 140 carácteres
            usuario, texto = self.tCtrlEscribir.GetValue().split(" ", 1)
            if usuario[0]=="@" and len(usuario)>0 and len(texto)>0 and len(texto)<141:
                self.miTimeline.enviarMensajePrivado(usuario[1:], texto)
                self.tCtrlEscribir.SetValue("")
                #Coloco el contador a 140
                self.contLetrasQueQuedan = 140
                self.lbLetrasQueQuedan.SetLabel(str(self.contLetrasQueQuedan)+self.espacioslbLetrasQueQuedan)
                self.reflescarTL()
        
    
    def favoritearTweet(self, evento=None):
        '''
        Hace favorito el tweet seleccionado.
        '''
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        id=self.cronologia[indiceSeleccionado/2][3]
        #Añadir a favoritos el mensaje.
        co = modelos.Comunes()
        co.hacerFavorito(id)
        #Reflescar TL
        self.reflescarTL()
        
    def contestarTweet(self, evento=None):
        '''
        Prepara un tweet para hacerle reply.
        '''
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        self.contestarTweetIDTuit = self.cronologia[indiceSeleccionado/2][3]
        usuario = self.cronologia[indiceSeleccionado/2][1]
        self.contestarTweetActivado = True
        self.tCtrlEscribir.SetValue(usuario[0:(usuario.find("("))])
        
    def retweetNativoEstado(self, evento=None):
        '''
        Hace RT nativo un tweet.
        '''
        #Obtener la id de self.cronologia (suele ser el mismo indice que el seleccionado
        #de self.listCtrlListaTweets, pero tener cuídado porque se puede seleccionar el 
        #mensaje (filas impares) o el @(filas pares, contando el 0)).
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        id=self.cronologia[indiceSeleccionado/2][3]
        #Hacer retweet del mensaje.
        co = modelos.Comunes()
        co.hacerRetweet(id)
        #Reflescar TL
        self.reflescarTL()
        
    def pegaTexto(self, evento=None):
        #Encuentra urls y las acorta usando bit.ly.
        #Una URL comienza por http:// o https:// y termina por espacio. Así que primero 
        #hacemos split y buscamos una cadena que comience por http:// o https://
        #1º Sacar texto del portapapeles
        def intercambia(urlsNuevas, elTexto):
            resIntercambia=""
            cont = 0
            for cosa in elTexto.split():
                if (cosa[0:4]=="http"):
                    resIntercambia = resIntercambia + (" ") + urlsNuevas[cont]
                    cont = cont + 1
                else:
                    resIntercambia = resIntercambia + " " + cosa
            return resIntercambia[1:] #Nos cargamos primer espacio.
        
        success = False
        data = wx.TextDataObject() 
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(data)
            wx.TheClipboard.Close()
        if success:
            texto=data.GetText()
            #Separar en palabras el texto y localizar palabras que comiencen por http y 
            #añadirlas a urlsAAcortar.
            urlsAAcortar = filter((lambda palabra: palabra[0:4]=="http"), texto.split())
            if len(urlsAAcortar)>0:
                #Usar bit.ly para acortar todas las urls.
                co = modelos.Comunes()
                urlsCortas = map(co.acortarUrl, urlsAAcortar)
                #Cambiar los http por los de urlsCortas en el texto (todo estará en orden).
                res = intercambia(urlsCortas,texto)
                #Guardar res en portapapeles.
                datos = wx.TextDataObject()
                datos.SetText(res)
                if wx.TheClipboard.Open():
                    wx.TheClipboard.SetData(datos)
                    wx.TheClipboard.Close()
        #print evento.
        evento.Skip()
    
    def reflescarTL(self, evento=None):
        '''
        '''
        #Actualizo.
        nuevos = self.filtraTweets(self.miTimeline.actualizar(self.LIMITE_DE_TUITS), self.listaLosQueNoLeo, True)
        if (len(nuevos)>0):
            self.cronologia = nuevos + self.cronologia
            #Añado los nuevos elementos a la lista de imagenes y a listCtrlListaTweets.
            indice=0
            nuevoCont=0
            for i in nuevos:
                #Actualizar lista de imagenes.
                aux=self.listaDeImagenesTL.Add(wx.Bitmap(i[0],wx.BITMAP_TYPE_ANY))
                #Añadir @ y texto
                index = self.listCtrlListaTweets.InsertStringItem(nuevoCont, "")
                self.listCtrlListaTweets.SetStringItem(index, 1, i[1])
                #Inicio colocar @nick en negrita
                #elElemento=self.listCtrlListaTweets.GetItem(index)
                #font = elElemento.GetFont()
                #font.SetWeight(wx.FONTWEIGHT_BOLD)
                #font.SetPointSize(8)
                #elElemento.SetFont(font)
                #self.listCtrlListaTweets.SetItem(elElemento)
                #Fin colocar @nick en negrita
                #Inicio cambiar color del fondo.
                self.listCtrlListaTweets.SetItemBackgroundColour(nuevoCont, self.COLOR_NO_LEIDO)
                #Fin cambiar color del fondo.
                nuevoCont = nuevoCont + 1
                #Añadir imagen y status
                #img = indice%(aux+1)
                index = self.listCtrlListaTweets.InsertImageItem(nuevoCont, aux)#img)
                self.listCtrlListaTweets.SetStringItem(index, 1, self.separaEnLineasDe22emes(i[2].replace("\n"," ").replace("&lt;","<").replace("&gt;",">"), self.miDc))
                #Inicio cambiar color del fondo.
                self.listCtrlListaTweets.SetItemBackgroundColour(nuevoCont, self.COLOR_NO_LEIDO)
                #Fin cambiar color del fondo.
                nuevoCont = nuevoCont + 1
                indice = indice + 1
            self.listCtrlListaTweets.Refresh()
    
    def decrementaOIncrementaContador(self, evento=None):
        #Si ha pulsado la tecla retroceso (8) o supr (127) incrementa contador.
        #En caso contrario lo decrementa.
        #codigoTecla=evento.GetKeyCode()
        self.contLetrasQueQuedan = 140-len(self.tCtrlEscribir.GetValue())
        self.lbLetrasQueQuedan.SetLabel(str(self.contLetrasQueQuedan) + " - "+self.nomFicheroListaNoVerUsado)#+self.espacioslbLetrasQueQuedan)
        if self.contLetrasQueQuedan<0:
            self.btDM.Enable(False)
            self.btTweet.Enable(False)
        elif not self.btTweet.IsEnabled():
            self.btDM.Enable(True)
            self.btTweet.Enable(True)
        
        evento.Skip()
    
    def corregirOrtografiaEnTuit(self, evento=None):
        self.sugerenciasOrtografia #{palabra: ['correcciones']}
        if self.tCtrlEscribir.GetValue()!="":
            corrector = pyaspell.pyaspell.Aspell(("lang", "es"))#Instalar en synaptics el aspell-es
            todasPalabras = self.tCtrlEscribir.GetValue().split()
            resto = ""
            for palabra in todasPalabras:
                if not corrector.check(str(palabra)) and palabra[0:4]!="http":
                    fg = wx.Colour(255, 0, 0)#Colorear de rojo para avisar que está mal.
                    at = wx.TextAttr(fg)
                    inicio = len(resto)
                    self.tCtrlEscribir.SetStyle(inicio, inicio+len(palabra)+1, at)
                    self.sugerenciasOrtografia.update({palabra:corrector.suggest(str(palabra))})
                resto = resto + (" " +palabra if resto!="" else palabra)
    
    def subirImagenUsandoTwitPic(self, evento=None):
        sit = subirImagenATwitpic.SubirImagenATwitpic(None, -1, "")
        sit.Show()
    
    def casillaSeleccionada(self, evento=None):
        '''
        '''
        #Si la casilla es un tweet (fila impar), seleccionar fila superior.
        #Si la casilla es un @nick (fila par y el 0), seleccionar también fila inferior.
        indice = self.listCtrlListaTweets.GetFirstSelected()
        indiceRes = indice+1 if (indice%2==0) else indice-1
        self.listCtrlListaTweets.Select(indiceRes)
        #Marcar como leídas las dos casillas pintandolas de self.COLOR_LEIDO
        self.listCtrlListaTweets.SetItemBackgroundColour(indice, self.COLOR_LEIDO)
        self.listCtrlListaTweets.SetItemBackgroundColour(indiceRes, self.COLOR_LEIDO)
    
    def enviarTweet(self, evento=None):
        '''
        El tuitear de toda la vida.
        '''
        if self.tCtrlEscribir.GetValue()!="":
            if self.contestarTweetActivado:
                self.miTimeline.contestarTweetConTweet(self.tCtrlEscribir.GetValue(), self.contestarTweetIDTuit)
                self.contestarTweetActivado = False
            else:
                self.miTimeline.enviarTweetATimeline(self.tCtrlEscribir.GetValue())
            self.tCtrlEscribir.SetValue("")
            #Coloco el contador a 140
            self.contLetrasQueQuedan = 140
            self.lbLetrasQueQuedan.SetLabel(str(self.contLetrasQueQuedan)+self.espacioslbLetrasQueQuedan)
            self.reflescarTL()
        
    def salir(self, evento=None):
        self.terminado = True
        self.Destroy()
        
        
class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = ControladorPrincipal(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
        
