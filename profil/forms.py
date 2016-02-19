from django.forms import ModelForm, modelformset_factory
from .models import UserProfile, Phone


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('firstname', 'lastname')

PhoneFormSet = modelformset_factory(Phone,
                                          exclude=['user'])
