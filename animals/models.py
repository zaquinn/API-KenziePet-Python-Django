from django.db import models

# Create your models here.

class Sex(models.TextChoices):
    MALE = "Macho"
    FEMALE = "Fêmea"
    OTHER = "Não informado"

class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=15, choices=Sex.choices, default=Sex.OTHER)

    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="animals_group")

    traits = models.ManyToManyField("traits.Trait", related_name="animals_traits")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        return f"<Animal {self.id} - {self.name}>"
