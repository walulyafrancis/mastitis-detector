import importlib
from pathlib import Path
import os
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import APIView

urlpatterns = [
    path('', APIView.index.as_view(), name="invalid-entry"),
    #g
    #path("<str:lang>/accounting/finacialyears/<int:yearid>/", accounting_view.getFinancialYearById.as_view(), name="get-accounting-finacialyears-units-by-id"),
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)