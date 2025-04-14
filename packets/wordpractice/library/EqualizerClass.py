import soundfile as sf
from fastdtw.fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
import scipy.signal as signal


class EqualizerClass():
    def apply(_self,audio):
        bands = [(200,350),(350,600),(600,2000),(2000,3000),(3000,8000)]
        gains = [-3,2,1,1,3,1]  # en decibelios

        # procesamiento de ecualización 
        order = 4
        b_coeffs = []
        a_coeffs = []
        for i, band in enumerate(bands):
            f_low, f_hight = band
            nyquist = 0.5 * 32000 # Es el doble de 16khz
            low = f_low / nyquist
            hight = f_hight / nyquist
            b, a = signal.butter(order, [low,hight], btype='bandpass')
            if (not gains[i]==0):
                b_coeffs.append(b * gains[i])
                a_coeffs.append(a)

        # Apply each filter to the input signal
        filtered = np.zeros_like(audio)
        for b, a in zip(b_coeffs, a_coeffs):
            filtered += signal.lfilter(b, a, audio)

        return filtered    