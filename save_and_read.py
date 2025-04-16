import numpy as np 
import pandas as pd
import os
import tkinter
from tkinter import filedialog

def save_calc(event, intensity, delta_values):
    intensity = intensity.get_intensity(delta_values)
    
    real_deltas = delta_values * 1e3 
    
    df = pd.DataFrame({"#Δ (мм)": real_deltas, "Интенсивность": intensity})    
    
    df.to_csv('saved.csv', index=False)
    
    print("Сохранено (saved.csv)")

def read_data():
    try:
        tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
        file_path = filedialog.askopenfilename()
        df = pd.read_csv(file_path)
        return df["#Δ (мм)"].values, df["Интенсивность"].values
    except:
        pass