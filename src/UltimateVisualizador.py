#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Thu Feb 10 22:00:56 2011

import wx
import wx.lib.agw.aui as aui
import misTabs.verTexto
import misTabs.verImagen
import misTabs.verImagenYTexto
import misTabs.verTL
import misTabs.VentanaOpciones

# begin wxGlade: extracode
# end wxGlade

class AUIManager(aui.AuiManager):
    """
    Clase manejadora del AUI.
    """
    def __init__(self, ventana):
        '''
        Constructor.
        '''
        aui.AuiManager.__init__(self)
        self.SetManagedWindow(ventana)
        
class AUINotebook(aui.AuiNotebook):
    '''
    Clase que maneja el notebook que lleva las pestañas del editor, conversor, generador, demostrador y resultados.
    '''
    def __init__(self, parent, *args, **kwds):
        '''
        Constructor.
        '''
        aui.AuiNotebook.__init__(self, parent=parent)
        self.default_style = aui.AUI_NB_DEFAULT_STYLE | aui.AUI_NB_TAB_EXTERNAL_MOVE | wx.NO_BORDER
        self.SetWindowStyleFlag(self.default_style)
        self.hayTabs=False
        self.listaTabs = []
        #self.parametros=(args, kwds)
        
        
    def anyadirPagina(self, nombreClasePagina, nombreDePagina, aui_mgr, exportado):
        '''
        Añade una página al notebook.
        '''
        tab=nombreClasePagina(self, -1, style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL|wx.FULL_REPAINT_ON_RESIZE)
        #NUEVO IF
        
        #if nombreDePagina=="Logicas":
        #    tab.referenciaAPrincipal(exportado)
        #elif nombreDePagina=="Demostrador":
        #    tab.pasarReferenciaDeMarco(exportado)
        #elif nombreDePagina=="Editor":
        #    tab.pasarReferenciaDeMarco(exportado)
        #elif nombreDePagina=="Generador aleatorio":
        #    tab.pasarReferenciaDeMarco(exportado)
        self.AddPage(tab, nombreDePagina, False)
        self.listaTabs = self.listaTabs + [tab]
        if not self.hayTabs:
            #Actualizar estilos de pestañas.
            todoPane = aui_mgr.GetAllPanes()
            self.hayTabs = True
            #if instruccion!="abrirFicheroFormula":
            #    todoPane=aui_mgr.GetAllPanes()
            #else:
            #    todoPane=aui_mgr.aui_mgr.GetAllPanes()
            for pane in todoPane:
                nb = pane.window
                nb.SetArtProvider(aui.ChromeTabArt())
                nb.Refresh()
                nb.Update()



class Visualizador(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Visualizador.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        #Variables
        self.ptrPrincipal = None
        
        #self.note_visualizador = wx.Notebook(self, -1, style=0)
        #self.notebook_1_pane_1 = wx.Panel(self.note_visualizador, -1)
        
        # create the AUI manager
        self.aui_mgr = AUIManager(self)
        # create the AUI Notebook
        self.note_visualizador = AUINotebook(self,*args,**kwds)
        # add notebook to AUI manager
        self.aui_mgr.AddPane(self.note_visualizador, aui.AuiPaneInfo().Name("notebook_content").CenterPane().PaneBorder(False))
        self.aui_mgr.Update()
        # fin AUI
        
        #self.tCtrlInfoTweet = wx.TextCtrl(self.notebook_1_pane_1, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_AUTO_URL)
        
        self.__set_properties()
        self.__do_layout()
        #Evento al salir
        wx.EVT_CLOSE(self, self.salir)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Visualizador.__set_properties
        self.SetTitle("Visualizador")
        self.SetMinSize((620, 520))
        #self.tCtrlInfoTweet.SetMinSize((600, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Visualizador.__do_layout
        #sizer_1 = wx.BoxSizer(wx.VERTICAL)
        #sizer_2 = wx.BoxSizer(wx.VERTICAL)
        
        #Añadir páginas al self.note_visualizador
        #self.note_visualizador.anyadirPagina(misTabs.verTexto.VerTexto, "Ver el texto", self.aui_mgr, None)
        #self.note_visualizador.anyadirPagina(misTabs.verTexto.VerTexto, "Ver el texto", self.aui_mgr, None)
        #self.note_visualizador.anyadirPagina(misTabs.verTexto.VerTexto, "Ver el texto", self.aui_mgr, None)
        
        
        #Cosas extrañas:
        #tab=self.note_visualizador.GetPage(0)#Me busco la primera página.
        #self.note_visualizador.SetSelectionToWindow(tab)#Traer página el frente.
        notebook_style= self.note_visualizador.default_style
        notebook_style &= ~(aui.AUI_NB_CLOSE_BUTTON |
                                 aui.AUI_NB_CLOSE_ON_ACTIVE_TAB |
                                 aui.AUI_NB_CLOSE_ON_ALL_TABS)
        self.note_visualizador.SetWindowStyleFlag(notebook_style)
        self.note_visualizador.Refresh()
        self.note_visualizador.Update()
        
        #self.note_visualizador.AddPage(self.notebook_1_pane_1, "tab1")
        
        #sizer_2.Add(self.tCtrlInfoTweet, 0, 0,0)
        
        #self.notebook_1_pane_1.SetSizer(sizer_2)
        
        #sizer_1.Add(self.note_visualizador, 1, wx.EXPAND, 2)
        
        #self.SetSizer(sizer_1)
        #sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
    #Necesarios.
    def setPtrPrincipal(self, ctrl):
        self.ptrPrincipal = ctrl
    
    def salir(self, evento=None):
        self.ptrPrincipal.visualizadorEstaCerrado = True
        self.Destroy()
    
    #Pestañas.
    def abrirPestanyaDeTexto(self, tituloTexto, texto):
        self.note_visualizador.anyadirPagina(misTabs.verTexto.VerTexto, tituloTexto, self.aui_mgr, None)
        self.note_visualizador.listaTabs[-1].anyadirTexto(texto)
        
    def abrirPestanyaDeImagen(self, tituloImagen, urlImagen):
        self.note_visualizador.anyadirPagina(misTabs.verImagen.VerImagen, tituloImagen, self.aui_mgr, None)
        self.note_visualizador.listaTabs[-1].anyadirImagen(urlImagen)
    
    def abrirPestanyaDeTL(self, tituloPestanya, listaEstados, controla):
        self.note_visualizador.anyadirPagina(misTabs.verTL.VerLista, tituloPestanya, self.aui_mgr, {"tituloPestanya":tituloPestanya, "listaEstados":listaEstados})
        self.note_visualizador.listaTabs[-1].dameControladorYVisualizador(controla, self)
        self.note_visualizador.listaTabs[-1].anyadirLista(listaEstados, tituloPestanya=="DM")
    
    def abrirPestanyaDeImagenYTexto(self, titulo, url, texto, urlImagen):
        self.note_visualizador.anyadirPagina(misTabs.verImagenYTexto.VerImagenYTexto, titulo, self.aui_mgr, None)
        #self.note_visualizador.listaTabs[-1].anyadirURL(url)
        self.note_visualizador.listaTabs[-1].anyadirTexto(texto)
        self.note_visualizador.listaTabs[-1].anyadirImagen(urlImagen)
        
    def abrirPestanyaDeOpciones(self):
        #Las opciones modificadas no se modificarán hasta reiniciar la aplicación.
        self.note_visualizador.anyadirPagina(misTabs.VentanaOpciones.OpcionesTwittpyth, "Opciones", self.aui_mgr, None) 
    
# end of class Visualizador


