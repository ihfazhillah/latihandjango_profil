import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.auth.models import User 
from django.core.urlresolvers import reverse




class FunctionalTestingProfilApp(LiveServerTestCase):


    def get_abs_url(self, url_name):
        """
        url helper, untuk mendapatkan absolute url 
        menggunakan live server url milik django
        """
        return "{}{}".format(self.live_server_url, reverse(url_name))

    def setUp(self):
        # Membuat superUser
        User.objects.create_superuser(username='ihfazh',
                                      email='',
                                      password='ihfazhillah')
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        super(FunctionalTestingProfilApp, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(FunctionalTestingProfilApp, self).tearDown()

    def test_my_test(self):
        # Saya pergi ke profil app url
        self.driver.get(self.get_abs_url('profil:index'))
        # untuk memastikan bahwa aplikasi yang saya 
        # masuki benar, maka saya melihat ke url
        # dan saya dapati bahwa title adalah
        # "Profil Index App"
        self.assertEqual(self.driver.title, "Profil Index App")
        self.fail("Testing belum selesai")

