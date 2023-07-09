from django.urls import path
from . import views

urlpatterns = [
    path("test/", views.test),
    path("addFavorite/", views.addFavorite),
    path("addConsumption/", views.addConsumption),
    path("addFood/", views.addFood),
    path("api/food/barcode/<str:barcode>", views.getFoodByBarcode),
    path("api/food/favorite/<int:favoriteCode>", views.getFoodByFavoriteCode),
    path("api/food/id/<int:id>", views.getFoodById),
    path("api/add/", views.add),
    path("api/time/", views.getTime),
    path("api/consumption/id/<int:id>", views.getConsumptionById),
    path("api/consumption/datetime/", views.getConsumptionByTime),
]