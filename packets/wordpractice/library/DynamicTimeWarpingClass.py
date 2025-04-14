import soundfile as sf
from fastdtw.fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
import librosa.feature as feature
import librosa as librosa
import numpy.typing as npt
from .EqualizerClass import EqualizerClass
from .MfccClass import MfccClass
from tslearn import metrics as tslearn_metrics 
from scipy.signal import correlate

class DynamicTimeWarpingClass(MfccClass):
    __equalizer = EqualizerClass()

    ## El original para la practica 
    sr_test = []
    fs_test = 0

    ## El de evaluación fonetica 

    sr_review = []
    fs_review = 0
    
    #La Distancia entre dos señales
    test_distance = []
    review_path = []
    test_dist =[]

    # Valor de x y x
    __x = []
    __y = []
    __acum_distance = []

    __dist_dtw = 0

    __std_dev = 0
    __mean = 0

    def getStdDev(self):
        return self.__std_dev

    def getMedia(self):
        return self.__mean
    
    def getTest(self):
        return self.sr_test

    def getReview(self):
        return self.sr_review

    def reviewSound(self):
        # Ecualizar Audios 

        # Este metodo eliminar cualquier sonido que no sea importancia. 
        
        y=self.getMfccTarget()
        x=self.getMfccTest()

        self.__dist_dtw = tslearn_metrics.dtw(y[0],x[0], global_constraint="sakoe_chiba", sakoe_chiba_radius=3)

        self.lcss_path, sim_lcss = tslearn_metrics.lcss_path(y[0],x[0], eps=1)

        self.__std_dev,self.__mean = self.CalculaDesviacionStandar(self.lcss_path,y[0],x[0],False)

        self.test_distance ='%.4f' % round(abs(self.__dist_dtw),4)

        return self
    
    def getDistDtw(self):
        return self.__dist_dtw
    
    def getAcumDistance(self):
        return self.__acum_distance
    
    def getDistance(self):
        return float(self.test_distance)
    
    def getPath(self):
        return self.lcss_path
    
    def getDist(self):
        return self.test_dist
    
    def CalculaDesviacionStandar(self,lcss_path,audio_tr,audio_ts, allData = True):
        info_p = []
        sample = []

        distance = 0
        ## Se cargan las distancias de intervalo
        for item in lcss_path:
            distance = float(abs(abs(float(audio_ts[item[1]])) - abs(float(audio_tr[item[0]]))))
            ##distance *= (10**13)
            distance*=100
            sample.append(round(distance,2))
        
        mean = np.mean(sample)
        std_dev = np.std(sample)

        max_dat = mean + (std_dev + 1)
        min_dat = mean - (std_dev + 1)


        info_p = [sample[i] for i in range(0,len(sample)) if  sample[i]>min_dat and sample[i]<max_dat]

        mean_info = np.mean(info_p)
        std_dev_info = np.std(info_p)

        # print("Media Población",mean_info,"Desviacion",std_dev_info)

        # print("Info Datos",info_p)

        considerados = len(info_p)
        muestra = len(sample)
        descartados = muestra - considerados
        porc_desv = float(considerados/muestra)

        if allData==False:
            return round(std_dev,4),round(mean,2)

        return round(std_dev,4), round(porc_desv*100,2),round(mean,2),round(muestra,2),considerados,descartados,sample
    def alinear_señales(self,signal1, signal2):
        """
        Alinea dos señales de audio que son muy similares pero pueden estar desfasadas en el tiempo.

        Retorna:
            señal_alineada (numpy.ndarray): Señal de audio 2 alineada con la señal 1
        """
        # Calcula la cross-correlación entre las dos señales
        corr = correlate(signal1, signal2, mode='full')
        # Encuentra el índice que maximiza la correlación
        max_corr_idx = np.argmax(corr)
        min_corr_idx = np.argmin(corr)

        # max_corr_idx2 = np.argmax(signal2)
        #print("max_corr_idx",max_corr_idx)
        #print("min_corr_idx",min_corr_idx)
        # print("max_corr_idx 2",max_corr_idx2)
        #print("len(signal1)",len(signal1))

        # Calcula el desfase
        if (max_corr_idx<min_corr_idx):
            desfase = max_corr_idx - (len(signal1) + 1)
        else:
            desfase = (len(signal1) + 1) - max_corr_idx

        print("desfase",desfase)

        # Alinea la señal 2 con la señal 1
        señal_alineada = np.roll(signal2, desfase)

        return señal_alineada

    





