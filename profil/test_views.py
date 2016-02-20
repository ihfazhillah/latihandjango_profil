from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import UserProfile, Phone, Website


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

    def test_create_profil_with_get_is_bound_is_false(self):
        """
        checking empty form is using is_bound property from 
        gived context
        """
        self.login()
        response = self.client.get(reverse('profil:create'))
        context_is_bound = lambda x : response.context[x].is_bound
        self.assertFalse(context_is_bound('profile_form'))
        self.assertFalse(context_is_bound('phone_form'))
        self.assertFalse(context_is_bound('website_form'))

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
        self.assertEqual(len(phone), 1)
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
        self.assertEqual(len(phone), 1)
        self.assertEqual(len(web), 1)
        self.assertRedirects(response, reverse('profil:index'))

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
        self.assertEqual(len(phone), 0)
        self.assertEqual(len(web), 0)

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
        phone = Phone.objects.create(user=self.first,
                                     nomor='1234',
                                     tipe='p')
        website = Website.objects.create(user=self.first,
                                         url='http://this.url',
                                         tipe='p')
        Website.objects.create(user=self.second,
                               url='http://how.url',
                               tipe='p')
        self.login()
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
        phone = Phone.objects.create(user=self.second,
                                     nomor='1234',
                                     tipe='p')
        website = Website.objects.create(user=self.second,
                                         url='http://this.url',
                                         tipe='p')
        Website.objects.create(user=self.first,
                               url='http://how.url',
                               tipe='p')
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
