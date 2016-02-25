import time
from selenium.common.exceptions import NoSuchElementException
from .test_profil import FunctionalTestingProfilApp

class AddNewProfil(FunctionalTestingProfilApp):
    def test_add_new_profil(self):
        self.driver.get(self.get_abs_url("profil:index"))
        # saya masuk login lagi,
        # saya klik login link dahulu
        self.driver.find_element_by_link_text("Login").click()
        self.assertEqual(self.driver.current_url,
                         self.get_abs_url("profil:login"))
        self.enter_username_password(username="ihfazh", 
                                     password="ihfazhillah")
        # Kemudian, saya ingin untuk menambah profil baru
        add_new_profil = self.driver.find_element_by_id("add_new_profil")
        add_new_profil.find_element_by_tag_name("a").click()
        # Dan aku dibawa ke form add profil
        self.assertEqual(self.driver.current_url, 
                         self.get_abs_url("profil:create"))
        # Aku lihat ke title tulisannya 
        # Tambahkan Profil Baru
        self.assertEqual(self.driver.title, 
                         "Tambahkan Profil Baru")
        # Dan juga di header pagenya
        header = self.driver.find_element_by_tag_name("h3")
        self.assertEqual(header.text, "Tambahkan Profil Baru")
        # Karena aku sudah login,
        # maka disana juga ada logged_as ihfazh
        # dan ada juga tulisan logout
        logged_as = self.driver.find_element_by_id("logged_as")
        self.assertEqual(logged_as.text,
                         "Logged as ihfazh")
        logout = self.driver.find_element_by_id("logout")
        # print(help(logout))
        self.assertEqual(
                         self.driver.find_element_by_tag_name("a").get_attribute('href'),
                         self.get_abs_url("profil:logout"))
        # Aku juga dapati, disitu ada form dengan beberapa input

        # firstname
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
        self.assertEqual(save.get_attribute("type"), "submit")

        ##########
        #testing input with valid data
        # So, aku ingin mengisi firstname dan lastname saja
        firstname.send_keys("ihfazh")
        lastname.send_keys("muhammad")
        # Dan itu berhasil. Tidak ada error
        save.click()
        # Setelah aku save, aku diredirect ke halaman index
        self.assertEqual(
                         self.driver.current_url,
                         self.get_abs_url("profil:index"))
        # Disana, aku bisa lihat profil baru yang telah aku buat
        profil_item = self.driver.find_element_by_id("profil_item")
        ul_li = profil_item.find_elements_by_id("item")
        self.assertEqual(len(ul_li), 1)
        self.assertEqual(ul_li[0].text, "ihfazh")

        # Oke, berhasil, sekarang aku ingin membuat profil baru lagi
        # Yaitu dengan firstname , lastname, dan juga phone
        # "maryam", "soleh", "12345", "p"
        # firstname
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
        firstname.send_keys("maryam")
        lastname.send_keys("soleh")
        phone_0_nomor.send_keys("12345")
        phone_0_tipe.send_keys("p")
        save.click()
        self.assertEqual(self.driver.current_url,
                         self.get_abs_url("profil:index"))
        profil_item = self.driver.find_element_by_id("profil_item")
        ul_li = profil_item.find_elements_by_id("item")
        self.assertEqual(len(ul_li), 2)
        self.assertEqual(ul_li[0].text, "ihfazh")
        self.assertEqual(ul_li[1].text, "maryam")

        # dan aku mau membuat profil yang ke tiga dengan detail
        # sakkuun , ihfazh, 11111, s, http://url.sakkuun, p
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
        firstname.send_keys("sakkuun")
        lastname.send_keys("ihfazh")
        phone_0_nomor.send_keys("11111")
        phone_0_tipe.send_keys("s")
        web_0_tipe.send_keys("p")
        web_0_url.send_keys("http://url.sakkuun")
        save.click()
        self.assertEqual(self.driver.current_url,
                         self.get_abs_url("profil:index"))
        profil_item = self.driver.find_element_by_id("profil_item")
        ul_li = profil_item.find_elements_by_id("item")
        self.assertEqual(len(ul_li), 3)
        self.assertEqual(ul_li[0].text, "ihfazh")
        self.assertEqual(ul_li[1].text, "maryam")
        self.assertEqual(ul_li[2].text, "sakkuun")

        self.fail("Testing belum selesai")