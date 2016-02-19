from django.test import TestCase
from .forms import UserProfileForm


class UserProfileFormTest(TestCase):

    def make_form(self, firstname, lastname):
        return UserProfileForm({'firstname': firstname,
                               'lastname': lastname})

    def test_with_valid_data(self):
        form = self.make_form('first', 'last')
        self.assertTrue(form.is_valid())

    def test_with_missing_firstname(self):
        form = self.make_form('', 'last')
        self.assertFalse(form.is_valid())
        #get error code
        error = form['firstname'].errors.as_data()[0]
        self.assertEqual(error.code, 'required')

    def test_with_missing_lastname(self):
        form = self.make_form('firstname', '')
        self.assertFalse(form.is_valid())
        #get error code
        error = form['lastname'].errors.as_data()[0]
        self.assertEqual(error.code, 'required')