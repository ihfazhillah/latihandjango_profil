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
        self.fail("Testing belum selesai")