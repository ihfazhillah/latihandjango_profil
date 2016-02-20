from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden
from .models import UserProfile
from .forms import UserProfileForm, PhoneFormSet, WebsiteFormSet

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


def create(request):
    
    if not request.user.is_authenticated():
      return HttpResponseForbidden("Anda tidak diperkenankan masuk")

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST)
        phone_form = PhoneFormSet(request.POST,
                                  prefix='phone')
        website_form = WebsiteFormSet(request.POST,
                                      prefix='web')

        if profile_form.is_valid() and phone_form.is_valid() and website_form.is_valid():
            profile = profile_form.save()
            phone = phone_form.save(commit=False)
            web = website_form.save(commit=False)

            for p in phone:
                p.user = profile
                p.save()

            for w in web:
                w.user = profile 
                w.save()

            return redirect(reverse('profil:index'))


    profile_form = UserProfileForm()
    phone_form = PhoneFormSet(prefix='phone')
    website_form = WebsiteFormSet(prefix='web')
    context = {'profile_form': profile_form,
                       'phone_form': phone_form,
                       'website_form': website_form}

    return render(request, 'profil/create.html', context)