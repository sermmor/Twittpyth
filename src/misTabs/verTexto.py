#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.lib.agw.hyperlink

'''
Created on 11/02/2011

@author: sergio
'''

class VerTexto(wx.ScrolledWindow):
    '''
    classdocs
    '''
    
    def __init__(self, *args, **kwds):
        '''
        Constructor
        '''
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self.tCtrlInfoTweet = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_AUTO_URL)
        
        self.__set_properties()
        self.__do_layout()
        
    def __set_properties(self):
        self.tCtrlInfoTweet.SetMinSize((600, 500))
        
    def __do_layout(self):
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.tCtrlInfoTweet, 0, 0, 0)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        
    def anyadirTexto(self, texto):
        self.tCtrlInfoTweet.SetValue(texto)

        