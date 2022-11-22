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
# class getAllFinancialYears(APIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get']
#     # Request
#     def get(self, request, lang):
#         lang = DEFAULT_LANG if lang == None else lang 
#         results = _accounting.getAllFinancialYears(request, lang)
#         return Response(results, status=200)
#     def post(self, request, lang):
#         lang = DEFAULT_LANG if lang == None else lang
#         return Response({"message": "Invalid request method", "status": "failed"}, status=400)

# class getFinancialYearById(APIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get']
#     # Request
#     def get(self, request, lang, yearid):
#         lang = DEFAULT_LANG if lang == None else lang 
#         if not yearid:
#             return Response({"message": "Incomplete data request", "status": "failed"}, status=400)
#         # get module
#         results = _accounting.getFinancialYearById(request, lang, yearid)
#         if not (results == None):
#             # if there is results
#            return Response(results, status=200)
#         else:
#            return Response({"message": "No Year Found", "status": "failed"}, status=400) 

#     def post(self, request, lang, yearid):
#         lang = DEFAULT_LANG if lang == None else lang
#         return Response({"message": "Invalid request method", "status": "failed"}, status=400)


# class getCurrentFinancialYear(APIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get']
#     # Request
#     def get(self, request, lang):
#         lang = DEFAULT_LANG if lang == None else lang 
#         results = _accounting.getCurrentFinancialYear(request, lang)
#         if not (results == None):
#             # if there is results
#            return Response(results, status=200)
#         else:
#            return Response({"message": "No Year Found", "status": "failed"}, status=400) 

#     def post(self, request, lang, yearid):
#         lang = DEFAULT_LANG if lang == None else lang
#         return Response({"message": "Invalid request method", "status": "failed"}, status=400)


# class closeCurrentFinancialYear(APIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get']
#     # Request
#     def get(self, request, lang):
#         lang = DEFAULT_LANG if lang == None else lang 
#         if "narration" not in request.GET and "auto_create_new_fyear" not in request.GET:
#                return Response({"message": "Incomplete data request", "status": "failed"}, status=400)
#         elif not str(request.GET["auto_create_new_fyear"]):
#             return Response({"message": "Auto create new financial year is required", "status": "failed"}, status=400)
#         narration = request.GET["narration"]
#         results = _accounting.closeCurrentFinancialYear(request, lang, narration)
#         return results

#     def post(self, request, lang, yearid):
#         lang = DEFAULT_LANG if lang == None else lang
#         return Response({"message": "Invalid request method", "status": "failed"}, status=400)


# class CreateCurrentFinancialYear(APIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['post']
#     def post(self, request, lang):
#         lang = DEFAULT_LANG if lang == None else lang 
#         #print(request.POST)
#         if "start_date" in request.POST and "end_date" in request.POST and "narration" in request.POST:
#             if request.POST["start_date"] and not request.POST["end_date"]:
#                return Response({"message": "End date is required", "status": "failed"}, status=400)
#             elif request.POST["end_date"] and not request.POST["end_date"]:
#                 return Response({"message": "Start date is required", "status": "failed"}, status=400)
#             elif  request.POST["start_date"] and _helper.convertToDate(request.POST["start_date"]) < _helper.getCurrentDate():
#                 return Response({"message": "Start date already passed", "status": "failed"}, status=400)
#             elif request.POST["start_date"] and _helper.convertToDate(request.POST["end_date"]) < _helper.getCurrentDate():
#                 return Response({"message": "End date already passed", "status": "failed"}, status=400)
#             elif request.POST["start_date"] and request.POST["end_date"] and _helper.compareDates((_helper.convertToDate(request.POST["start_date"]), 1), (_helper.convertToDate(request.POST["end_date"]), 1)).get("is_expired"):
#                 return Response({"message": "End date already passed", "status": "failed"}, status=400)
#             elif  request.POST["start_date"] and request.POST["end_date"] and _helper.compareDates((_helper.convertToDate(request.POST["start_date"]), 1), (_helper.convertToDate(request.POST["end_date"]), 1)).get("days_left") < 365:
#                 return Response({"message": f'Finacial year of {_helper.compareDates((_helper.convertToDate(request.POST["start_date"]), 1), (_helper.convertToDate(request.POST["end_date"]), 1)).get("days_left")} is too short, it must be greater than 365 days', "status": "failed"}, status=400)
#             else:
#                 response = _accounting.createNewFinancialYear(request, lang, request.POST["narration"])
#                 return response
#         else:
#             return Response({
#             'message': "Incomplete data request",
#             'success': False
#             })



