from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

class Inventario(viewsets.ViewSet):

    def list(self, request):
        return Response("hola")
