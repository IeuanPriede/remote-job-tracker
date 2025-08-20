from django.shortcuts import render
from django.http import JsonResponse


def health(_request):
    return JsonResponse({"status": "ok"})
