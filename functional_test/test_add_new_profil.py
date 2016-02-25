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
        self.assertEqual(
                         self.driver.find_element_by_tag_name(
                                                              "a").get_attribute(
                                                              'href'),
                         self.get_abs_url("profil:logout"))
        
        ##########
        #testing input with valid data
        # So, aku ingin mengisi firstname dan lastname saja
        # Setelah aku save, aku diredirect ke halaman index
        self.fill_create_profil(firstname_="ihfazh",
                                lastname_="muhammad")
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
        self.fill_create_profil(firstname_= "maryam", 
                                lastname_= "soleh", 
                                nomor= "12345",  
                                tipe_nomor="p", 
                                url= "" , tipe_url="")
        self.assertEqual(self.driver.current_url,
                         self.get_abs_url("profil:index"))
        profil_item = self.driver.find_element_by_id("profil_item")
        ul_li = profil_item.find_elements_by_id("item")
        self.assertEqual(len(ul_li), 2)
        self.assertEqual(ul_li[0].text, "ihfazh")
        self.assertEqual(ul_li[1].text, "maryam")
        #### Ketiga
        self.fill_create_profil(firstname_="sakkuun", 
                                lastname_="ihfazh", 
                                nomor="11111", 
                                tipe_nomor="s", url="http://url.sakkuun", 
                                tipe_url="p")
        self.assertEqual(self.driver.current_url,
                         self.get_abs_url("profil:index"))
        profil_item = self.driver.find_element_by_id("profil_item")
        ul_li = profil_item.find_elements_by_id("item")
        self.assertEqual(len(ul_li), 3)
        self.assertEqual(ul_li[0].text, "ihfazh")
        self.assertEqual(ul_li[1].text, "maryam")
        self.assertEqual(ul_li[2].text, "sakkuun")

###
#Testing invalid input
###


        self.fail("Testing belum selesai")