# -*- coding: utf-8 -*-
from typing import Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import json
from datetime import date, datetime
if __name__=='__main__':
    import kn_compare

class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_untitled_test_case(self):
        driver = self.driver
        driver.get("https://kn.vutbr.cz/")
        driver.find_element_by_link_text(u"Informační systém KolejNetu").click()
        driver.find_element_by_name("odeslat").click()
        driver.find_element_by_name("str").click()
        driver.find_element_by_name("str").clear()
        driver.find_element_by_name("str").send_keys("A03-0934")
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='ÚČTO - Výpis fakturací za užívané služby v síti KolejNet'])[1]/following::td[1]").click()
        # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | xpath=(.//*[normalize-space(text()) and normalize-space(.)='ÚČTO - Výpis fakturací za užívané služby v síti KolejNet'])[1]/following::td[1] | ]]
        driver.find_element_by_xpath("//input[@value='hledej']").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)




class KNScrapper:
    def __init__(self, block='A03', min_room_num=1, max_room_num=40, min_floor=2, max_floor=9) -> None:
        
        #driver.implicitly_wait(30)
        base_url = "https://kn.vutbr.cz/"
        self.min_room = min_room_num
        self.max_room = max_room_num
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.block = block
        
    @staticmethod    
    def generate_room_str(flor, room_num):
        room_id = int(f"{flor}{room_num:02d}")
        return f"{room_id:04d}"


    def generate_room_numbers(self):
        current = self.min_room
        while current <= self.max_room:
            yield current
            current += 1

    def generate_flor(self):
        current = self.min_floor
        while current <= self.max_floor:
            yield current
            current += 1

    def get_room(self):
        for f in self.generate_flor():
            for r in self.generate_room_numbers():
                yield f"{self.block}-{self.generate_room_str(f, r)}"


    def main(self):
        for r in self.get_room():
            pass
            # print(r)

    def scrap(self):
        db = []
        self.driver = webdriver.Chrome()
        driver = self.driver
        driver.get("https://kn.vutbr.cz/is2/")
        driver.find_element_by_name("AUTH_LOGIN").click()
        driver.find_element_by_name("AUTH_LOGIN").click()
        driver.find_element_by_name("AUTH_LOGIN").clear()
        driver.find_element_by_name("AUTH_LOGIN").send_keys("mosyurchak")
        driver.find_element_by_xpath("//form[@action='https://kn.vutbr.cz/is2/index_ssl.html']").click()
        # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | xpath=//form[@action='https://kn.vutbr.cz/is2/index_ssl.html'] | ]]
        driver.find_element_by_name("AUTH_PW").click()
        driver.find_element_by_name("AUTH_PW").clear()
        driver.find_element_by_name("AUTH_PW").send_keys("q82a?#ar")
        driver.find_element_by_name("odeslat").click()
        driver.find_element_by_xpath("//input[@value='hledej']").click()
        driver.find_element_by_name("str").click()
        driver.find_element_by_name("str").clear()
        for r in self.get_room():
            driver.find_element_by_name("str").clear()
            driver.find_element_by_name("str").send_keys(r)
            driver.find_element_by_xpath("//input[@value='hledej']").click()
            driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Minimálni délka hledaného řetězce je 6 znaků'])[1]/following::table[1]").click()
            try:
                p1 = driver.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[2]/td/form/table[2]/tbody/tr[2]/td/table/tbody/tr[1]/th").text
                p1 = p1.replace('1. ', '')
            except:
                p1 = ""
            try:
                p2 = driver.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[2]/td/form/table[2]/tbody/tr[4]/td/table/tbody/tr[1]/th").text
                p2 = p2.replace('2. ', '')
            except:
                p2 = ""
                pass
            room = {r: [p1, p2]}

            db.append(room)
        return db

    @staticmethod
    def statistics(db, show=True, show_empty_rooms=False):
        count = 0
        full = []
        semi = []
        empty = []
        for i in db:
            d = list(i.items())
            room = d[0][0]
            pers = d[0][1]
            if pers[0] and pers[1]:
                full.append(room)
                count +=2
            elif pers[0] and not pers[1]:
                semi.append(room)
                count += 1
            elif not pers[0] and not pers[1]:
                empty.append(room)
            else:
                print('Processing error')

        if show:
            print("Number of students: ", count)
            print("Full rooms: ", len(full))
            print("One person living in the room: ", len(semi))
            print("Empty rooms: ", len(empty))
            if show_empty_rooms:
                print("Empty rooms: ", "\n".join(empty))

            


if __name__ == "__main__":
    a = KNScrapper(block='A03', min_floor=2)
    a.generate_room_str(7, 3)
    a.main()
    db = {}
    db = a.scrap()
    t = str(datetime.now()).replace(' ', '-').replace('.', "-")
    t = datetime.now().strftime('%Y-%m-%d-%H_%M_%S')
    file_content = json.dumps(db, indent=4)
    filename = f'C:/_projects/test-prj/db-{a.block}-{t}.json'
    with open(filename, 'w+') as f:
        f.write(file_content)

    # with open(filename, "r+") as f:
    #     db = json.loads(f.read())
    a.statistics(db)

    transfers = kn_compare.KnTransfers(new_db=filename)
    transfers.compare(scrapper_class=KNScrapper)
        
    #print(db)
    a.driver.stop_client()