from rest_framework import serializers

# Permite la subida de los archivos y verificar que funcione
class EvaluarPalabraSerializer(serializers.Serializer):
    file_target = serializers.FileField(required=True)
    file_test = serializers.FileField(required=True)


# Permite la subida de los archivos y verificar que funcione
class ResultadoDePalabraSerializer(serializers.Serializer):
    message = serializers.CharField()
    errores = serializers.CharField()
    test_data =serializers.JSONField()
    porcentaje = serializers.DecimalField(max_digits=9,decimal_places=2)
    resultado = serializers.CharField()
