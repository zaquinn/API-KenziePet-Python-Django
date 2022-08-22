from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Request, Response, status

from .models import Animal
from .serializers import AnimalSerializer, CustomExceptionError

# Create your views here.
#fazer diagrams com os relacionamentos

class AnimalView(APIView):
    def get(self, request: Request) -> Response:
        animals = Animal.objects.all()
        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        possible_errors = []
        sample_request_dict = {
            "name": "test",
            "age": 1,
            "weight": 1.11,
            "sex": "Não informado",
            "group": {"name": "test", "scientific_name": "testing"},
            "traits": [{"name": "test"}, {"name": "testing"}]
            }

        for key, value in sample_request_dict.items():
            if not request.data.get(key):
                possible_errors.append({f"{key}": ["This field is required."]})
        
        #retorna mensagem de erro se houver erros
        if len(possible_errors) > 0:
            return Response(
                {"detail": possible_errors}, status.HTTP_400_BAD_REQUEST)

        serializer = AnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class AnimalDetailView(APIView):
    def get(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)
        serializer = AnimalSerializer(animal)
        return Response(serializer.data)

    def patch(self, request: Request, animal_id: int) -> Response:
        possible_errors = []
        sample_request_dict = {
            "sex": "Não informado",
            "group": {"name": "test", "scientific_name": "testing"},
            "traits": [{"name": "test"}, {"name": "testing"}]
            }
        
        for key, value in sample_request_dict.items():
            if request.data.get(key):
                possible_errors.append({f"{key}": f"You can not update {key} property."})
        
        #retorna mensagem de erro se houver erros
        if len(possible_errors) > 0:
            return Response(
                {"detail": possible_errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        animal = get_object_or_404(Animal, id=animal_id)

        serializer = AnimalSerializer(animal, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def delete(self, request: Request, animal_id: int) -> Response:
        animal = get_object_or_404(Animal, id=animal_id)

        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

