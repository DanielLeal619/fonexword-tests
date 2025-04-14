class EvaluadorCorrelacion:
    def __init__(self, datos_recopilados,porcentaje):
        self.datos_recopilados = datos_recopilados
        self.resultado = None
        self.porcentaje = porcentaje

    def evaluar_por_correlacion(self):
        condiciones = [
            {'condicion': self._es_excelente,'resultado': 'Excelente', 'porcentaje': 100},
            {'condicion': self._es_bueno,'resultado': 'Lo has hecho bien', 'porcentaje': 90},
            {'condicion': self._es_regular,'resultado': 'Intenta mejorar', 'porcentaje': 80},
            {'condicion': self._es_poco_bueno,'resultado': 'Vas por buen camino, puedes mejorar', 'porcentaje': 70},
            {'condicion': self._es_no_reconocido,'resultado': 'Su Frase no fue reconocida', 'porcentaje': 50},
            {'condicion': self._es_ajuste,'resultado': 'Es posible que tenga ajustar tu micrófono', 'porcentaje': 40}
        ]
        for condicion in condiciones:
            if condicion['condicion']():
                self.resultado = condicion['resultado']
                self.porcentaje = condicion['porcentaje']
                break
        return self.resultado, self.porcentaje

    def _es_excelente(self):
        return (self.datos_recopilados['media'] <= 7 and 
                -0.07 > self.datos_recopilados['correlacion'] and 
                0.02 > self.datos_recopilados['probabilidad'] and 
                self.datos_recopilados['valida'] == 'yes')

    def _es_bueno(self):
        return (self.datos_recopilados['media'] <= 8 and 
                -0.06 > self.datos_recopilados['correlacion'] and 
                0.05 > self.datos_recopilados['probabilidad'] and 
                self.datos_recopilados['valida'] == 'yes')

    def _es_regular(self):
        return (self.datos_recopilados['media'] <= 9 and 
                -0.05 > self.datos_recopilados['correlacion'] and 
                0.05 > self.datos_recopilados['probabilidad'] and 
                self.datos_recopilados['valida'] == 'yes')

    def _es_poco_bueno(self):
        return (self.datos_recopilados['media'] <= 10 and 
                -0.01> self.datos_recopilados['correlacion'])

    def _es_no_reconocido(self):
        return (self.datos_recopilados['media'] <= 15 and 
                -0.005 > self.datos_recopilados['correlacion'])

    def _es_ajuste(self):
        return True