import numpy as np

class GainPPPClass():
    def igualPtoP(self,audio_a, audio_b):
        """
            PPP : Son valores pico a pico del audio 
        """

        # Calcula el Pico más alto del audio A
        ppp_a = np.max(audio_a)
        ppp_b = np.max(audio_b)


        # Verifica si los RMS son homogéneos
        if (ppp_a == ppp_b):
            return audio_b # No cambiar nada si los RMS son iguales

        # Calcula el factor de ganancia para igualar el RMS
        ## if (ppp_a>ppp_b):
        ##    gain = np.float32(ppp_b / ppp_a)
        ##else:
        gain = np.float32(ppp_a / ppp_b)

        # Se ajusta el nivel del volumen con respecto audio_a
        return audio_b * gain