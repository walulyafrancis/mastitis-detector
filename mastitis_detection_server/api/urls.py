import importlib
from pathlib import Path
import os
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import APIView

urlpatterns = [
    path('', APIView.index.as_view(), name="invalid-entry"),
    ################################
    path('detect/mastitis/tempreture/<int:animalid>/', APIView.DetectMastitisTemp.as_view(), name="detect-tempreture"),
    path('detect/mastitis/milk/<int:animalid>/', APIView.DetectMastitisMilk.as_view(), name="detect-milk"),
    ####################################3
    path('animals/all/', APIView.getAllAnimals.as_view(), name="get-all-animals"),
    ##################3333
    path('tempreture/save/', APIView.index.as_view(), name="save-tempreture"),
    path('milk/save/', APIView.index.as_view(), name="save-milk"),
    #g
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)