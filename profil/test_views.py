from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import UserProfile, Phone, Website
from .forms import UserLoginForm


class VIewTest(TestCase):


    def make_data(self, firstname, lastname, 
                  phone_nomor='', phone_tipe='', 
                  phone_nomor2='', phone_tipe2='', 
                  web_url='', web_tipe='', 
                  web_url2='', web_tipe2=''):
        
        return {
                    'firstname':firstname,
                    'lastname': lastname,
                    'phone-TOTAL_FORMS':2,
                    'phone-INITIAL_FORMS':0,
                    'phone-MAX_NUM_FORMS':'',
                    'phone-0-nomor': phone_nomor,
                    'phone-0-tipe': phone_tipe,
                    'phone-1-nomor': phone_nomor2,
                    'phone-1-tipe': phone_tipe2,
                    'web-TOTAL_FORMS':2,
                    'web-INITIAL_FORMS':0,
                    'web-MAX_NUM_FORMS':'',
                    'web-0-url': web_url,
                    'web-0-tipe': web_tipe,
                    'web-1-url': web_url2,
                    'web-1-tipe': web_tipe2,
                    }
    
    def login(self):
        self.client.login(username='ihfazh',
                          password='ihfazhillah')

    def setUp(self):
        User.objects.create_superuser(username='ihfazh',
                                    email='',
                                    password='ihfazhillah')

        self.first = UserProfile.objects.create(firstname='first',
                                   lastname='last')
        self.second = UserProfile.objects.create(firstname='one',
                                   lastname='two')

        phone = Phone.objects.create(user=self.second,
                                     nomor='1234',
                                     tipe='p')
        website = Website.objects.create(user=self.second,
                                         url='http://this.url',
                                         tipe='p')
        website2 = Website.objects.create(user=self.first,
                               url='http://how.url',
                               tipe='p')
        phone2 = Phone.objects.create(user=self.first,
                                     nomor='1234',
                                     tipe='p')

###
# testing index view
###

    def test_index_view_return_200_status_code(self):
        response = self.client.get(reverse('profil:index'))
        self.assertEqual(response.status_code, 200)
        
    def test_index_using_right_template(self):
        response = self.client.get(reverse('profil:index'))
        self.assertTemplateUsed(response, 'profil/index.html')

    def test_index_return_profile_list(self):
        response = self.client.get(reverse('profil:index'))
        self.assertEqual(len(response.context['userprofile']), 2)

