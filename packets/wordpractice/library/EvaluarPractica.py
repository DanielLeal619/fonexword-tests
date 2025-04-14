from .DynamicTimeWarpingClass import DynamicTimeWarpingClass
from .EvaluadorPorMedia import EvaluadorMedia
from .EvaluadorPorCorrelacion import EvaluadorCorrelacion
import os,sys
import numpy as np

class EvaluarPractica():
    DTWClass=None
    dat_recop ={}
    __resultado = ''
    __porcentaje = 40

    def test_practica(self,name_target,name_test):
        try:
            path_target =os.path.join('siteweb/static/audio/target/',name_target)
            path_test = os.path.join('siteweb/static/audio/test/',name_test)

            self.DTWClass =  DynamicTimeWarpingClass()

            self.__processTest(path_target,path_test)

            data_json = self.__resultadosEvaluadores()

            errores = None
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            data_json = {'distancia':0.00,'correlacion':0.00,'probabilidad':0.00,'condicion':0.00}
            errores = str(exc_type)+" "+str(exc_obj) + " "+ str(fname)+" "+str(exc_tb.tb_lineno) + " " + str(exc_tb.tb_lasti)
            self.__resultado = "Espere!!!"
            self.__porcentaje = 60
            
        return self.__resultado, self.__porcentaje, errores, data_json 
    
    def __processTest(self,path_target,path_test):
        self.DTWClass.setLongMoving(14) # Definición de espaciado en la iteraciones de Correlación
        self.DTWClass.setLongIterado(60)
        ## Evalua la correlación del audio 
        y,x,sr = self.DTWClass.SearchCorrelation(path_target,path_test)

        ## Aplica procesamiento Abcentral y luego DTW
        self.DTWClass.MfccDelete(y,x,sr,sr)

        ## Aplica y Busca la Semilitud de la dos ondas.
        self.DTWClass.reviewSound()

        # print(file_name[i] + ' Similitud: ' + str(DTWClass.getDistance()) + ' Correlación: ' + str(DTWClass.getCorrelate()[0]) + ' p_value:' + str(DTWClass.getCorrelate()[1]) + ' respC:' + str(DTWClass.getCorrelate()[2]))
        self.__saveResult()

    def __evaluarConCorrelacion(self):
        evaluador = EvaluadorCorrelacion(self.dat_recop,self.__porcentaje)
        self.__resultado, self.__porcentaje = evaluador.evaluar_por_correlacion()

    def __evaluarPorLaMedia(self):
        evaluador = EvaluadorMedia(self.dat_recop,self.__porcentaje,self.__resultado)
        self.__resultado, self.__porcentaje = evaluador.evaluar_por_media()
        
    def __returnJson(self):
        return {
            'media':self.dat_recop['media'],
            'std_dev':self.dat_recop['std_dev'],
            'correlacion':self.dat_recop['correlacion'],
        }
    
    def __returnJsonCompleted(self):
        return {
            'media':self.dat_recop['media'],
            'std_dev':self.dat_recop['std_dev'],
            'distancia':self.dat_recop['distancia'],
            'correlacion':self.dat_recop['correlacion'],
            'probabilidad':self.dat_recop['probabilidad'],
            'valida':self.dat_recop['valida']
        }
    
    def __resultadosEvaluadores(self): 
        self.__resultado = ''
        self.__porcentaje = 40

        self.__evaluarConCorrelacion()

        # self.__evaluarPorLaMedia()        
        
        return self.__returnJson()

    
    def __saveResult(self):
        ## Analizar los datos para la repuesta 
        self.dat_recop['media'] = self.DTWClass.getMedia()
        self.dat_recop['std_dev'] = self.DTWClass.getStdDev()
        self.dat_recop['distancia'] =self.DTWClass.getDistance()
        self.dat_recop['correlacion'] = float(self.DTWClass.getCorrelate()[0])
        self.dat_recop['probabilidad'] = float(self.DTWClass.getCorrelate()[1][0])
        self.dat_recop['valida'] = 'yes' if  (self.DTWClass.getRespCorrelation()==True) else 'not'
        

        


