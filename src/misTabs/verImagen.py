#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

'''
Created on 11/02/2011

@author: sergio
'''

class VerImagen(wx.ScrolledWindow):
    '''
    classdocs
    '''
    
    def __init__(self, *args, **kwds):
        '''
        Constructor
        '''
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self.sBImagen = wx.StaticBitmap(self, -1)
        
        #self.__set_properties()
        self.__do_layout()
        
    #def __set_properties(self):
    #    self.sBImagen.SetMinSize((600, 500))
        
    def __do_layout(self):
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.sBImagen, 0, 0, 0)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        
    def anyadirImagen(self, rutaImagen):
        #Ajustar la imagen a un tamaño antes de mostrarla por pantalla (no guardarla 
        #con este nuevo tamaño). ¡Cuidado con la relación ancho*alto!
        imagen = wx.Image(rutaImagen,wx.BITMAP_TYPE_ANY)
        #1º fijo un alto (280px).
        nuevoAlto = 300
        #2º Extraer ancho y alto.
        viejoAncho, viejoAlto = imagen.GetSize()
        #3º Por regla de tres calculamos el ancho: nuevoAncho=(nuevoAlto*viejoAncho)/viejoAlto.
        nuevoAncho=(nuevoAlto*viejoAncho)/viejoAlto
        #4º Reduzco imagen al nuevo tamaño (sin guardarla).
        imagen.Rescale(nuevoAncho,nuevoAlto,quality=wx.IMAGE_QUALITY_HIGH)
        #5º Muestro imagen reducida por pantalla.
        self.sBImagen.SetBitmap(bitmap=imagen.ConvertToBitmap())

        