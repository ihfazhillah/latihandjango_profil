from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import UserProfile
# Create your views here.

def index(request):
    userprofile = UserProfile.objects.all()
    context = {'userprofile': userprofile}
    return render(request, 'profil/index.html',
                  context)

def detail(request, pk):
    userprofile = get_object_or_404(UserProfile, pk=pk)
    context = {'userprofile': userprofile}
    return render(request,
                  'profil/detail.html',
                  context)