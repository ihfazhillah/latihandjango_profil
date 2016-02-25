from selenium.common.exceptions import NoSuchElementException
from .test_profil import FunctionalTestingProfilApp


        ###
        # Login
        ###
class LoginTest(FunctionalTestingProfilApp):
    def testing_login(self):
        self.driver.get(self.get_abs_url("profil:index"))
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
        self.assertTrue(self.driver.find_element_by_name("username"))
        self.assertTrue(self.driver.find_element_by_name("password"))
        # Ok, sekarang saya harus bersungguh sungguh.
        # Saya memasukkan data username dan password dengan benar
        self.enter_username_password(username="ihfazh", 
                                     password="ihfazhillah")
        # Dan kemudian aku di redirect ke halaman utama.
        self.assertEqual(self.driver.current_url, self.get_abs_url('profil:index'))
        # Disana saya lihat bahwa nama saya tercantum..
        # Logged as ihfazh
        logged_as = self.driver.find_element_by_id("logged_as")
        self.assertEqual(logged_as.text, "Logged as ihfazh")
        # Dan di sampingnya saya lihat ada link untuk logout
        logout = self.driver.find_element_by_id("logout")
        self.assertEqual(logout.text, "Logout")
        # Dan saya juga lihat, disana terdapat link yang berbunyi
        # Add New Profil
        add_new_profil = self.driver.find_element_by_id("add_new_profil")
        self.assertEqual(add_new_profil.text,
                         "Add New Profil")
        # Ok, saya sudah puas sementara.
        # Sekarang, saya ingin keluar dahulu.
        # Sehingga link logout aku klik
        logout.find_element_by_tag_name("a").click()
        # Dan saya langsung redirect ke index
        self.assertEqual(self.driver.current_url, 
                         self.get_abs_url("profil:index"))
        # Serta session saya sudah terhapus
        # Sehingga :
        # Diliuar, saya tidak dapati logged_as
        self.assertRaises(NoSuchElementException, 
                         self.driver.find_element_by_id, 
                         "logged_as")
        # juga logout link
        self.assertRaises(NoSuchElementException, 
                         self.driver.find_element_by_id, 
                         "logout")
        # Juga add new profil
        self.assertRaises(NoSuchElementException, 
                         self.driver.find_element_by_id, 
                         "add_new_profil")