# class UpdateCurrentFinancialYear(APIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['post']
#     def post(self, request, lang):
#         lang = DEFAULT_LANG if lang == None else lang 
#         #print(request.POST)
#         if "start_date" in request.POST and "end_date" in request.POST and "narration" in request.POST:
#             if request.POST["start_date"] and not request.POST["end_date"]:
#                return Response({"message": "End date is required", "status": "failed"}, status=400)
#             elif request.POST["end_date"] and not request.POST["end_date"]:
#                 return Response({"message": "Start date is required", "status": "failed"}, status=400)
#             elif  request.POST["start_date"] and _helper.convertToDate(request.POST["start_date"]) < _helper.getCurrentDate():
#                 return Response({"message": "Start date already passed", "status": "failed"}, status=400)
#             elif request.POST["start_date"] and _helper.convertToDate(request.POST["end_date"]) < _helper.getCurrentDate():
#                 return Response({"message": "End date already passed", "status": "failed"}, status=400)
#             elif request.POST["start_date"] and request.POST["end_date"] and _helper.compareDates((_helper.convertToDate(request.POST["start_date"]), 1), (_helper.convertToDate(request.POST["end_date"]), 1)).get("is_expired"):
#                 return Response({"message": "End date already passed", "status": "failed"}, status=400)
#             elif  request.POST["start_date"] and request.POST["end_date"] and _helper.compareDates((_helper.convertToDate(request.POST["start_date"]), 1), (_helper.convertToDate(request.POST["end_date"]), 1)).get("days_left") < 365:
#                 return Response({"message": f'Finacial year of {_helper.compareDates((_helper.convertToDate(request.POST["start_date"]), 1), (_helper.convertToDate(request.POST["end_date"]), 1)).get("days_left")} is too short, it must be greater than 365 days', "status": "failed"}, status=400)
#             else:
#                 response = _accounting.createNewFinancialYear(request, lang, request.POST["narration"])
#                 return response
#         else:
#             return Response({
#             'message': "Incomplete data request",
#             'success': False
#             })



# class UpdatetFinancialYearById(APIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['post']
#     def post(self, request, lang):
#         lang = DEFAULT_LANG if lang == None else lang 
#         #print(request.POST)
#         if "start_date" in request.POST and "end_date" in request.POST and "narration" in request.POST:
#             if request.POST["start_date"] and not request.POST["end_date"]:
#                return Response({"message": "End date is required", "status": "failed"}, status=400)
#             elif request.POST["end_date"] and not request.POST["end_date"]:
#                 return Response({"message": "Start date is required", "status": "failed"}, status=400)
#             elif  request.POST["start_date"] and _helper.convertToDate(request.POST["start_date"]) < _helper.getCurrentDate():
#                 return Response({"message": "Start date already passed", "status": "failed"}, status=400)
#             elif request.POST["start_date"] and _helper.convertToDate(request.POST["end_date"]) < _helper.getCurrentDate():
#                 return Response({"message": "End date already passed", "status": "failed"}, status=400)
#             elif request.POST["start_date"] and request.POST["end_date"] and _helper.compareDates((_helper.convertToDate(request.POST["start_date"]), 1), (_helper.convertToDate(request.POST["end_date"]), 1)).get("is_expired"):
#                 return Response({"message": "End date already passed", "status": "failed"}, status=400)
#             elif  request.POST["start_date"] and request.POST["end_date"] and _helper.compareDates((_helper.convertToDate(request.POST["start_date"]), 1), (_helper.convertToDate(request.POST["end_date"]), 1)).get("days_left") < 365:
#                 return Response({"message": f'Finacial year of {_helper.compareDates((_helper.convertToDate(request.POST["start_date"]), 1), (_helper.convertToDate(request.POST["end_date"]), 1)).get("days_left")} is too short, it must be greater than 365 days', "status": "failed"}, status=400)
#             else:
#                 response = _accounting.createNewFinancialYear(request, lang, request.POST["narration"])
#                 return response
#         else:
#             return Response({
#             'message': "Incomplete data request",
#             'success': False
#             })


# class deleteFinancialYear(APIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get']
#     # Request
#     def get(self, request, lang, yearid):
#         lang = DEFAULT_LANG if lang == None else lang 
#         if not yearid:
#             return Response({"message": "Incomplete data request", "status": "failed"}, status=400)
#         # get module
#         results = _accounting.getFinancialYearById(request, lang, yearid)
#         if not (results == None):
#             # if there is results
#            return Response(results, status=200)
#         else:
#            return Response({"message": "No Year Found", "status": "failed"}, status=400) 

#     def post(self, request, lang, yearid):
#         lang = DEFAULT_LANG if lang == None else lang
#         return Response({"message": "Invalid request method", "status": "failed"}, status=400)
