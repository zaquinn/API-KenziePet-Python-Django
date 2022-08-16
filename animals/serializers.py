from groups.serializers import GroupSerializer
from rest_framework import serializers
from traits.serializers import TraitSerializer


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField()

    group = GroupSerializer()
    traits = TraitSerializer(many=True)
