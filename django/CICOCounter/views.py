import time

from CICOCounter.models import *

from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework import status

import json


SUCCESS_RESPONSE = HttpResponse("Success.")
BAD_REQUEST = Response("Bad request.", status=status.HTTP_400_BAD_REQUEST)


def test(req):
    FOOD = Food()
    FOOD.barcode = "845785"
    FOOD.name = "Vegemite"
    FOOD.kilojoulesPerGram = 798/100
    FOOD.gramsOfProteinPerGram = 25.4/100
    FOOD.gramsOfFatPerGram = 0
    FOOD.gramsOfSaturatedFatPerGram = 0
    FOOD.gramsOfCarbohydratePerGram = 19.9/100
    FOOD.gramsOfSugarPerGram = 2.2/100
    FOOD.gramsOfSodiumPerGram = 3.450/100

    CONSUMPTION = Consumption()
    CONSUMPTION.time = 1690077270.0
    CONSUMPTION.foodId = FOOD
    CONSUMPTION.weightGrams = 499


    for obj in [FOOD, CONSUMPTION]:
        obj.save()

@api_view(["GET"])
def addFavorite(request: Request):
    json = '[{"model": "CICOCounter.favorite", "fields": {"id": 640, "foodId": 10}}, {"model": "CICOCounter.favorite", "fields": {"id": 141, "foodId": 11}}]'
    for food in serializers.deserialize("json", json):
        food.object.save()
    return SUCCESS_RESPONSE


@api_view(["GET"])
def addConsumption(request: Request):
    json = '[{"model": "CICOCounter.consumption", "fields": {"foodId": 1, "weightGrams": 20}}]'
    for food in serializers.deserialize("json", json):
        food.object.save()
    return SUCCESS_RESPONSE

@api_view(["GET"])
def addFood(request: Request):
    json = '[{"model": "CICOCounter.food", "fields": {"kilojoulesPerGram": 20}}]'
    for food in serializers.deserialize("json", json):
        food.object.save()
    return SUCCESS_RESPONSE

@api_view(["GET"])
def printFood(request: Request):
    food = Food.objects.all()
    data = serializers.serialize("json", food)
    print(data)
    return HttpResponse(data)


@api_view(["GET"])
def getFoodByBarcode(request: Request, barcode: str):
    food = get_object_or_404(Food, barcode=barcode)
    data = serializers.serialize("json", [food])
    return HttpResponse(data)


@api_view(["GET"])
def getFoodByFavoriteCode(request: Request, favoriteCode: int):
    favorite = get_object_or_404(Favorite, id=favoriteCode)
    data = serializers.serialize("json", [favorite.foodId])
    return HttpResponse(data)


@api_view(["GET"])
def getFoodById(request: Request, id: int):
    food = get_object_or_404(Food, id=id)
    data = serializers.serialize("json", [food])
    return HttpResponse(data)


@api_view(["GET"])
def getConsumptionById(request: Request, id: int):
    consumption = get_object_or_404(Consumption, id=id)
    data = serializers.serialize("json", [consumption])
    return HttpResponse(data)


@api_view(["GET"])
def getFavoriteById(request: Request, id: int):
    favorite = get_object_or_404(Favorite, id=id)
    data = serializers.serialize("json", [favorite])
    return HttpResponse(data)


@api_view(["GET"])
def getTime(request: Request):
    data = f'{{"time": {time.time()}}}'
    return HttpResponse(data)


@api_view(["GET"])
def getConsumptionByTime(request: Request):
    # Obtain URL params and set 
    after = request.GET.get("after", None)
    before = request.GET.get("before", None)

    # Parse times and fill in defaults if they are not specified
    try:
        if after is not None:
            after = float(after)
        else:
            after = 0
        if before is not None:
            before = float(before)
        else:
            before = time.time()

    except ValueError:
        return Response("Invalid time format. Use UNIX timestamp.", status=status.HTTP_400_BAD_REQUEST)

    # Query DB
    print("==================================")
    print(after)
    print(before)
    consumptions = Consumption.objects.filter(time__range=(after, before))
    if len(consumptions) == 0:
        raise Http404
    response = serializers.serialize("json", consumptions)
    return HttpResponse(response)


@api_view(["POST"])
def add(request: Request):
    print(request.body)
    for obj in serializers.deserialize("json", request.body):
        obj.object.save()
    return SUCCESS_RESPONSE
