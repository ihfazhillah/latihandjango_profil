import time
from selenium.common.exceptions import NoSuchElementException
from profil.models import UserProfile, Phone, Website
from .test_profil import FunctionalTestingProfilApp


class TestUpdateView(FunctionalTestingProfilApp):

    def create_db_data(self):
        profil = UserProfile.objects.create(firstname="ihfazh",
                                            lastname="amin")
        profil.phone.create(nomor="123456", tipe="p")
        profil.phone.create(nomor="213456", tipe="s")
        profil.website.create(url="http://url.ku", tipe='p')

    def assert_value_equal(self, name, value):
        elem = self.driver.find_element_by_name(name)
        self.assertEqual(elem.get_attribute("value"), value)

    def test_updating_data(self):
        self.create_db_data()
        ul_li = self.get_index_items()
        self.assertEqual(len(ul_li), 1)
        self.assertRaises(NoSuchElementException,
                          ul_li[0].find_element_by_link_text,
                          "Update")
        # kemudian aku login, dan aku dapati disana
        # terdapat update link
        self.driver.get(self.get_abs_url("profil:login"))
        self.enter_username_password(username="ihfazh",
                                     password="ihfazhillah")
        ul_li = self.get_index_items()
        links = [x.find_element_by_link_text("Update") for x in ul_li]
        links[0].click()
        # Pertama aku mengecek, apakah benar url yang ada?
        self.assertEqual(self.driver.current_url,
                         self.get_abs_url("profil:edit", args=[1]))
        # Kemudian title  dan header
        # Disitu harusnya tertulis "Update ihfazh's profil"
        self.assertEqual(self.driver.title, "Update ihfazh's profil")
        header = self.driver.find_element_by_tag_name("h3")
        self.assertEqual(header.text, "Update ihfazh's profil")
        # Karena ini adalah page digunakan untuk mengedit
        # maka, disana harusnya ada initial data. So, sebelum 
        # aku meng edit, aku lihat dulu initial datanya
        # benar atau tidak.
        self.assert_value_equal("firstname", "ihfazh")
        self.assert_value_equal("lastname", "amin")
        self.assert_value_equal("phone-0-nomor", "123456")
        self.assert_value_equal("phone-0-tipe", "p")
        self.assert_value_equal("phone-1-nomor", "213456")
        self.assert_value_equal("phone-1-tipe", "s")
        self.assert_value_equal("web-0-url", "http://url.ku")
        self.assert_value_equal("web-0-tipe", "p")
        # Haa, semua seperti yang di inginkan.
        # So, aku ingin mengubah phone nomer pertama.
        elem = self.driver.find_element_by_name("phone-0-nomor")
        elem.clear()
        elem.send_keys("098765")
        submit = self.driver.find_element_by_name("save")
        submit.click()
        self.assertTrue("098765" in self.driver.page_source)
        # Kemudian aku masuk lagi ke halaman itu, halaman update
        self.driver.get(self.get_abs_url("profil:edit", args=[1]))
        elem = self.driver.find_element_by_name("phone-0-nomor")
        elem.clear()
        elem.send_keys("ini invalid")
        submit = self.driver.find_element_by_name("save")
        submit.click()
        self.assertTrue("bukan numeric" in self.driver.page_source)
