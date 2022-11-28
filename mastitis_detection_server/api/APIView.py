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
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
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

# Milk demo
#loading the dataset
# training_data = pd.read_csv('models/testingdata.csv')
# #
# training_data.head()
# #
# training_data.shape
# #
# training_data[training_data.isnull().any(axis=1)].count()
# #removing null values
# training_data = training_data.dropna()
# training_data.isnull().sum()
# #
# np.shape(training_data)

# missing_values = training_data.isnull().sum().sort_values(ascending = False)
# missing_values = missing_values[missing_values > 0]/training_data.shape[0] # normalize
# # print(f'{missing_values *100} %')
# #####
# training_data.dropna(inplace= True)
milk_model = pickle.load(open('models/milk_model.pkl', 'rb'))
###
df = pd.read_csv ('models/testingdata.csv')

#removing null values
df = df.dropna()
df.isnull().sum()
# # check for missing values
missing_values = df.isnull().sum().sort_values(ascending = False)
missing_values = missing_values[missing_values > 0]/df.shape[0] # normalize
# print(f'{missing_values *100} %')
# #
df.dropna(inplace= True)

data = df.drop(['animal.num', 'Consumed', 'Yield', 'Counsumed.times', 'Total.Duration',
       'DaysInMilk','lactation', 'month', 'age'], axis=1)
data.head()
# # check for missing values
# #droping null values
data=data.dropna()
#  #
scaled_df = StandardScaler().fit_transform(data)

# #view first five rows of scaled DataFrame
# print(scaled_df[:5])

# #spliting the data into target and features
kmeans_kwargs = {
"init": "random",
"n_init": 10,
"random_state": 1,
}

#create list to hold SSE values for each k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_df)
    sse.append(kmeans.inertia_)
##############################
#instantiate the k-means class, using optimal number of clusters
kmeans = KMeans(init="random", n_clusters=3, n_init=10, random_state=1)

#fit k-means algorithm to data
kmeans.fit(scaled_df)

#view cluster assignments for each observation
kmeans.labels_
#append cluster assingments to original DataFrame
data['cluster'] = kmeans.labels_

# #view updated DataFrame
# print(data)

X = data.iloc[:,:4].values
y = data.iloc[:,4].values
# print(X)
# ####
X_trainn, X_testt, y_trainn, y_testt =  train_test_split(X,y,test_size = 0.25, random_state= 0)
###
sc_X = StandardScaler()
sc_X.fit_transform(X_trainn)
sc_X.transform(X_testt)
#######
input_data = (5.43,4.99,5.32,4.53)
#converting the input data into a numpyarray 
input_conductivity = np.asarray(input_data)
#reshaping the numpy array
input_cond_reshaped = input_conductivity.reshape(1,-1)
input_cond_reshaped.shape

#standardizing the data 
input_cond_std = sc_X.transform(input_cond_reshaped)
# print(input_cond_std)
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
                    results = _api.DetectMastitisMilk(request, animalid, data, milk_model, sc_X)
                    return Response(results, status=200)
                else:
                    return Response({"message": "Invalid request method", "status": "failed"}, status=400)
            else:
                return Response({"message": "Invalid request method", "status": "failed"}, status=400)
        else:
            return Response({"message": "Invalid request method", "status": "failed"}, status=400)


