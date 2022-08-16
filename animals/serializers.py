from rest_framework import serializers


class AnimalSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
