from animals.models import Animal
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from groups.models import Group
from traits.models import Trait


class AnimalTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.sex_default = "Não informado"

        cls.animal_1_data = {
            "name": "Doguinho",
            "age": 4,
            "weight": 23,
            "sex": "Não informado"
        }

        cls.animal_2_data = {
            "name": "Doguinha",
            "age": 4,
            "weight": 23
        }

        cls.animal_3_data = {
            "name": "Doguito",
            "age": 5,
            "weight": 21,
            "sex": "Escolha Inválida"
        }

        cls.group_1_data = {"name": "Cachorro", "scientific_name": "Catchorro"}

        cls.group_2_data = {"name": "Gatin", "scientific_name": "Gatoso"}

        cls.traits_1_data = {"name": "Peludo"}

        cls.traits_2_data = {"name": "Preto"}


        cls.group_1 = Group.objects.create(**cls.group_1_data)

        cls.group_2 = Group.objects.create(**cls.group_2_data)

        cls.traits_1 = Trait.objects.create(**cls.traits_1_data)

        cls.traits_2 = Trait.objects.create(**cls.traits_2_data)

        cls.animal_1 = Animal.objects.create(**cls.animal_1_data, group=cls.group_1)
        cls.animal_1.traits.add(cls.traits_1)
        cls.animal_1.traits.add(cls.traits_2)

        cls.animal_2 = Animal.objects.create(**cls.animal_2_data, group=cls.group_1)
        cls.animal_2.traits.add(cls.traits_1)
        cls.animal_2.traits.add(cls.traits_2)

        cls.animal_3 = Animal.objects.create(**cls.animal_3_data, group=cls.group_1)
        cls.animal_3.traits.add(cls.traits_1)
        cls.animal_3.traits.add(cls.traits_2)

    def test_animal_fields(self):
        print("Executando test_animal_fields")
        self.assertEqual(self.animal_1.name, self.animal_1_data["name"])
        self.assertEqual(self.animal_1.age, self.animal_1_data["age"])
        self.assertEqual(self.animal_1.weight, self.animal_1_data["weight"])
        self.assertEqual(
            self.animal_1.sex, self.animal_1_data["sex"]
        )
    
    def test_traits_fields(self):
        print("Executando test_traits_fields")
        self.assertEqual(self.traits_1.name, self.traits_1_data["name"])

    def test_group_fields(self):
        print("Executando test_group_fields")
        self.assertEqual(self.group_1.name, self.group_1_data["name"])
        self.assertEqual(self.group_1.scientific_name, self.group_1_data["scientific_name"])
    
    def test_sex_default_choice(self):
        print("Executando test_sex_default_choice")
        result_sex_default = self.animal_2.sex
        msg = f"Verifique se o valor padrão para sex é {self.sex_default}"

        self.assertEqual(result_sex_default, self.sex_default, msg)

    def test_sex_wrong_choice(self):
        print("Executando test_sex_wrong_choice")
        self.assertRaises(ValidationError, self.animal_3.full_clean)
    
    def test_animal_name_max_length(self):
        print("Executando test_animal_name_max_length")
        expected_max_length = 50
        result_max_length = self.animal_1._meta.get_field("name").max_length
        msg = "Vefique o max_length de `name`"

        self.assertEqual(result_max_length, expected_max_length, msg)
