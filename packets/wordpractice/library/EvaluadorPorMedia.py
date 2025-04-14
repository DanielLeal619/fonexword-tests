
class EvaluadorMedia:
    def __init__(self, datos_recopilados, porcentaje, resultado):
        self.datos_recopilados = datos_recopilados
        self.porcentaje = porcentaje
        self.resultado = resultado

    def evaluar_por_media(self):
        condiciones = [
            {'condicion': self._es_excelente,'resultado': 'Excelente', 'porcentaje': 100},
            {'condicion': self._es_bueno,'resultado': 'Lo has hecho bien', 'porcentaje': 90},
            {'condicion': self._es_regular,'resultado': 'Intenta mejorar', 'porcentaje': 80},
            {'condicion': self._es_poco_bueno,'resultado': 'Vas por buen camino, puedes mejorar', 'porcentaje': 70},
            {'condicion': self._es_no_reconocido,'resultado': 'Su Frase no fue reconocida', 'porcentaje': 50}
        ]
        for condicion in condiciones:
            if condicion['condicion']():
                self.resultado = condicion['resultado']
                self.porcentaje = condicion['porcentaje']
                break
        return self.resultado,self.porcentaje

    def _es_excelente(self):
        return (self.datos_recopilados['media'] <= 7 and self.porcentaje <= 50)

    def _es_bueno(self):
        return (self.datos_recopilados['media'] <= 8 and self.porcentaje <= 50)

    def _es_regular(self):
        return (self.datos_recopilados['media'] <= 9 and self.porcentaje <= 50)

    def _es_poco_bueno(self):
        return (self.datos_recopilados['media'] <= 10 and self.porcentaje <= 50)

    def _es_no_reconocido(self):
        return (self.datos_recopilados['media'] <= 15 and self.porcentaje <= 50)