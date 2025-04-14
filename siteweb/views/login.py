from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from drf_spectacular.utils import extend_schema_view,extend_schema,OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from siteweb.jsonSchema.usuarioSerializer import *
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

@extend_schema_view(
    post=extend_schema(
        description='Ingresar al Sistema' ,
        responses=registerSerializer(many=False),
        request=loginAccessSerializer(),
        auth=False,
    )
)
@api_view(['POST'])
def login(request):
    _username = request.data['username']
    _password = request.data['password']
    # Autentificar al usuario
    user = get_object_or_404(User,username=_username)
    if not user.check_password(_password):
        return Response({'message_error':'La contraseña no es correcta!!!','message':'No puedo pudo ingresar al sistema por favor, verifique su contraseña'}, status=status.HTTP_400_BAD_REQUEST)

    token,created = Token.objects.get_or_create(user=user)

    usuario = registerSerializer(instance=user)
    return Response({'token':token.key,'user':usuario.data},status=status.HTTP_200_OK)



@extend_schema_view(
    put=extend_schema(
        description='Registro de Usuario',
        auth=None,
        responses=registerSerializer(many=True),
        request=registerSerializer(),
    )
)
@api_view(['PUT'])
def register(request):
    serializer = registerSerializer(data=request.data)
    tmp_password = request.data['password']
    _group = request.data['group']
    if serializer.is_valid():
        serializer.save()
        # Definir el grupo a que pertenece el usuario 
        grupo = createGroup(_group)
        user = User.objects.get(email=serializer.data['email'])
        dataCurrent(user,grupo,tmp_password)
        user.save()
        serializer = registerSerializer(instance=user)
        
        token = Token.objects.create(user=user)
        # token = "ALDD85165DSFPOPS897990"
        return Response({'token':token.key,'usuario':serializer.data},status=status.HTTP_201_CREATED)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def profile(request):
    return Response({})


def dataCurrent(user,grupo,passw):
    user.is_active = 1
    user.is_staff = 1
    user.is_superuser = 0
    user.deleted = False
    user.groups.add(grupo)
    user.set_password(passw)
    return

def createGroup(_nameGroup):
    if (Group.objects.filter(name=_nameGroup).exists()):
        grupo = Group.objects.get(name=_nameGroup)
    else:
        grupo = Group()
        grupo.name = _nameGroup
        grupo.save()
    return grupo