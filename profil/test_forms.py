from django.test import TestCase
from .forms import (UserProfileForm, 
                    PhoneFormSet, 
                    WebsiteFormSet, 
                    UserLoginForm)


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

class UserProfilePhoneFormSet(TestCase):

    def form_data(self, 
                  nomor,
                  tipe,
                  nomor2='',
                  tipe2=''):
        return PhoneFormSet({
                            'form-TOTAL_FORMS':2,
                            'form-INITIAL_FORMS':0,
                            'form-MAX_NUM_FORMS':'',
                            'form-0-nomor': nomor,
                            'form-0-tipe': tipe,
                            'form-1-nomor': nomor2,
                            'form-1-tipe': tipe2,
                            })
    
    def test_with_valid_data(self):
        form = self.form_data("12345", 'p')
        self.assertTrue(form.is_valid())

    def test_with_non_numeric_nomor(self):
        """
        harusnya false ketika validasi
        """
        form = self.form_data("ini non numeric", 'p')
        self.assertFalse(form.is_valid())
        #get first form, and get nomor field.
        #then get it data with .as_data() method
        error = form[0]['nomor'].errors.as_data()[0]
        self.assertEqual(error.code, 'invalid input')

    def test_with_two_data(self):
        """
        isi dengan valid
        """
        form = self.form_data(nomor="12345", tipe="p", 
                              nomor2="31234", tipe2="s")
        self.assertTrue(form.is_valid())

    def test_with_two_data_second_nomor_is_invalid(self):
        """
        because the invalid formset is indexed by 1 (form number two)
        so, the error form is in form[1]
        """
        form = self.form_data(nomor="12345", tipe="p", 
                              nomor2="ini data salah", tipe2="s")
        self.assertFalse(form.is_valid())
        error = form[1]['nomor'].errors.as_data()[0]
        self.assertEqual(error.code, 'invalid input')

    def test_with_two_data_first_tipe_is_none(self):
        """
        Because the invalid data is in formset
        indexed by 0, so the error form is in 
        form[0]
        """
        form = self.form_data(nomor="12345", tipe="", 
                              nomor2="31234", tipe2="s")
        self.assertFalse(form.is_valid())
        error = form[0]['tipe'].errors.as_data()[0]
        self.assertEqual(error.code, 'required')

    def test_with_same_input(self):
        """
        Formset tidakboleh double data nomornya
        Ini menggunakan validasi via BaseModelFormSet,
        maka tidak bisa menggunakan errors properti secara langsung
        harus dengan form.non_form_errors barus bisa dapat pesan 
        error. Tapi, valid == False
        TODO: Pindahkan validasi sebisa mungkin ke models.py
        """
        form = self.form_data(nomor='12345', tipe='p', 
                              nomor2='12345', tipe2='s')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_form_errors().as_data()[0].code, 'duplikat')

class WebsiteFormSetTest(TestCase):


    def make_data(self, url, tipe, url2='', tipe2=''):
         return WebsiteFormSet({
                            'form-TOTAL_FORMS':2,
                            'form-INITIAL_FORMS':0,
                            'form-MAX_NUM_FORMS':'',
                            'form-0-url': url,
                            'form-0-tipe': tipe,
                            'form-1-url': url2,
                            'form-1-tipe': tipe2,
                            })
    def test_valid_data(self):
        form = self.make_data(url='http://this.url', tipe='p')
        self.assertTrue(form.is_valid())

    def test_invalid_url(self):
        """
        error form is in form[0]
        """
        form = self.make_data(url='invalidurl', tipe='p')
        self.assertFalse(form.is_valid())
        error = form[0]['url'].errors.as_data()[0]
        self.assertEqual(error.code, 'invalid')
    
    def test_with_invalid_twice(self):
        """
        the first url invalid
        the second form missing tipe 
        """
        form = self.make_data(url='invalidurl', tipe='p', 
                              url2='http://this.valid' , tipe2='')
        self.assertFalse(form.is_valid())
        url_first_error = form[0]['url'].errors.as_data()[0]
        tipe_second_error = form[1]['tipe'].errors.as_data()[0]
        self.assertEqual(url_first_error.code, 'invalid')
        self.assertEqual(tipe_second_error.code, 'required')

    def test_with_same_input(self):
        """
        Formset tidakboleh double data nomornya
        Ini menggunakan validasi via BaseModelFormSet,
        maka tidak bisa menggunakan errors properti secara langsung
        harus dengan form.non_form_errors barus bisa dapat pesan 
        error. Tapi, valid == False
        TODO: Pindahkan validasi sebisa mungkin ke models.py
        """
        form = self.make_data(url='http://url.jy', tipe='p', 
                              url2='http://url.jy', tipe2='s')
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_form_errors().as_data()[0].code, 'duplikat')

class UserLoginFormTest(TestCase):

        def make_data(self, username, password):
            return UserLoginForm({'username': username, 
                                 'password': password})

        def test_valid_data(self):
            form = self.make_data('ihfazh', 
                                  'cakepbanget')
            self.assertTrue(form.is_valid())

        def test_missing_username(self):
            form = self.make_data('', 'cakepbanget')
            self.assertFalse(form.is_valid())
            error = form['username'].errors.as_data()[0]
            self.assertEqual(error.code, 'required')

        def test_missing_password(self):
            form = self.make_data('ihfazh', '')
            self.assertFalse(form.is_valid())
            error = form['password'].errors.as_data()[0]
            self.assertEqual(error.code, 'required')