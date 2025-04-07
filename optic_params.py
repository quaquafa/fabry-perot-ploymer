import numpy as np
from scipy import constants

class Trans_Intensity:
    def __init__(self,
                 ro: float,
                 f: float,
                 n: float,
                 kappa : float,
                 d: float):
        self.ro = ro
        self.R = ro**2
        self.f = f
        self.n = n
        self.kappa = kappa
        self.d = d
        self.A = np.exp(-4 * np.pi * self.kappa * self.d * self.f / constants.c)
        self.R_absorb = self.R * self.A
        self.F = 4 * self.R_absorb / ((1 - self.R_absorb)**2)
    
    def __call__(self, delta: np.ndarray) -> np.ndarray:
        phase = (2 * np.pi * self.f / constants.c) * (delta + self.d * self.n)
        return 1 / (1 + self.F * np.sin(phase)**2)
    
    def get_intensity(self, delta: np.ndarray) -> np.ndarray:
        return self(delta)
    def update_R_absorb(self):
        self.R = self.ro**2
        self.A = np.exp(-4 * np.pi * self.kappa * self.d * self.f / constants.c)
        self.R_absorb = self.R * self.A

    def update_F(self):        
        self.F = 4 * self.R_absorb / ((1 - self.R_absorb)**2)
