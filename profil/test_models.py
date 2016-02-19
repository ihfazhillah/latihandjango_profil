from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import UserProfile, UserProfilePhone, UserProfileWebsite

class UserProfileModelTest(TestCase):


    def setUp(self):
        #membuat userprofile object baru
        self.user = UserProfile(firstname='first',
                    lastname='last')
        self.user.save()

    def test_can_save(self):
        user = UserProfile.objects.all()
        self.assertEqual(len(user), 1)

    def test_can_delete(self):
        self.user.delete()
        user = UserProfile.objects.all()
        self.assertEqual(len(user), 0)

    def test_str_definition_return_firstname(self):
        user = UserProfile.objects.get(pk=self.user.id)
        self.assertEqual(user.__str__(), 'first')


class UserProfilePhoneTest(TestCase):


    def setUp(self):
        self.user = UserProfile.objects.create(firstname='first',
                                               lastname='last')
        self.first_phone = UserProfilePhone.objects.create(user=self.user,
                                                           nomor='12345',
                                                           tipe = 'p')
    
    def test_retrieve_created_object(self):
        phone = UserProfilePhone.objects.all()
        self.assertEqual(len(phone), 1)

    def test_str_definition_return_alias_with_it_number(self):
        """str method harus mereturn 'nama (nomor)'"""
        phone = UserProfilePhone.objects.get(id=self.first_phone.id)
        self.assertEqual(phone.__str__(), '12345')

    def test_if_nomor_not_numeric(self):
        """
        kalau field nomor tidak diisi dengan data
        numeric, maka akan muncul validation error
        """
        phone = UserProfilePhone.objects.create(nomor='ini salah',
                                                tipe='s',
                                                user=self.user)
        self.assertRaises(ValidationError,  phone.full_clean)

    def test_tipe_must_be_one_in_s_or_p(self):
        phone = UserProfilePhone.objects.create(nomor='12345',
                                                tipe='g',
                                                user=self.user)
        self.assertRaises(ValidationError, phone.full_clean)


class UserProfileWebsiteTest(TestCase):


    def setUp(self):
        self.user = UserProfile.objects.create(firstname="first",
                                               lastname="last")
        self.website_first = UserProfileWebsite.objects.create(
                                                               user = self.user,
                                                               tipe='p',
                                                               url = 'http://thisurl.url')

    def test_first_website_created(self):
        web = UserProfileWebsite.objects.all()
        self.assertEqual(len(web), 1)

    

    def test_first_website_str_def(self):
        self.assertEqual(self.website_first.__str__(),
                         'http://thisurl.url')

    def test_tipe_must_be_one_in_s_or_p(self):
        web = UserProfileWebsite.objects.create(url='http://this.url',
                                                tipe='g',
                                                user=self.user)
        self.assertRaises(ValidationError, web.full_clean)
