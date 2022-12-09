from django.urls import path
from . import views

app_name = "predictor"

urlpatterns = [
    path("image_upload/", views.uploadImage, name="image_upload"),
    path("get_predictions/", views.getPredictions, name="get_predictions"),
    path("delete_image/<int:id>", views.deleteImage, name="delete_image")
]
