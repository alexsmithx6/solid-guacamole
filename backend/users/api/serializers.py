from rest_framework import serializers
from users.models import account

class AcccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = ['app', 'uid']