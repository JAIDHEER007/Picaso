from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Image, JoinTable
from django.contrib.auth.models import User

from .forms import promtForm
from feature.models import Switch
from .image_gen import ImageGen

from django.conf import settings

from .awsS3 import AwsManager

import logging
logger = logging.getLogger('watchtower-logger')

# Create your views here.
@login_required(login_url='/', redirect_field_name=None)
def showGallery(request):
    logger.info("Show Gallery Request")
    if request.method == 'GET':
        imageObjects = None
        bypassOpenAISwitch = Switch.objects.get(feature_name = 'bypass_openai').toggle
        form = promtForm() if not bypassOpenAISwitch else None
        try:
            imageObjects = Image.objects.filter(jointable__user = User.objects.get(username = request.user.username))
            logger.info("Fetched Image Objects")
        except Exception as exp: 
            logger.error(f"Got Expcetion {exp}")
        context = {
            'form': form,
        'bypassOpenAISwitch': bypassOpenAISwitch,
            'imageObjects': imageObjects,
            'AWS_STORAGE_BUCKET_URL': settings.AWS_STORAGE_BUCKET_URL,
        }
        return render(request, 'gallery/showGallery.html', context)
    elif request.method == 'POST':
        form = promtForm(request.POST)
        if form.is_valid():
            logger.info("Form is valid")
            prompt = form.cleaned_data['prompt']

            img_uid = ImageGen(prompt).execute()

            # Creating the Image Record and JoinTable Record
            imgObj = Image(img_uid = img_uid, img_prompt = prompt)
            imgObj.save()
            logger.info("Saved image object")
            jtObj = JoinTable(img = imgObj, user = User.objects.get(username = request.user.username))
            jtObj.save()
            logger.info("Created a record in Join Table")

            return redirect('gallery:showImage', img_uid)


def showImage(request, img_uid):
    imageObject, userObject = None, None
    try:
        imageObject = Image.objects.get(img_uid = img_uid)
        userObject = JoinTable.objects.get(img = imageObject).user
    except Exception as exp:
        return HttpResponse(status = 404)
        logger.error(f"Caught an exception: {exp}")

    canDelete = request.user and request.user.is_authenticated and request.user.username == userObject.username
    if request.method == 'DELETE':
        logger.info("Delete Request")
        if not canDelete:
            return HttpResponse(status = 401)
        imageObject.delete()
        logger.info("Deleted Image Object")
        
        res = AwsManager.delete_file(img_uid + '.png')
        logger.info(f"Deleted Image from S3: {res}")
        
        if not res: return HttpResponse(status = 402)
        return HttpResponse(status = 204)

    
    context = {
        'imageObject': imageObject,
        'AWS_STORAGE_BUCKET_URL': settings.AWS_STORAGE_BUCKET_URL, 
        'disableDelete': 'disabled' if not canDelete else '',
    }
   
    return render(request, 'gallery/showImage.html', context)
    
