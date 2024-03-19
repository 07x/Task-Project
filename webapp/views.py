from django.shortcuts import render

# EXTERNAL IMPORTS 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import IsAuthenticated


# INTERNAL IMPORTS 
from django.contrib.auth import get_user_model 
from django.contrib.auth import authenticate
from .models import CustomUserModel , TaskProgress
from .serializers import UserRegistrationSerializer , TaskSerializer , TaskProgressSerializer


User = get_user_model()

# LOGIN API 
class LoginAPI(APIView):
    # POST 
    def post(self,request):
        data = request.data 

        # AUTHTICATE       
        user = authenticate(request,email=data.get('email'),password=data.get('password'))
        if user:
            refresh = RefreshToken.for_user(user)

            serializer = UserRegistrationSerializer(user)         
            response = {
                'message'       : 'login succesfully',
                'response_code' : 200,
                'data'          : serializer.data,
                'refresh'       : str(refresh),
                'access'        : str(refresh.access_token),
            }
            return Response(response,status=status.HTTP_200_OK)

# REGISTRATION API 
class RegistrationAPI(APIView):

    # POST 
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']  # Corrected line
            password = serializer.validated_data['password']
            mobile_no = serializer.validated_data['mobile_no']
            user = User.objects.create_user(email      = email,
                                            password   = password 
                                            ,mobile_no = mobile_no)
            serializer = UserRegistrationSerializer(user)
            response = {
                'message'       : 'user registered successfuly',
                'response_code' : 200,
                'data'          : serializer.data
            }
            return  Response(response,status=status.HTTP_200_OK)
        else:
            response = {
                'message'       : serializer.errors,
                'response_code' : 400,
            }
            return  Response(response,status=status.HTTP_200_OK)
        
# CREATE &  ASSSIGN TASK  
class TaskCreation(APIView):
    
    # POST 
    #AUTH & PERMISSION CLASSES 
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated] 
    def post(self,request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # CREATE TASK INSTANCE
            serializer.validated_data['creator'] = request.user
            task = serializer.save()
            response = {
                'message'       : 'Task created successfully', 
                'response_code' : 200,
                'data'          : serializer.data
            }
            return Response(response,status=status.HTTP_200_OK)
        else:
            response = {
                'message'       : serializer.errors, 
                'response_code' : 400
            }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        

# TASK REPORT BASED ON USER 
class TaskPerformance(APIView):

    # POST
    #AUTH & PERMISSION CLASSES 
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated] 
    def post(self,request):

        # GET DATA FROM TASK 
        total_assigned_task = TaskProgress.objects.filter(assignee=request.user)
        completed_task_count  = total_assigned_task.filter(is_completed=True).count()
        percentage_val        = round((completed_task_count/total_assigned_task.count())*100,2)

        data = {
        'percentage'     : percentage_val, 
        'completed_task' : completed_task_count, 
        'assigned_task'  : total_assigned_task.count(),
        }

        response = {
            'message'       : 'get report succesfully',
            'response_code' : 200,
            'performance'   : data, 
        }
        return Response(response,status=status.HTTP_200_OK)