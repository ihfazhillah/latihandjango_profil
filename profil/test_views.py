from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import UserProfile


class VIewTest(TestCase):


    def setUp(self):
        UserProfile.objects.create(firstname='first',
                                   lastname='last')
        UserProfile.objects.create(firstname='one',
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

