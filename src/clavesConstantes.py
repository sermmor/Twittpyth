#!/usr/bin/env python
# -*- coding: utf-8 -*
'''
Created on 06/02/2011

@author: sergio
'''

class clavesConstantes(object):
    '''
    Contiene como "constantes" todas las claves necesarias para la aplicación.
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        #Constantes para loguearse.
        self.CONSUMER_KEY = ''
        self.CONSUMER_SECRET = ''
        self.ACCESS_KEY = ''
        self.ACCESS_SECRET = ''
        #Constantes para bit.ly
        self.BIT_LY_USERNAME = ''
        self.BIT_LY_API_KEY = ''
        #Claves para twitpic
        self.TWITPIC_SERVICE_KEY = ''
        #Directorio de la aplicación
        self.PATH_APP = ''
        
