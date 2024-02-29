from rest_framework import serializers
from .models import Model

class ModelSerial(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


    def create(self, validated_data):
        return Model.objects.create(**validated_data)