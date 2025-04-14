import librosa.feature as feature
import librosa as librosa
from .CorrelateClass import CorrelateClass
from .GainPPPClass import GainPPPClass
import numpy as np



class MfccClass(CorrelateClass):
    # Variables Mfcc
    __mfcc_target = []
    __mfcc_test = []
    __gain_rsm = GainPPPClass()  

    def MfccDelete(self, y,x,sr_y,sr_x):

        self.__mfcc_target = feature.mfcc(y=y, sr=sr_y, n_mfcc=13, n_fft=1024, hop_length=512, n_mels=32, lifter=20,fmin=20,fmax=8000)
        self.__mfcc_test = feature.mfcc(y=x, sr=sr_x, n_mfcc=13, n_fft=1024, hop_length=512, n_mels=32, lifter=20,fmin=20,fmax=8000)
        
        ## Normalización
        self.__mfcc_target = librosa.util.normalize(self.__mfcc_target, norm=2)
        self.__mfcc_test = librosa.util.normalize(self.__mfcc_test, norm=2)

        return self

    def getMfccTarget(self):
        return self.__mfcc_target

    def getMfccTest(self):
        return self.__mfcc_test    
    

    
