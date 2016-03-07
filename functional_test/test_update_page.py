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

    def test_updating_data(self):
        self.create_db_data()
        ul_li = self.get_index_items()
        self.assertEqual(len(ul_li), 1)
        # # mencari update link
        # link = ul_li[0].find_element_by_tag_name("a")
        # link.click()
        self.assertRaises(NoSuchElementException,
                          ul_li[0].find_element_by_link_text,
                          "Update")
        # kemudian aku login, dan aku dapati disana 
        # terdapat update link
        self.driver.get(self.get_abs_url("profil:login"))
        self.enter_username_password(username="ihfazh", 
                                     password="ihfazhillah")
        time.sleep(2)
        ul_li = self.get_index_items()
        links = [x.find_element_by_link_text("Update") for x in ul_li]
        print(links)
        self.fail("belum selesai")
