import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from django.test import LiveServerTestCase
from django.contrib.auth.models import User 
from django.core.urlresolvers import reverse




class FunctionalTestingProfilApp(LiveServerTestCase):


    def get_abs_url(self, url_name, args=[]):
        """
        url helper, untuk mendapatkan absolute url 
        menggunakan live server url milik django
        """
        url = reverse(url_name, args=args)
        return "{}{}".format(self.live_server_url, url)

    def enter_username_password(self, 
                                username="" , 
                                password=""):
        username_ = self.driver.find_element_by_name("username")
        password_ = self.driver.find_element_by_name("password")
        username_.clear()
        username_.send_keys(username)
        password_.clear()
        password_.send_keys(password)
        submit = self.driver.find_element_by_name("submit")
        submit.click()

    def fill_create_profil(self, firstname_="", lastname_="",
                           nomor="", tipe_nomor="", 
                           url="", tipe_url=""):
        self.driver.get(self.get_abs_url("profil:create"))
        firstname = self.driver.find_element_by_name("firstname")
        # lastname
        lastname = self.driver.find_element_by_name("lastname")
        # phone-0-nomor
        phone_0_nomor = self.driver.find_element_by_name(
                                                                "phone-0-nomor")
        # phone-0-tipe
        phone_0_tipe = self.driver.find_element_by_name(
                                                               "phone-0-tipe")
        # web-0-url
        web_0_url = self.driver.find_element_by_name(
                                                            "web-0-url")
        # web-0-tipe
        web_0_tipe = self.driver.find_element_by_name(
                                                            "web-0-tipe") 
        # dan juga, aku dapati disana ada yang namanya
        # tombol save
        save = self.driver.find_element_by_name(
                                                "save")
        self.assertRaises(NoSuchElementException,
                          self.driver.find_element_by_name,
                          "phone-1-nomor")
        self.assertRaises(NoSuchElementException,
                          self.driver.find_element_by_name,
                          "phone-1-tipe")
        firstname.send_keys(firstname_)
        lastname.send_keys(lastname_)
        phone_0_nomor.send_keys(nomor)
        phone_0_tipe.send_keys(tipe_nomor)
        web_0_tipe.send_keys(tipe_url)
        web_0_url.send_keys(url)
        save.click()
        
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



class ProfilTest(FunctionalTestingProfilApp):
    def test_my_test(self):
        # Saya pergi ke profil app url
        self.driver.get(self.get_abs_url('profil:index'))
        # untuk memastikan bahwa aplikasi yang saya 
        # masuki benar, maka saya melihat ke url
        # dan saya dapati bahwa title adalah
        # "Profil Index App"
        self.assertEqual(self.driver.title, "Profil Index App")
        # Kemudian saya memperhatikan header page, dan
        # saya dapati juga seperti itu
        header = self.driver.find_element_by_tag_name("h1")
        self.assertEqual(header.text, "Profil Index App")
        # Dan aku juga dapati, ada sub header yang berbunyi
        # Project Sederhana Tentang Profil
        sub_header = self.driver.find_element_by_tag_name("h3")
        self.assertEqual(sub_header.text, "Project Sederhana Tentang Profil")
        # aku juga dapati, bahwa disana ada link menuju login
        # dikarenakan aku belum masuk
        self.assertTrue(self.driver.find_element_by_link_text("Login"))
        # Dan aku dapati, bahwa disana ada id="profil_item" namun
        # Kosong.
        profil_item = self.driver.find_element_by_id("profil_item")
        ul_li = profil_item.find_elements_by_id("item")
        self.assertEqual(len(ul_li), 0)

        




