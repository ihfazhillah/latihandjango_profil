from django.forms import ModelForm, modelformset_factory
from .models import UserProfile, Phone, Website


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('firstname', 'lastname')

PhoneFormSet = modelformset_factory(Phone,
                                          exclude=['user'])

WebsiteFormSet = modelformset_factory(
                                      Website,
                                      exclude=['user'])