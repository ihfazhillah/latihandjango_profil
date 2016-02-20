from django.forms import (ModelForm, 
                          modelformset_factory, 
                          BaseModelFormSet,
                          ValidationError,)
from .models import UserProfile, Phone, Website


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('firstname', 'lastname')

class BasePhoneFormSet(BaseModelFormSet):


    def clean(self):
        super(BasePhoneFormSet, self).clean()

        if any(self.errors):
            return

        nomors = []
        for form in self.forms:
            if form.cleaned_data:
                nomor = form.cleaned_data['nomor']

                if nomor :
                    if nomor in nomors:
                        raise ValidationError("Nomor tidak boleh terduplikasi",
                                          code='duplikat')
                    nomors.append(nomor)

class BaseWebsiteFormSet(BaseModelFormSet):


    def clean(self):
        super(BaseWebsiteFormSet, self).clean()

        if any(self.errors):
            return

        urls = []
        for form in self.forms:
            if form.cleaned_data:
                url = form.cleaned_data['url']

                if url:
                    if url in urls:
                        raise ValidationError("Url tidak boleh terduplikasi",
                                              code='duplikat')
                    urls.append(url)


PhoneFormSet = modelformset_factory(Phone,
                                          exclude=['user'],
                                          formset=BasePhoneFormSet)

WebsiteFormSet = modelformset_factory(
                                      Website,
                                      exclude=['user'],
                                      formset=BaseWebsiteFormSet)