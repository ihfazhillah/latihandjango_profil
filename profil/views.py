from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import (authenticate, login as auth_login, 
                                 logout as auth_logout)
from .models import UserProfile, Phone, Website
from .forms import (UserProfileForm, PhoneFormSet, 
                    WebsiteFormSet, UserLoginForm)

# Create your views here.
def login(request):
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, 
                                password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect(reverse('profil:index'))
            else:
                error = "Password atau Email yang anda masukkan salah"
                return render(request,
                                "profil/login.html",
                                {'errors':error,
                                'login_form': login_form})
        else:
            return render(request, "profil/login.html",
                          {'login_form': login_form})

    login_form = UserLoginForm()
    return render(request, 'profil/login.html',
                  {'login_form': login_form})

def logout(request):
    auth_logout(request)
    return redirect(reverse('profil:index'))

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
    phone_form = PhoneFormSet(prefix='phone',
                              queryset=Phone.objects.none())
    website_form = WebsiteFormSet(prefix='web',
                                  queryset=Website.objects.none())
    context = {'profile_form': profile_form,
                       'phone_form': phone_form,
                       'website_form': website_form}

    return render(request, 'profil/create.html', context)

def edit(request, pk):
    userprofile = get_object_or_404(UserProfile, pk=pk)

    if not request.user.is_authenticated():
        return HttpResponseForbidden("Kamu tidak diperkenankan")

    if request.method == 'POST':
        userform = UserProfileForm(initial=userprofile.__dict__, 
                                   data=request.POST, instance=userprofile)
        phoneform = PhoneFormSet(queryset=userprofile.phone.all(),
                                 data=request.POST, prefix='phone')
        webform = WebsiteFormSet(queryset=userprofile.website.all(),
                                 data=request.POST, prefix='web')

        if userform.is_valid() and phoneform.is_valid() and webform.is_valid():
            userform.save()
            phone = phoneform.save(commit=False)
            web = webform.save(commit=False)

            for p in userprofile.phone.all():
                p.delete()

            for p in phone :
                p.user = userprofile
                p.save()

            for w in userprofile.website.all():
                w.delete()

            for w in web:
                w.user = userprofile
                w.save()




        return redirect(reverse('profil:detail', args=[userprofile.pk]))

    userform = UserProfileForm(initial=userprofile.__dict__)
    phoneform = PhoneFormSet(queryset=userprofile.phone.all(),
                             prefix='phone')
    webform = WebsiteFormSet(queryset=userprofile.website.all(),
                             prefix='web')

    context = {'userform':userform,
                    'phoneform': phoneform,
                    'webform': webform }

    return render(request, 'profil/edit.html',
                context)

