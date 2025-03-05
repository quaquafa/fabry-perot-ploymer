import numpy as np
from scipy import constants

class Trans_Intensity:
    def __init__(self,
                 ro:float, # Коэффицент отражения 
                 f:float, # Частота волны (Гц)
                 n:float, # Преломление плёнки
                 d:float, # Ширина плёнки (м)
                 ):
        self.ro = ro
        self.R = ro**2 
        self.f = f 
        self.n = n 
        self.d = d
        self.F = 4 * self.R / ((1 - self.R)**2) # Коэфф. резкости
    
    def __call__(self,
                 delta:float # Расстояние между стёклами
                ):
        phase = (2 * np.pi * self.f / constants.c) * (delta + self.d * self.n)
        return 1 / (1 + self.F * (np.sin(phase))**2)
    
    def get_intensity(self, delta):
        return self(delta)
    