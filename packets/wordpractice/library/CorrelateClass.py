import numpy as np
from scipy.signal import correlate
from scipy.stats import pearsonr
import librosa.feature as feature
import librosa as librosa
from .GainPPPClass import GainPPPClass
import sys

sys.setrecursionlimit(505)

class CorrelateClass():
    __gain_ppp = GainPPPClass()

    valor_correlacion = 0
    valores = []
    min_corr = 0.00
    y2_posc_active = []
    __resp_correlation = False
    __long = 10
    __toDraw = False
    acum_long = 0
    direccion = ''
    __longIterado = 100
    __tam = 0
    __y_temp = 0
    __x_temp = 0
    def setLongIterado(self,numero):
        self.__longIterado = numero
        return
    def SearchCorrelation(self,file_target,file_test):
        y, sr = librosa.load(file_target,mono=True,sr=24000)
        x, srx = librosa.load(file_test,mono=True,sr=24000)

        x = self.__gain_ppp.igualPtoP(y,x)
        x = self.__stretchAudio(y,x,sr)

        y,x = self.__calcularLong(len(y),y,x)

        self.clearvars()

        #Se halla tambien el valor de Correlación de las señales
        self.direccion = "right"
        self.CorrelateVal(y,x,0,'right') 

        if (not self.min_corr<-0.1):
            self.acum_long = 0
            self.valor_correlacion = self.min_corr
            self.direccion = "left"
            self.CorrelateVal(y,x,0,'left')
        
        if (self.min_corr<-0.01):
            # Existe algo de Correlación Negativa 
            self.__resp_correlation = True

        if (self.__resp_correlation):
            ## Los dos audios estan correlacionado
            return self.__y_temp,self.__x_temp,sr
        
        return y, x,sr
    
    def CorrelateVal(self,y1,y2,interado,arrow):
        # Asegúrate de que las señales tengan la misma longitud
        min_len = min(len(y1), len(y2)) if interado==0 else len(y1)

        interado+=1
        desplz = 0 if interado==0 else 1

        self.acum_long += int(self.__long) if interado>0 else 0

        y1 = y1[0:min_len]
        y2 = self.__procArrow(arrow,desplz,min_len,y2)
 

        y2_d = -y2 # Desafasada a 180º

        correlation, p_value = pearsonr(y1,y2_d)

        p_value = float('%.2f' % round(p_value,2))
        
        
        
        self.valores = [p_value,self.min_corr]
        ant_min_corr = self.min_corr
        self.min_corr = min(correlation,self.min_corr)
        self.valor_correlacion = '%.4f' % round(self.min_corr,4)

        if (self.min_corr<ant_min_corr):
            ## Este en todo caso la mejor correlación por lo cual la señal puede dar una
            ## mejor evaluación en el DTW
            self.__x_temp = y2
            self.__y_temp = y1

        # Solo funciona en pruebas con ipynb
        if (self.__toDraw): 
            self.__printGraphic(audio_l=y1,sr_l=22400,audio_r=y2,sr_r=22400,interado=interado)

        if (interado==self.__longIterado):
            self.__resp_correlation=False ## No hay problemas de cancelación no sigue interando
            return
            ## Si no existe correlación menor que -0.03 y que la Hipótesis nula tienda a cero (Se considera verdadero.). 
        self.CorrelateVal(y1,y2,interado,arrow) 

        return
    # La direccion del desplazamiento de la onda
    def __procArrow(self,arrow,desplz, min_len,y2):
        y2 = y2[0:min_len] if desplz==0 else self.__insertZero(arrow,min_len,y2)

        if desplz==1:
            y2 = self.__shiftWave(arrow,min_len,desplz,y2)

        return y2
    # Insertar Cero 
    def __insertZero(self,arrow,min_len,y2):
        return np.insert(y2,min_len,np.zeros(self.__long)) if arrow=='right' else np.insert(y2,0,np.zeros(self.__long))
    
    # desplazar onda 
    def __shiftWave(self,arrow,min_len,desplz,y2):
        return y2[self.__long:min_len+self.__long] if arrow=='right' else y2[0:min_len]
        
    # Devuelve la Correlación
    def getCorrelate(self):
        return [self.valor_correlacion,self.valores,self.__resp_correlation]
    
    def  getCorrFile(self):
        return self.y2_posc_active
    
    def getRespCorrelation(self):
        return self.__resp_correlation
    
    def clearvars(self):
        self.valor_correlacion = 0
        self.min_corr = 0
        self.valores = 0
        self.acum_long=0
        return
    
    def setLongMoving(self, valor):
        self.__long = valor
        return
    
    
    def __stretchAudio(self,yv,xv,sr):
        # Obtener la duración de los audios
        duration_a = librosa.get_duration(y=yv, sr=sr)
        duration_b = librosa.get_duration(y=xv, sr=sr)

        # Calcular la relación de estiramiento
        stretch_factor = float(duration_b / duration_a)

        # Aplicar el estiramiento
        audio_a_stretched = librosa.effects.time_stretch(y=xv, rate=stretch_factor)
        
        return audio_a_stretched
    
    def  __calcularLong(self,cant,a_y,a_x):
        self.__tam = int(cant * 0.16)
        # self.__long =int(self.__tam/(self.__longIterado/2)) # Un 16 % en la cantidad de interaciones    
        # Rellanar de ceros en la derecha e izquierda
        a_y = np.insert(a_y,0,np.zeros(self.__tam))
        a_y = np.insert(a_y,len(a_y),np.zeros(self.__tam))

        a_x = np.insert(a_x,0,np.zeros(self.__tam))
        a_x = np.insert(a_x,len(a_x),np.zeros(self.__tam))

        return a_y,a_x
    def __printGraphic(self, audio_l, sr_l,audio_r,sr_r,interado):
        import matplotlib.pyplot as plt
        plt.show()
        plt.figure(figsize=(16, 8))

        long_data = len(audio_l)
        n = np.arange(0,long_data)/sr_l
        # Presenta la imagen audio
        plt.subplot(1,2,1)
        plt.plot(n,audio_l)
        plt.ylabel("DB Audio")
        plt.xlabel("Duracción")


        long_data = len(audio_r)
        n = np.arange(0,long_data)/sr_r
        # Presenta la imagen audio
        plt.subplot(1,2,2)
        plt.plot(n,audio_r)
        plt.ylabel("DB Audio")
        plt.xlabel("Duracción" )
        plt.show()
        print(str(interado) + "-Correlate",self.valor_correlacion,"Desplz",str(self.acum_long),"Direc",self.direccion)
        return 

    def setToDraw(self,state):
        self.__toDraw = state
        return self

 
    



