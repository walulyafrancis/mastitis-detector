from django.shortcuts import render
#Feature scaling
from sklearn.preprocessing import StandardScaler
# Create your views here.
from .API import  API
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import json
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

_api = API()

####################
#Data preprocessing
udder_temp = pd.read_csv('models/uddertemperature.csv')
udder_temp.head()
# Renaming some of the columns 
udder_temp = udder_temp.rename(columns={'Status':'target'})
#data cleaning
#removing null values
udder_temp = udder_temp.dropna()
udder_temp.isnull().sum()
#replace the strings in target column with corresponding numbers
udder_temp =udder_temp.replace({'clinical': 2, 'subclinical': 1, 'Healthy': 0})
udder_temp.head()
# checking the distribution of the target variable
udder_temp['target'].value_counts()
X = udder_temp.drop(columns='target',axis = 1)
y = udder_temp['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,random_state=2)

tempreture_model = pickle.load(open('models/NNuddertemperature_model.pkl', 'rb'))
# load models
scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)
X_test_std = scaler.fit_transform(X_test)
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
        data = request.data
        if data:
            if data:
                if "save" in data and "right-front-udder-quarter" in data and "left-front-udder-quarter" in data and "right-rear-udder-quarter" in data and "left-rear-udder-quarter" in data:
                    results = _api.DetectMastitisTemp(request, animalid, data, tempreture_model, scaler)
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
        data = request.data
        if data:
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


