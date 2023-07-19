from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger('watchtower-logger')

def home(request):
    return render(request, 'picaso/home.html')

@login_required(login_url='/', redirect_field_name=None)
def logout_view(request):
    if request.method != 'POST':
        logger.error(f"Request method is not POST for Logout View. Got {request.method}")
        return HttpResponse(status=405)
    logout(request)
    return redirect(request.META['HTTP_REFERER'])