#Feature scaling
from sklearn.preprocessing import StandardScaler
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
import pandas as pd
import numpy as np


# master module class
class API:
    def __init__(self):
       self.scaler = StandardScaler()
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

    def majority_element(self, num_list):
            idx, ctr = 0, 1
            
            for i in range(1, len(num_list)):
                if num_list[idx] == num_list[i]:
                    ctr += 1
                else:
                    ctr -= 1
                    if ctr == 0:
                        idx = i
                        ctr = 1
            
            return num_list[idx]
    def DetectMastitisTemp(self, request, animalid, data, tempreture_model, scaler):
        result_list = []
        save = data["save"]
        right_front_udder_quarter = data["right-front-udder-quarter"]
        left_front_udder_quarter = data["left-front-udder-quarter"]
        right_rear_udder_quarter = data["right-rear-udder-quarter"]
        left_rear_udder_quarter = data["left-rear-udder-quarter"]
        ##############3
        rt_right_front_udder_quarter = self.TempreturePrediction(tempreture_model, self.TempretureStandardization(right_front_udder_quarter,scaler))
        rt_right_front_udder_quarter ["temp"] = right_front_udder_quarter
        rt_left_front_udder_quarter = self.TempreturePrediction(tempreture_model, self.TempretureStandardization(left_front_udder_quarter, scaler))
        rt_left_front_udder_quarter["temp"] = left_front_udder_quarter
        rt_right_rear_udder_quarter = self.TempreturePrediction(tempreture_model, self.TempretureStandardization(right_rear_udder_quarter, scaler))
        rt_right_rear_udder_quarter["temp"] = right_rear_udder_quarter
        rt_left_rear_udder_quarter = self.TempreturePrediction(tempreture_model, self.TempretureStandardization(left_rear_udder_quarter, scaler))
        rt_left_rear_udder_quarter["temp"] = left_rear_udder_quarter
        ## add them to list 
        result_list.append(rt_right_front_udder_quarter["prediction"])
        result_list.append(rt_left_front_udder_quarter["prediction"])
        result_list.append(rt_right_rear_udder_quarter["prediction"])
        result_list.append(rt_left_rear_udder_quarter["prediction"])
        if save:
            # save test
            test = TempretureTest.objects.create(
                animal = Animal(pk=int(animalid)),
                right_front_udder_quarter = right_front_udder_quarter,
                left_front_udder_quarter = left_front_udder_quarter,
                right_rear_udder_quarter = right_rear_udder_quarter,
                left_rear_udder_quarter = left_rear_udder_quarter
            )
            test.save()
            # save results
            TempretureResult.objects.create(
                test = TempretureTest(pk=test.pk),
                right_front_udder_quarter = rt_right_front_udder_quarter["prediction"],
                left_front_udder_quarter = rt_left_front_udder_quarter["prediction"],
                right_rear_udder_quarter = rt_right_rear_udder_quarter["prediction"],
                left_rear_udder_quarter =  rt_left_rear_udder_quarter["prediction"]
            ).save()
        return {
            "right_front_udder_quarter": rt_right_front_udder_quarter,
            "left_front_udder_quarter": rt_left_front_udder_quarter,
            "right_rear_udder_quarter": rt_right_rear_udder_quarter,
            "left_rear_udder_quarter": rt_left_rear_udder_quarter,
            "prediction": self.majority_element(result_list)
        }

    def TempretureStandardization(self, temp, scaler):
        input_temp = (temp)
        #converting the input data into a numpyarray 
        input_udder_temp = np.asarray(input_temp)
        #reshaping the numpy array
        input_temp_reshaped = input_udder_temp.reshape(1,-1)
        input_temp_reshaped.shape
        #3yyyyyyy
        ##standardizing the data 
        input_temp_std = scaler.transform(input_temp_reshaped)
        # print(input_temp_std)
        #standardizing the data 
        return  input_temp_std 

    def TempreturePrediction(self, tempreture_model, input_temp_std):
        prediction =  tempreture_model.predict(input_temp_std)
        prediction_label = [np.argmax(prediction)]
        result = ""
        if(prediction_label[0]==2):
            result = "clinical Mastitis Detected"
        elif (prediction_label[0]==1):
            result = "subclinical mastitis Detected"
        else:
            result = "Healthy animal and no mastitis Detected"
        return {
            "prediction": prediction_label[0],
            "results": result
        }

    def DetectMastitisMilk(self, request, animalid, data, milk_model, sc_X):
        save = data["save"]
        conductivity_lf = data["conductivity_lf"]
        conductivity_lr = data["conductivity_lr"]
        conductivity_rf = data["conductivity_rf"]
        conductivity_rr = data["conductivity_rr"]
        conductivity_test = (conductivity_lf, conductivity_lr, conductivity_rf, conductivity_rr)
        ##############3
        rt_conductivity = self.MilkPrediction(milk_model, self.MilkStandardization(conductivity_test, sc_X))

        if save:
            # save test
            test = MilkTest.objects.create(
                animal = Animal(pk=int(animalid)),
                conductivity_lf = conductivity_lf,
                conductivity_lr = conductivity_lr,
                conductivity_rf = conductivity_rf,
                conductivity_rr = conductivity_rr,
            )
            test.save()
            # save results
            MilkResult.objects.create(
                test = MilkTest(pk=test.pk),
                results = rt_conductivity["prediction"]
            ).save()
        return {
            "results": rt_conductivity,
            "prediction": rt_conductivity["prediction"]
        }


    def MilkStandardization(self, input_data, sc_X):
        #converting the input data into a numpyarray 
        input_conductivity = np.asarray(input_data)
        #reshaping the numpy array
        input_cond_reshaped = input_conductivity.reshape(1,-1)
        input_cond_reshaped.shape
        #standardizing the data 
        return sc_X.transform(input_cond_reshaped)

    def MilkPrediction(self, milk_model, input_temp_std):
        prediction =  milk_model.predict(input_temp_std)
        prediction_label = [np.argmax(prediction)]
        result = ""
        if(prediction_label[0]==1):
            result = "clinical Mastitis Detected"
        elif (prediction_label[0]==2):
            result = "Healthy animal and no mastitis Detected"
        else:
            result = "subclinical mastitis Detected"
        return {
            "prediction": prediction_label[0],
            "results": result
        }