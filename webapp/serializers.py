from rest_framework import serializers 
from django.contrib.auth import get_user_model
from .models import Task , TaskProgress

User = get_user_model()

# CREATE SERIALIZER 
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('mobile_no', 'email')

    def validate(self, attrs):
        email = attrs.get('mobile_no')
        if not email:
            raise serializers.ValidationError("mobile_no")
        return attrs 
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task 
        fields = '__all__'

class TaskProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskProgress 
        fields = '__all__'