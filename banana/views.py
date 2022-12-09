from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import Image
from django.contrib.auth.decorators import login_required

# model packages
import pathlib
import cv2
import numpy as np

# Create your views here.


@login_required(login_url='/accounts/login')
def uploadImage(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

        return redirect('/predictor/image_upload')

    else:
        form = ImageUploadForm()
        images = Image.objects.filter(user=request.user)
    return render(request, "predictor/predict.html", {"form": form, "images": images})


def deleteImage(request, id):
    image = Image.objects.get(id=id)
    image.delete()
    form = ImageUploadForm()
    return redirect("/predictor/image_upload")


def processImages(images):
    pass


def getPredictions(request):
    import tensorflow as tf
    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

    model = tf.keras.models.load_model(
        BASE_DIR / 'predictor/new_banana_leaf_model.h5')

    images_dir = pathlib.Path(BASE_DIR / "media/images/")

    # fetch images
    images = Image.objects.all()

    if type(images) == list:
        images = images[::1]

    images_list = {"list": [], "urls": []}

    for image in images:
        images_list["list"].append(f"{BASE_DIR}{image.thumb.url}")
        images_list["urls"].append(image.thumb.url)
    # images_list = list(images_dir.glob("*"))

    images_object = {}
    for count in range(len(images_list["list"])):
        images_object[f"Image{count}"] = images_list["list"][count]

    X = []

    for label, image in images_object.items():
        img = cv2.imread(str(image))
        resized_img = cv2.resize(img, (256, 256))
        X.append(resized_img)

    X = np.array(X)

    predictions = model.predict(X)

    results = []

    for count in range(len(predictions)):
        url = images_list["urls"][count]
        if(np.argmax(predictions[count]) == 0):
            prediction = "Healthy"
        elif(np.argmax(predictions[count]) == 1):
            prediction = "Cordana"
        elif(np.argmax(predictions[count]) == 2):
            prediction = "Pestalotiopsis"
        else:
            prediction = "Sigatoka"

        results.append({"url": url, "prediction": prediction})

    return render(request, "predictor/results.html", {"results": results})

