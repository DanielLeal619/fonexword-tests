from rest_framework import serializers
# from siteweb.models.User import User
from django.contrib.auth.models import User,Group

# Registro o Datos del Usuario
class registerSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','email','password','group')
        extra_kwargs = {'password':{'write_only':True}}

    def get_group(self, obj):
        group = obj.groups.first()  # Asumiendo que el usuario pertenece a un solo grupo
        return group.name if group else None        

# Ingreso al Sistema 
class loginAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password')
        extra_kwargs = {'username':{'write_only':True}}

