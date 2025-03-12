import numpy as np
from scipy import constants

class Trans_Intensity:
    def __init__(self, ro: float, f: float, n_real: float, n_imag: float, d: float):
        self.ro = ro
        self.R = ro**2
        self.f = f
        self.n_real = n_real
        self.n_imag = n_imag
        self.d = d
        self.F = 4 * self.R / ((1 - self.R)**2)
    
    def __call__(self, delta: np.ndarray) -> np.ndarray:
        phase = (2 * np.pi * self.f / constants.c) * (delta + self.d * self.n_real)
        absorption = np.exp(-4 * np.pi * (self.f / constants.c) * self.d * self.n_imag) # https://en.wikipedia.org/wiki/Refractive_index#Complex_refractive_index
        return absorption / (1 + self.F * np.sin(phase)**2)
    
    def get_intensity(self, delta: np.ndarray) -> np.ndarray:
        return self(delta)