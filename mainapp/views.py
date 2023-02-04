from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serilaizers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt as JWT_
from diplom.settings import SIMPLE_JWT
# Create your views here.
#########################################



class ProfileView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        refresh_token_get = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
        jwt=JWT_.decode(
            refresh_token_get,
            SIMPLE_JWT['SIGNING_KEY'],
        algorithms = [SIMPLE_JWT['ALGORITHM']],
            )
        
        queryset=User.objects.get(id=jwt['user_id'])
        serilaizers= UserSerilizer(queryset)
        serilaizersProf=ProfileSerilizer(Profile.objects.get(user=queryset))

        return Response({'user':serilaizers.data,'profile':serilaizersProf.data}, status=status.HTTP_200_OK)



# Refresh TokenObtainPairView (add user)
class AuthorizateView(TokenObtainPairView):
    serializer_class = AuthorizateSerializer




class GetJk(APIView):
    serializer_class = JKSerilizer
 
    def get(self,request):
   

        queryset = self.get_queryset()
        serializer = JKSerilizer(queryset, many=True)

        return Response(serializer.data)

    def get_queryset(self):
        
        return JK.objects.filter()

class RegistrationView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    def post(self, request):
        

        # Паттерн создания сериализатора, валидации и сохранения - довольно
        # стандартный, и его можно часто увидеть в реальных проектах.
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        user = User.objects.filter(username=serializer.data['username'])
       
     
        
        if user.exists():
            return Response({"username":f"Пользователь уже существует в системе"},status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer.is_valid(raise_exception=True)
            new_user = User.objects.create_user(
                        username = request.data["username"],
                        first_name = request.data["first_name"],
                        last_name = request.data["last_name"],
                        password = request.data["password"],
                        surname = request.data["surname"],
                        email = request.data["email"],
                        )
            new_profile = Profile.objects.create(
                        user = new_user,
                        JK = JK.objects.get(id = request.data["nameResidentialComplex"]),
                        room_number = request.data["roomNumber"],

                        )
            refresh = RefreshToken.for_user(new_user)
            return Response({'user':serializer.data, 
                    'profile_user':ProfileSerilizer(new_profile).data,  
                    'is_superuser':new_user.is_superuser,   
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }, status=status.HTTP_201_CREATED)



class ElectronView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = QrCodeSerilizer
    def post(self, request):

        electron = QrCode.objects.filter(id_in_electron = request.data['id_in_electron'])
        if electron.exists():
            data = electron.first()
            data.qr = request.data['qr']
            data.save()
            return Response(QrCodeSerilizer(data).data,status=status.HTTP_200_OK)
        else:
            data = QrCode.objects.create(id_in_electron = request.data['id_in_electron'],qr = request.data['qr'])
            
            return Response(QrCodeSerilizer(data).data,status=status.HTTP_200_OK)

