#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from wx.lib.agw import ultimatelistctrl as ULC
import wx.lib.agw.hyperlink
import sys
import modelos

'''
Created on 11/02/2011

@author: sergio
'''

class VerLista(wx.ScrolledWindow):
    '''
    classdocs
    '''
    
    def __init__(self, *args, **kwds):
        '''
        Constructor
        '''
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        #CONSTANTES
        self.COLOR_TUITS = wx.Colour(225, 255, 255)#(Rojo, Verde, Azul)
        #VARIABLES
        self.cronologia = None
        self.esDM = False
        self.primeraVezClickDerecho = False
        self.controla = None
        self.visuali = None
        
        #self.tCtrlInfoTweet = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_AUTO_URL)
        self.listCtrlListaTweets = ULC.UltimateListCtrl(self, -1, agwStyle=ULC.ULC_REPORT|ULC.ULC_HAS_VARIABLE_ROW_HEIGHT|ULC.ULC_SEND_LEFTCLICK)
        
        self.__set_properties()
        self.__do_layout()
        
        self.listCtrlListaTweets.Bind(wx.EVT_LIST_ITEM_SELECTED, self.casillaSeleccionada)
        wx.EVT_LIST_ITEM_RIGHT_CLICK(self, self.listCtrlListaTweets.GetId(), self.clicDerechoEstado)
    
    def __set_properties(self):
        self.listCtrlListaTweets.SetMinSize((600, 500))
        
    def __do_layout(self):
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.listCtrlListaTweets, 0, 0, 0)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        
    def dameControladorYVisualizador(self, controla, visuali):
        self.controla = controla
        self.visuali = visuali
        
    def separaEnLineasDe22emes(self, cadenaAFragmentar, dc):
        '''
        Fragmenta en líneas de 486 pixeles (width).
        '''
        #Para entender esto:
        #VER http://stackoverflow.com/questions/2455255/how-to-get-the-width-of-a-string-in-pixels
        #Y VER http://www.wxpython.org/docs/api/wx.DC-class.html#GetTextExtent
        ANCHO_PIXELES = 486 #286
        res = ""
        width, height = dc.GetTextExtent(cadenaAFragmentar)
        if width>ANCHO_PIXELES: 
            temporal = ""
            fragmentos = cadenaAFragmentar.split()
            for cad in fragmentos:
                temporal2 = temporal + " " + cad
                width, height = dc.GetTextExtent(" "+temporal2)
                if width>ANCHO_PIXELES:
                    res = res + " " + temporal+"\n"
                    temporal = cad
                else:
                    temporal = temporal2
            res = res + " " + temporal
        else:
            res = cadenaAFragmentar
        return res
        
    def anyadirLista(self, listaEstados, esDM):
        self.cronologia = listaEstados
        self.esDM = esDM
        co = modelos.Comunes()
        lista = co.listaTuplasRutaImagenNickEstadoID(listaEstados, esDM) 
        #Inicio declaración lista de tweets
        self.listCtrlListaTweets.InsertColumn(0, "", width=50)
        self.listCtrlListaTweets.InsertColumn(1, "", width=550)#450
        #Me pillo mi timeline
        #self.miTimeline = Timeline(self.LIMITE_DE_TUITS)#(200)
        #la lista = self.cronologia = self.miTimeline.listaTuplasRutaImagenNickEstadoID()
        #Guardamos las imágenes (tamaño=(48x48)) en una lista de imagenes, para luego exportarlas 
        #al UltimateListCtrl.
        self.listaDeImagenesTL=wx.ImageList(48,48,True)
        aux=0
        for imag in lista:
            aux=self.listaDeImagenesTL.Add(wx.Bitmap(imag[0],wx.BITMAP_TYPE_ANY))
        #Asignar lista de imagenes.
        self.listCtrlListaTweets.SetImageList(self.listaDeImagenesTL, wx.IMAGE_LIST_SMALL)
        #Preparar dc para lo de la separación en líneas.
        f = self.GetFont()
        self.miDc = wx.WindowDC(self)
        self.miDc.SetFont(f)
        indice=0
        #self.ultimoIndice = 0 #DEPURAR
        for i in lista:
            #Añadir @ y texto
            index = self.listCtrlListaTweets.InsertStringItem(sys.maxint, "")
            self.listCtrlListaTweets.SetStringItem(index, 1, i[1])
            #Inicio cambiar color del fondo.
            self.listCtrlListaTweets.SetItemBackgroundColour(index, self.COLOR_TUITS)
            #Fin cambiar color del fondo.
            #Añadir imagen y status
            img = indice%(aux+1)
            index = self.listCtrlListaTweets.InsertImageItem(sys.maxint, img)
            self.listCtrlListaTweets.SetStringItem(index, 1, self.separaEnLineasDe22emes(i[2].replace("\n"," ").replace("&lt;","<").replace("&gt;",">"), self.miDc)+"\n____________________________________________\n"+i[4])
            #Inicio cambiar color del fondo.
            self.listCtrlListaTweets.SetItemBackgroundColour(index, self.COLOR_TUITS)
            #Fin cambiar color del fondo.
            indice = indice+1
        #Fin declaración lista de tweets
        self.listCtrlListaTweets.Select(0)
    
    def casillaSeleccionada(self, evento=None):
        '''
        '''
        #Si la casilla es un tweet (fila impar), seleccionar fila superior.
        #Si la casilla es un @nick (fila par y el 0), seleccionar también fila inferior.
        indice = self.listCtrlListaTweets.GetFirstSelected()
        indiceRes = indice+1 if (indice%2==0) else indice-1
        self.listCtrlListaTweets.Select(indiceRes)
    
    def clicDerechoEstado(self, evento=None):
        if self.primeraVezClickDerecho:
            self.primeraVezClickDerecho = False
        else:
            indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
            estado=self.cronologia[indiceSeleccionado/2].getMensaje().text
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
            arrobas = filter(lambda elem: elem[0]=="@", estado.split())
            for contacto in arrobas:
                nuevaID = wx.NewId()
                con = contacto[:-1] if(contacto[-1]==":") else contacto 
                self.idsPorPerfilVisualiza.update({nuevaID:con})
                menu.Append(nuevaID, con)
                wx.EVT_MENU( menu, nuevaID, self.MenuSeleccionVisualPerfilCb)
                
            #Ir a perfil en navegador.
            self.urlDePerfilSeleccionado = "http://twitter.com/"+self.cronologia[indiceSeleccionado/2].getMensaje().user.screen_name
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
            
    def MenuSeleccionVisualPerfilCb(self, evento=None):
        co = modelos.Comunes()
        self.controla.verFlujoDeUsuarioEnVisualizador(self.idsPorPerfilVisualiza[evento.GetId()], co)
        
    def MenuSelectionCb(self, evento=None):
        #Abrir link
        abreLinks = wx.lib.agw.hyperlink.HyperLinkCtrl(self, wx.NewId())
        abreLinks.GotoURL(self.idsPorLink[evento.GetId()], True, True)
    
    def MenuSeleccionVisualCb(self, evento=None):
        self.controla.verImagenEnVisualizador(self.idsPorLinkVisualiza[evento.GetId()])
    
    def TraduceTweet(self, evento=None):
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        texto = self.cronologia[indiceSeleccionado/2].getMensaje().text
        
        tgt = modelos.TraductorGoogleTranslate()
        textoTraducido=tgt.translate(texto, to="es") #Uso autodeteción de idioma.
        
        if self.controla.visualizadorEstaCerrado:
            self.controla.abrirVisualizador()
        self.controla.miVisualizador.abrirPestanyaDeTexto("Tuit traducido", "Texto original: \n"+texto+"\n\nTraducción automática: \n"+textoTraducido)
    
    def copiarTuit(self, evento=None):
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        #Guardar estado en portapapeles.
        datos = wx.TextDataObject()
        datos.SetText(self.cronologia[indiceSeleccionado/2].getMensaje().text)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(datos)
            wx.TheClipboard.Close()
    
    def contestarTweet(self, evento=None):
        '''
        Prepara un tweet para hacerle reply.
        '''
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        self.controla.contestarTweetIDTuit = self.cronologia[indiceSeleccionado/2].getMensaje().id
        usuario = "@"+self.cronologia[indiceSeleccionado/2].getMensaje().user.screen_name
        self.controla.contestarTweetActivado = True
        self.controla.tCtrlEscribir.SetValue(usuario)
    
    def favoritearTweet(self, evento=None):
        '''
        Hace favorito el tweet seleccionado.
        '''
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        id=self.cronologia[indiceSeleccionado/2].getMensaje().id
        #Añadir a favoritos el mensaje.
        co = modelos.Comunes()
        co.hacerFavorito(id)
        #Reflescar TL
        self.controla.reflescarTL()
    
    def retweetNativoEstado(self, evento=None):
        '''
        Hace RT nativo un tweet.
        '''
        #Obtener la id de self.cronologia (suele ser el mismo indice que el seleccionado
        #de self.listCtrlListaTweets, pero tener cuídado porque se puede seleccionar el 
        #mensaje (filas impares) o el @(filas pares, contando el 0)).
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        id=self.cronologia[indiceSeleccionado/2].getMensaje().id
        #Hacer retweet del mensaje.
        co = modelos.Comunes()
        co.hacerRetweet(id)
        #Reflescar TL
        self.controla.reflescarTL()
        
    def RTConComentario(self, evento=None):
        indiceSeleccionado = self.listCtrlListaTweets.GetFirstSelected()
        usuario = self.cronologia[indiceSeleccionado/2].getMensaje().user.screen_name
        estado = self.cronologia[indiceSeleccionado/2].getMensaje().text
        self.controla.tCtrlEscribir.SetValue("RT "+usuario+" "+estado)
    
    
