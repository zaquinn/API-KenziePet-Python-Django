import math

from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import serializers
from traits.models import Trait
from traits.serializers import TraitSerializer

from .models import Animal, Sex


class CustomExceptionError(Exception):
    ...

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Sex.choices, default=Sex.OTHER)

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    age_in_human_years = serializers.SerializerMethodField(read_only=True)

    def get_age_in_human_years(self, obj: Animal) -> str:
        return str(16 * math.log(obj.age) + 31)

    def create(self, validated_data: dict) -> Animal:
        group_data = validated_data.pop("group")

        traits_data = validated_data.pop("traits")

        group_obj = Group.objects.get_or_create(**group_data)

        animal_obj = Animal.objects.create(**validated_data, group=group_obj[0])

        for traits_dict in traits_data:
            traits_obj, _ = Trait.objects.get_or_create(**traits_dict)
            animal_obj.traits.add(traits_obj)

        return animal_obj

class AnimalDetailSerializer(serializers.Serializer): 
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Sex.choices, default=Sex.OTHER)

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    age_in_human_years = serializers.SerializerMethodField(read_only=True)

    def get_age_in_human_years(self, obj: Animal) -> str:
        return str(16 * math.log(obj.age) + 31)

    def update(self, instance: Animal, validated_data: dict) -> Animal:
        for key, value in validated_data.items():
            if key in ["traits, group, sex"]:
                raise CustomExceptionError(
                    {f"{key}": f"You can not update {key} property."}
                )
            setattr(instance, key, value)

            instance.save()

            return instance
