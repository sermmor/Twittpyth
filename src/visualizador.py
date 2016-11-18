#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Thu Feb 10 22:00:56 2011

import wx

# begin wxGlade: extracode
# end wxGlade



class Visualizador(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Visualizador.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.note_visualizador = wx.Notebook(self, -1, style=0)
        self.notebook_1_pane_1 = wx.Panel(self.note_visualizador, -1)
        self.tCtrlInfoTweet = wx.TextCtrl(self.notebook_1_pane_1, -1, "", style=wx.TE_PROCESS_ENTER|wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_AUTO_URL)
        
        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Visualizador.__set_properties
        self.SetTitle("Visualizador")
        self.SetMinSize((620, 520))
        self.tCtrlInfoTweet.SetMinSize((600, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Visualizador.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        self.note_visualizador.AddPage(self.notebook_1_pane_1, "tab1")
        
        sizer_2.Add(self.tCtrlInfoTweet, 0, 0,0)
        
        self.notebook_1_pane_1.SetSizer(sizer_2)
        
        sizer_1.Add(self.note_visualizador, 1, wx.EXPAND, 2)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# end of class Visualizador


class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_Visualizador = Visualizador(None, -1, "")
        self.SetTopWindow(frame_Visualizador)
        frame_Visualizador.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
