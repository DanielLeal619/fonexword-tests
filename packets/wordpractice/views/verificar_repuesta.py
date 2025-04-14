from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema_view,extend_schema,OpenApiParameter
from packets.wordpractice.serializers.verificarRepuestaSerializer import *
from packets.wordpractice.library.EvaluarPractica import EvaluarPractica
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import AllowAny
import os
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.conf import settings
import librosa
import soundfile as sf 
import secrets
import string

class VerificarRepuestaView(APIView):
    serializer_class = EvaluarPalabraSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes  = [AllowAny]
    parser_classes = [MultiPartParser,FormParser]

    __file_target = ''
    __file_test = ''

    resultado=0
    porcentaje=0
    errores=0 
    data_json = None

    file_target_path=''
    file_test_path = ''

    name_file_target = ''
    name_file_test = ''

    @extend_schema(
        description='Carga de la  practica y evaluacion' ,
        responses=ResultadoDePalabraSerializer(many=True),
        request=EvaluarPalabraSerializer(),
        auth=False,
    )
    def post(self, request, format=None):
        # try:
        request.encoding = "utf-8"
        serializer = EvaluarPalabraSerializer(data=request.data)
        if serializer.is_valid():
            self.__file_target = request.data.get('file_target')
            self.__file_test = request.data.get('file_test')

            self.__nameFile()

            self.__assignPath()

            self.__ejecutarVerificacion()

            return Response({'message': 'Archivo fue procesado correctamente',
                                'resultado':self.resultado,
                                'porcentaje':self.porcentaje,
                                'errores':self.errores,
                                'test_data':self.data_json}, status=status.HTTP_200_OK)
        # except Exception as err:
        #    exc_type, exc_obj, exc_tb = sys.exc_info()
        #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #    return Response({'success':'error','message':str(exc_type) +" "+ str(exc_obj) + " "+ str(fname)+" "+str(exc_tb.tb_lineno)}, status=status.HTTP_200_OK)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def __generar_aleatorio(self):
        caracteres = string.ascii_letters + string.digits
        aleatorio = ''.join(secrets.choice(caracteres) for _ in range(8))
        return aleatorio
    
    def __ejecutarVerificacion(self):
        self.__saveFiles()

        eval_pract = EvaluarPractica()
        
        self.resultado, self.porcentaje,self.errores , self.data_json = eval_pract.test_practica(self.name_file_target,self.name_file_test)

        self.__removeFiles()

    def __save_file(self, file_path,file):
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                x, srx = librosa.load(file_path)
                x,index_space = librosa.effects.trim(y=x, frame_length=1024, top_db=40)
                sf.write(file_path,x,srx) 

    def __assignPath(self):
        self.file_target_path = os.path.join(settings.BASE_DIR,'siteweb\\static\\audio\\target',self.name_file_target)
        self.file_test_path = os.path.join(settings.BASE_DIR,'siteweb\\static\\audio\\test',self.name_file_test)

    def __nameFile(self):
        numero_aleatorio = self.__generar_aleatorio()

        self.name_file_target = "T" + numero_aleatorio+"_"+self.__file_target.name        
        self.name_file_test = "D" + numero_aleatorio+"_"+self.__file_test.name

    def __saveFiles(self):
        self.__save_file(self.file_target_path,self.__file_target)
        self.__save_file(self.file_test_path,self.__file_test)

    def __removeFiles(self):
        os.remove(self.file_test_path)
        os.remove(self.file_target_path)
        return





    
