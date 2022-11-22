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

# master module class
class API:
    def __init__(self):
        pass