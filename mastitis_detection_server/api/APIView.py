from django.shortcuts import render
# Create your views here.
from .API import  API
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import json

_api = API()

# Create your views here.
class index(APIView):
    http_method_names = ['get']
    def get(self, request, format=None):
        return HttpResponse("<h2>Invalid Entry point </h2>")


# # Get all tax locations
class getAllAnimals(APIView):
    http_method_names = ['get']
    # Request
    def get(self, request):
        results = _api.getAllAnimals(request)
        return Response(results, status=200)
    def post(self, request, lang):
        return Response({"message": "Invalid request method", "status": "failed"}, status=400)

#############################################
class DetectMastitisTemp(APIView):
    http_method_names = ['post']
    def post(self, request, animalid):
        request_object = request.body.decode("utf-8")
        if request_object:
            data = json.loads(request_object)
            if data:
                if "right-front-udder-quarter" in data and "left-front-udder-quarter" in data and "right-rear-udder-quarter" in data and "left-rear-udder-quarter" in data:
                    results = _api.DetectMastitisTemp(request, animalid, data)
                    return Response(results, status=200)
                else:
                    return Response({"message": "Invalid request method", "status": "failed"}, status=400)
            else:
                return Response({"message": "Invalid request method", "status": "failed"}, status=400)
        else:
            return Response({"message": "Invalid request method", "status": "failed"}, status=400)


#############################################
class DetectMastitisMilk(APIView):
    http_method_names = ['post']
    def post(self, request, animalid):
        request_object = request.body.decode("utf-8")
        if request_object:
            data = json.loads(request_object)
            if data:
                if "conductivity_lf" in data and "conductivity_lr" in data and "conductivity_rf" in data and "conductivity_rr" in data:
                    results = _api.DetectMastitisTemp(request, animalid, data)
                    return Response(results, status=200)
                else:
                    return Response({"message": "Invalid request method", "status": "failed"}, status=400)
            else:
                return Response({"message": "Invalid request method", "status": "failed"}, status=400)
        else:
            return Response({"message": "Invalid request method", "status": "failed"}, status=400)