###
# testing detail view
###

    def test_detail_view_return_200_status_code(self):
        response = self.client.get(reverse('profil:detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_with_non_exist_profile_return_404(self):
        response = self.client.get(reverse('profil:detail', args=[10]))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_using_right_template(self):
        response = self.client.get(reverse('profil:detail', args=[1]))
        self.assertTemplateUsed(response, 'profil/detail.html')

    def test_detail_view_with_exist_data_return_context(self):
        response = self.client.get(reverse('profil:detail', args=[1]))
        self.assertEqual(response.context['userprofile'].__str__(), 'first')

###
#testing adding view
###
    def test_create_profil_with_get_anonymous_return_403(self):
        response = self.client.get(reverse('profil:create'))
        self.assertEqual(response.status_code, 403)

    def test_create_profil_with_get_return_200_with_correct_user(self):
        self.login()
        response = self.client.get(reverse('profil:create'))
        self.assertEqual(response.status_code, 200)

    def test_create_profil_with_get_using_right_template(self):
        self.login()
        response = self.client.get(reverse('profil:create'))
        self.assertTemplateUsed(response, 'profil/create.html')

    def test_create_get_return_empty_forms(self):
        """
        this test return None value.
        """
        self.login()
        response = self.client.get(reverse('profil:create'))
        self.assertEqual(len(
                         response.context['phone_form']),
                        1)
        self.assertEqual(
                         response.context['phone_form'][0]['nomor'].value(),
                         None)
        self.assertEqual(
                         response.context['phone_form'][0]['tipe'].value(),
                         None)
        self.assertEqual(
                         response.context['website_form'][0]['url'].value(),
                         None)
        self.assertEqual(
                         response.context['website_form'][0]['tipe'].value(),
                         None)

    def test_create_profil_with_post_and_just_profile_form(self):
        self.login()
        data = self.make_data(firstname="first", 
                              lastname="last")
        response = self.client.post(reverse('profil:create'), data=data)
        #get all profile
        profil = UserProfile.objects.all()
        self.assertEqual(len(profil), 3)
        self.assertRedirects(response, reverse('profil:index'))

    def test_create_profil_with_post_and_just_profile_form_and_phone(self):
        self.login()
        data = self.make_data(firstname="first", 
                              lastname="last",
                              phone_nomor='12345',
                              phone_tipe='p')
        response = self.client.post(reverse('profil:create'), data=data)
        #get all profile & phone
        profil = UserProfile.objects.all()
        phone = Phone.objects.all()
        self.assertEqual(len(profil), 3)
        self.assertEqual(len(phone), 3)
        self.assertRedirects(response, reverse('profil:index'))

    def test_create_profil_with_post_and__profile_phone_and_web(self):
        self.login()
        data = self.make_data(firstname="first", 
                              lastname="last",
                              phone_nomor='12345',
                              phone_tipe='p',
                              web_url='http://my.url',
                              web_tipe='p')
        response = self.client.post(reverse('profil:create'), data=data)
        #get all profile & phone & web
        profil = UserProfile.objects.all()
        phone = Phone.objects.all()
        web = Website.objects.all()
        self.assertEqual(len(profil), 3)
        self.assertEqual(len(phone), 3)
        self.assertEqual(len(web), 3)
        self.assertRedirects(response, reverse('profil:index'))

    def test_create_multiple_data(self):
        self.login()
        data_1 = self.make_data(firstname="onet",
                                lastname="last")
        self.client.post(reverse('profil:create'), data=data_1)
        data_2 = self.make_data(firstname="satu",
                                lastname="dua",
                                phone_nomor="1234",
                                phone_tipe="p")
        self.client.post(reverse('profil:create'), data=data_2)
        data_3 = self.make_data(firstname="two", 
                                lastname="one", 
                                phone_nomor="2345", 
                                phone_tipe="s",  
                                web_url="http://hehe.hoho", 
                                web_tipe="p")
        self.client.post(reverse("profil:create"), data=data_3)
        self.fail(UserProfile.objects.all())

    def test_create_profil_with_post_and_profile_phone_and_web_with_invalid(self):
        """
        field asalah tidak akan teredirect. Tetap di situ
        """
        self.login()
        data = self.make_data(firstname="first", 
                              lastname="last",
                              phone_nomor='ini salah',
                              phone_nomor2="1234",
                              phone_tipe='p',
                              phone_tipe2='s',
                              web_url='http://my.url',
                              web_url2='ini salah',
                              web_tipe2='s',
                              web_tipe='p')
        response = self.client.post(reverse('profil:create'), data=data)
        #get all profile & phone & web
        profil = UserProfile.objects.all()
        phone = Phone.objects.all()
        web = Website.objects.all()
        self.assertEqual(len(profil), 2)
        self.assertEqual(len(phone), 2)
        self.assertEqual(len(web), 2)

###
# Testing edit view
###

    def test_return_403_with_anonymous_user(self):
        response = self.client.get(reverse('profil:edit', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_return_200_with_authenticated_user(self):
        self.login()
        response = self.client.get(reverse('profil:edit', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_if_user_not_found_got_404_not_found(self):
        self.login()
        response = self.client.get(reverse('profil:edit', args=[10]))
        self.assertEqual(response.status_code, 404)

    def test_using_right_template(self):
        self.login()
        response = self.client.get(reverse('profil:edit', args=[1]))
        self.assertTemplateUsed(response, 'profil/edit.html')

    def test_context_1_contains_userform_with_initial(self):
        self.login()
        response = self.client.get(reverse('profil:edit', args=[1]))
        self.assertEqual(response.context['userform']['firstname'].value(), 
                         'first')
        self.assertEqual(response.context['userform']['lastname'].value(),
                         'last')

    def test_context_2_contains_userform_with_initial(self):
        self.login()
        response = self.client.get(reverse('profil:edit', args=[2]))
        self.assertEqual(response.context['userform']['firstname'].value(), 
                         'one')
        self.assertEqual(response.context['userform']['lastname'].value(),
                         'two')

    def test_context_1_contains_correct_forms(self):
        """
        Di test ini akan membuat objek yang punya relasi
        sama userprofile pertama, dan menampilkan initial data yang 
        benar disetiap formsetnya
        """
      
        response = self.client.get(reverse('profil:edit', args=[1]))
        self.assertEqual(response.context['userform']['firstname'].value(), 
                         'first')
        self.assertEqual(response.context['userform']['lastname'].value(),
                         'last')
        # testing phoneformset this initial
        self.assertEqual(response.context['phoneform'][0]['nomor'].value(),
                         '1234')
        self.assertEqual(response.context['phoneform'][1]['nomor'].value(),
                         None)
        #testing webform this initial data
        self.assertEqual(response.context['webform'][0]['url'].value(),
                         'http://this.url')
        self.assertEqual(response.context['webform'][1]['url'].value(),
                         None)

    def test_context_1_contains_correct_forms(self):
        """
        Di test ini akan membuat objek yang punya relasi
        sama userprofile pertama, dan menampilkan initial data yang 
        benar disetiap formsetnya
        """
        
        self.login()
        response = self.client.get(reverse('profil:edit', args=[2]))
        self.assertEqual(response.context['userform']['firstname'].value(), 
                         'one')
        self.assertEqual(response.context['userform']['lastname'].value(),
                         'two')
        # testing phoneformset this initial
        self.assertEqual(response.context['phoneform'][0]['nomor'].value(),
                         '1234')
        self.assertEqual(response.context['phoneform'][1]['nomor'].value(),
                         None)
        #testing webform this initial data
        self.assertEqual(response.context['webform'][0]['url'].value(),
                         'http://this.url')
        self.assertEqual(response.context['webform'][1]['url'].value(),
                         None)

    def test_edit_detail_profile_1_with_valid_data(self):
        data = self.make_data(firstname='ihfazh', lastname='amin', 
                              phone_nomor='112', phone_tipe='s', 
                              phone_nomor2='1234', phone_tipe2='p', 
                              web_url='http://iki.aku', web_tipe='s', 
                              web_url2='http://itu.kamu', web_tipe2='p')
        self.login()

        response = self.client.post(reverse('profil:edit', args=[1]),
                                    data=data)
        self.assertRedirects(response, reverse('profil:detail', args=[1]))
    
    def test_editing_detail_profile_1_firstname_lastname(self):
        data = self.make_data(firstname='ihfazh', lastname='amin', 
                              phone_nomor='112', phone_tipe='s', 
                              phone_nomor2='1234', phone_tipe2='p', 
                              web_url='http://iki.aku', web_tipe='s', 
                              web_url2='http://itu.kamu', web_tipe2='p')
        self.login()

        response = self.client.post(reverse('profil:edit', args=[1]),
                                    data=data)
        userprofile = UserProfile.objects.get(pk=1)
        self.assertEqual(userprofile.firstname, 'ihfazh')
        self.assertEqual(userprofile.lastname, 'amin')

    def test_editing_detail_profile_1_phone(self):
        data = self.make_data(firstname='ihfazh', lastname='amin', 
                              phone_nomor='112', phone_tipe='s', 
                              phone_nomor2='1234', phone_tipe2='p', 
                              web_url='http://iki.aku', web_tipe='s', 
                              web_url2='http://itu.kamu', web_tipe2='p')
        self.login()

        response = self.client.post(reverse('profil:edit', args=[1]),
                                    data=data)
        userprofile = UserProfile.objects.get(pk=1)
        self.assertEqual(len(userprofile.phone.all()), 2)
        phone1 = userprofile.phone.first()
        self.assertEqual(phone1.nomor, '112')
        phone2 = userprofile.phone.last()
        self.assertEqual(phone2.nomor, '1234')

    def test_editing_detail_profile_1_web(self):
        data = self.make_data(firstname='ihfazh', lastname='amin', 
                              phone_nomor='112', phone_tipe='s', 
                              phone_nomor2='1234', phone_tipe2='p', 
                              web_url='http://iki.aku', web_tipe='s', 
                              web_url2='http://itu.kamu', web_tipe2='p')
        self.login()

        response = self.client.post(reverse('profil:edit', args=[1]),
                                    data=data)
        userprofile = UserProfile.objects.get(pk=1)
        self.assertEqual(len(userprofile.website.all()), 2)
        web1 = userprofile.website.first()
        self.assertEqual(web1.url, 'http://iki.aku')

###
# testing login view
###
    def test_get_login_view_return_found_code(self):
        response = self.client.get(reverse('profil:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_using_right_template(self):
        response = self.client.get(reverse('profil:login'))
        self.assertTemplateUsed(response, 'profil/login.html')

    def test_login_view_context_with_login_form(self):
        response = self.client.get(reverse('profil:login'))
        self.assertTrue(response.context['login_form'])

    def test_login_view_post_with_valid_data(self):
        """
        user sudah di buat di setUp method
        """
        data = {'username': 'ihfazh', 'password': 'ihfazhillah'}
        response = self.client.post(reverse('profil:login'), 
                                    data=data)
        # print(help(response.context['user']))
        self.assertRedirects(response, reverse('profil:index'))
        #pastikan, bahwa user adalah ihfazh, bukan
        #anonymous
        response = self.client.get(reverse('profil:index'))
        self.assertEqual(response.context['user'].__str__(),
                         'ihfazh')

    def test_login_with_invalid_data(self):
        data = {'username':'ihfazh', 'password':''}
        response = self.client.post(reverse('profil:login'), 
                                    data=data)
        self.assertEqual(response.status_code, 200)
        # pastikan mendapatkan error bahwa password is required
        error = response.context['login_form']['password'].errors.as_data()[0]
        self.assertEqual(error.code, "required")
        response = self.client.get(reverse('profil:index'))
        self.assertNotEqual(response.context['user'].__str__(),
                         'ihfazh')
    def test_login_with_invalid_password(self):
        data = {'username':'ihfazh', 'password': 'ini_password_salah'}
        response = self.client.post(reverse('profil:login'),
                                    data=data)
        self.assertEqual(response.context['errors'], 
                  'Password atau Email yang anda masukkan salah')
        # Pastikan, bahwa form tetap ada. Dan data masih data
        # Sebelumnya
        self.assertEqual(response.context['login_form'].as_p(),
                         UserLoginForm(data).as_p())

###
# Testing logout view
###

    def test_logout_view(self):
        # Pastikan, user masih ihfazh setelah login
        self.login()
        response = self.client.get(reverse('profil:index'))
        self.assertEqual(response.context['user'].__str__(),
                         'ihfazh')
        #ketika logout, maka redirect ke index
        response = self.client.get(reverse('profil:logout'))
        self.assertRedirects(response, reverse('profil:index'))
        # dan user menjadi anonymous
        response = self.client.get(reverse('profil:index'))
        self.assertNotEqual(response.context['user'].__str__(),
                         'ihfazh')
