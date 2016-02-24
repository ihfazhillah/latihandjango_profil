import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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

    def enter_username_password(self, 
                                username="" , 
                                password=""):
        username_ = self.driver.find_element_by_name("username")
        password_ = self.driver.find_element_by_name("password")
        username_.send_keys(username)
        password_.send_keys(password)
        submit = self.driver.find_element_by_name("submit")
        submit.click()

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
        
        ###
        # Login
        ###
        
        # Kemudian aku ingin mengeklik link login
        # Dan benar, link menghantarkanku ke halaman login ("profil:login")
        login_link = self.driver.find_element_by_link_text("Login")
        login_link.click()
        self.assertEqual(self.driver.current_url, self.get_abs_url("profil:login"))
        #Untuk benar benar memastikan bahwa ini emang login page
        # Aku melihat, titlenya bertuilsikan "Login Page"
        self.assertEqual(self.driver.title, 'Login Page')
        # dan ada header bertuliskan "Masuk Dulu bro"
        header = self.driver.find_element_by_tag_name("h3")
        self.assertEqual(header.text, 'Masuk Dulu bro')
        # aku menemukan disana ada 2 input text, yang satu bertuliskan
        # Username dan yang satunya lagi bertuliskan 
        # Password. Namun aku lupa untuk memasukkan data, dan kemudian
        # Aku meng-Enter
        self.enter_username_password()
        # Dan, taraaa... Pesan harus di isi muncul
        errors = self.driver.find_elements_by_class_name("errorlist")
        self.assertEqual(len(errors), 2)
        self.assertTrue(all([x.text == "This field is required." for x in errors]))
        # sadar akan hal itu, 
        # saya mencoba memasukkan username, tapi lupa 
        # memasukkan password dan saya mendapatkan pesan yang sama
        # lagi, namun hanya satu.
        self.enter_username_password(username="ihfazh")
        errors = self.driver.find_elements_by_class_name("errorlist")
        self.assertEqual(len(errors), 1)
        self.assertTrue(all(x.text == "This field is required." for x in errors))
        # Kemudian, saya memasukkan username dan password
        # tapi password yang saya masukkan salah
        self.enter_username_password(username="ihfazh", 
                                     password="password_salah")
        # Maka keluar peringatan kesalahan password/email
        # "Password atau Email yang anda masukkan salah"
        errors = self.driver.find_elements_by_class_name("errorlist")
        self.assertEqual(len(errors), 1)
        self.assertTrue(any(x.text == \
                        "Password atau Email yang anda masukkan salah"\
                        for x in errors))
        time.sleep(3)
        self.fail("Testing belum selesai")


