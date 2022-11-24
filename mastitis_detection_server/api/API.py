from tokenize import group
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Count
from django.db.models import Q
import datetime
from api.models import  *
from datetime import date

# master module class
class API:
    def __init__(self):
        pass

    def getAllAnimals(self, request):
        results = []
        animals = Animal.objects.all().order_by("-id")
        for animal in animals:
            birthdate = animal.date_of_birth
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            animal_name = animal.animal_name if animal.animal_name else "No name"
            animal_item = {
                "id": animal.pk,
                "animal_number": animal.animal_number,
                "age": age,
                "animal_name": animal_name,
                "date_of_birth": animal.date_of_birth,
                "created": animal.created
            }
            results.append(animal_item)
        return results


    def DetectMastitisTemp(self, request, animalid, data):
        results = []
        return data

    def DetectMastitisMilk(self, request, animalid, data):
        results = []
        return data