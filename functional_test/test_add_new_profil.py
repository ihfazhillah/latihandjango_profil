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
        
        ### Empty Data
        self.fill_create_profil()
        errorlist = self.driver.find_elements_by_class_name("errorlist")
        self.assertEqual(len(errorlist), 2)
        self.assertTrue(all(x.text == "This field is required." \
                        for x in errorlist))

        ### Kosong nomor
        self.fill_create_profil("ihfazh", "muhammed", tipe_nomor="p")
        errorlist = self.driver.find_elements_by_class_name("errorlist")
        self.assertEqual(len(errorlist), 1)
        self.assertTrue(all(x.text == "This field is required." \
                        for x in errorlist))

        ### Kosong tipe
        self.fill_create_profil("ihfazh", "muhammed", "12344")
        errorlist = self.driver.find_elements_by_class_name("errorlist")
        self.assertEqual(len(errorlist), 1)
        self.assertTrue(all(x.text == "This field is required." \
                        for x in errorlist))

        ### Nomor bukan numeric
        self.fill_create_profil("ihfazh", "muhammed", "tipe_nomor")
        errorlist = self.driver.find_elements_by_class_name("errorlist")
        self.assertEqual(len(errorlist), 2)
        self.assertTrue(any(x.text == "This field is required." \
                        for x in errorlist))
        self.assertTrue(any(x.text == "'tipe_nomor' bukan numeric." \
                        for x in errorlist))

        ### url tanpa tipe
        self.fill_create_profil("ihfazh", "muhammed", url="http://ini.url")
        errorlist = self.driver.find_elements_by_class_name("errorlist")
        self.assertEqual(len(errorlist), 1)
        self.assertTrue(all(x.text == "This field is required." \
                        for x in errorlist))

        ## tipe tanpa url
        self.fill_create_profil("ihfazh", "muhammed", tipe_url="p")
        errorlist = self.driver.find_elements_by_class_name("errorlist")
        self.assertEqual(len(errorlist), 1)
        self.assertTrue(all(x.text == "This field is required." \
                        for x in errorlist))

        # Hmmt.. Oo gitu yah ketika data yang aku masukkan
        # salah, mesti ada pesan error..
        # Saatnya mengecek setiap data yang ada, apakah betul sesuai 
        # yang kita masukkan...??

        # Masuk ke halaman index
        self.driver.get(self.get_abs_url("profil:index"))
        # aku masih lihat, bhw disana ada 3 data
        profil_item = self.driver.find_element_by_id("profil_item")
        ul_li = self.driver.find_elements_by_id("item")
        self.assertEqual(len(ul_li), 3)
        # saya ingin mengeklik link pertama agar diarahkan ke arah detail
        ul_li[0].find_element_by_tag_name("a").click()
        self.assertEqual(self.driver.current_url,
                         self.get_abs_url("profil:detail", args=[1]))
        time.sleep(4)
        self.assertEqual(self.driver.title, "ihfazh's detail")
        detail_profil = self.driver.find_element_by_id("detail_profil")
        firstname = detail_profil.find_element_by_id("firstname")
        lastname = detail_profil.find_element_by_id("lastname")
        self.assertEqual(detail_profil.find_element_by_tag_name("h3").text,
                         "Detail Profil")
        self.assertEqual(firstname.text, "Firstname")
        self.assertEqual(lastname.text, "Lastname")
        firstname_val = detail_profil.find_element_by_id("f_val")
        lastname_val = detail_profil.find_element_by_id("l_val")
        self.assertEqual(firstname_val.text, "ihfazh")
        self.assertEqual(lastname_val.text, "muhammad")
        # Cek, bahwa phone number and website tidak ada
        self.assertRaises(NoSuchElementException,
                          self.driver.find_element_by_id,
                          "detail_phone")
        self.assertRaises(NoSuchElementException,
                          self.driver.find_element_by_id,
                          "detail_website")

        ## Test data kedua
        # maryam, soleh, 1234, p
        
        # Masuk ke halaman index
        self.driver.get(self.get_abs_url("profil:index"))
        # aku masih lihat, bhw disana ada 3 data
        profil_item = self.driver.find_element_by_id("profil_item")
        ul_li = self.driver.find_elements_by_id("item")
        self.assertEqual(len(ul_li), 3)
        # saya ingin mengeklik link kedua agar diarahkan ke arah detail
        ul_li[1].find_element_by_tag_name("a").click()
        self.assertEqual(self.driver.current_url,
                         self.get_abs_url("profil:detail", args=[2]))
        self.assertEqual(self.driver.title, "maryam's detail")
        detail_profil = self.driver.find_element_by_id("detail_profil")
        firstname = detail_profil.find_element_by_id("firstname")
        lastname = detail_profil.find_element_by_id("lastname")
        self.assertEqual(detail_profil.find_element_by_tag_name("h3").text,
                         "Detail Profil")
        self.assertEqual(firstname.text, "Firstname")
        self.assertEqual(lastname.text, "Lastname")
        firstname_val = detail_profil.find_element_by_id("f_val")
        lastname_val = detail_profil.find_element_by_id("l_val")
        self.assertEqual(firstname_val.text, "maryam")
        self.assertEqual(lastname_val.text, "soleh")
        # Cek, bahwa website tidak ada
        
        detail_nomor = self.driver.find_element_by_id("detail_phone")
        self.assertEqual(
                         detail_nomor.find_element_by_tag_name("h3"),
                         "Detail Nomor")
        nomor = detail_nomor.find_element_by_id("nomor")
        self.assertEqual(nomor.text, 'Nomor')
        tipe = detail_nomor.find_element_by_id("tipe_nomor")
        self.assertEqual(tipe.text, "Tipe")
        self.assertRaises(NoSuchElementException,
                          self.driver.find_element_by_id,
                          "detail_website")



        self.fail("Testing belum selesai")