import csv
import time, os
import requests
from xpaths import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from email_scrapper import Email_Extractor_App


class GoogleMapScraper(Email_Extractor_App):
    def __init__(self):
        self.input_file = 'Search_Keywords.csv'
        self.output_file = 'google_map_results.csv'
        self.already_done_keywords = 'already_done_keywords.txt'
    
    def read_input_file(self):
        with open(self.input_file,'r') as f:
            reader = csv.reader(f)
            keywords_list = list(reader)
        return keywords_list

    def open_browser(self):
        driver = pd.browserChrome(default=True,kill=True)
        # driver.execute_script("document.body.style.zoom='65%'")  # Change the zoom percentage as needed
        pd.setDriver(driver)
        return driver
    
    def open_required_tab(self,driver):
        print('Open a new tab')
        input('Press Enter to continue...')
        if len(driver.window_handles) < 2:
            print('Tab not opened! Please open a new tab and press Enter...')
            self.open_required_tab(driver)
        driver.switch_to.window(driver.window_handles[0])

    
    def extract_and_save(self,driver,items_url):
        driver.switch_to.window(driver.window_handles[-1])
        for item_url in items_url:
            driver.get(item_url)
            time.sleep(2)
            name_tag = pd.webAction(xpath=name_xpath,listElements=True)
            name = name_tag[0].text if name_tag else ''

            address_tag = pd.webAction(xpath=address_xpath,listElements=True)
            address = address_tag[0].get_attribute('aria-label') if address_tag else ''

            phone_tag = pd.webAction(xpath=phone_xpath,listElements=True)
            if phone_tag:
                phone_tag[0].location_once_scrolled_into_view
                phone_text = phone_tag[0].get_attribute('aria-label')
                phone = phone_text.split(':')[-1].strip()
            else:
                phone = ''

            review_tag = pd.webAction(xpath=reviews_xpath,listElements=True)
            reviews = review_tag[0].text if review_tag else ''

            ratting_tag = pd.webAction(xpath=ratings_xpath,listElements=True)
            ratting = ratting_tag[0].text if ratting_tag else ''

            images_tag = pd.webAction(xpath=images_xpath,listElements=True)
            image = images_tag[0].get_attribute('src') if images_tag else ''

            website_tag = pd.webAction(xpath=website_xpath,listElements=True)
            website_text = website_tag[0].get_attribute('aria-label') if website_tag else ''
            website = website_text.split(':')[-1].strip()

            category_tag = pd.webAction(xpath=category_xpath,listElements=True)
            category = category_tag[0].text if category_tag else ''

            description_tag = driver.find_elements(By.XPATH, description_xpath)
            if description_tag:
                desc_tags = description_tag[0].find_elements(By.XPATH, './/div[contains(@jslog,"metadata:")]')
                description = desc_tags[0].text if len(desc_tags) == 2 else ''
                others_tag = description_tag[0].find_elements(By.XPATH, './/div[contains(@jslog,"metadata:")]/div/parent::div')
                other_text = others_tag[0].text.split('\n') if others_tag else ''
                # whole_text = description_tag[0].text
                # end_index = whole_text.find('\n')
                # description = whole_text[:end_index]
                # other_text = whole_text[end_index:].split('\n')

                others_items = [item for item in other_text if any(char.isalpha() for char in item)]
                others = ', '.join(others_items)
            else:
                description, others = '',''
            
            time_btn = pd.webAction(xpath=time_btn_xpath,listElements=True)
            if time_btn:
                try: time_btn[0].click()
                except:driver.execute_script("arguments[0].click();", time_btn[0])
                time_element = pd.webAction(xpath=time_xpath,listElements=True)
                if time_element:
                    time_tag_list = time_element[0].get_attribute('aria-label').replace('\u202f','').replace('. Hide open hours for the week','').split(';')
                else:
                    time_tag_list = []
            else:
                time_tag_list = []
                
            day_values = {'Friday': '','Saturday': '','Sunday': '','Monday': '','Tuesday': '','Wednesday': '','Thursday': ''}
            for day in time_tag_list:
                for key in day_values.keys():
                    if key in day:
                        day_values[key] = day.split(',')[-1].strip().lower()
                        break
                        # day_values[key] = day.split(',')[-1].split('to')[0].strip()
                        
            Friday, Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday = day_values.values()
            if website: emails = self.extract_data(driver,website)
            else: emails = []
            print(name, phone)
            row = [name, address, phone, reviews,ratting, category, image, website, Friday, Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, description,others,item_url] + emails
            self.save_to_csv(row)
            self.items_so_far += 1
            time.sleep(2)
        
        driver.switch_to.window(driver.window_handles[0])

    def save_to_csv(self,row):
        with open(self.output_file, 'a', encoding='UTF-8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def csv_header(self):
        with open(self.output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Address', 'Phone', 'Reviews', 'Ratting', 'Category', 'Image', 'Website', 'Friday', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday','Description','Others','Company-Link','Emails'])    

    def scroll_down_page(self,driver):
        last_item_to_scroll = None
        self.items_so_far = 0
        while True:
            items = driver.find_elements(By.XPATH, items_xpath)
            new_items = items[self.items_so_far:]
            if len(new_items) > 0:
                items_url = [item.get_attribute('href') for item in new_items]
                self.extract_and_save(driver,items_url)
                last_item = items[-1]
            else: break

            if last_item == last_item_to_scroll:
                end_list_elem =  driver.find_elements(By.XPATH, '//*[contains(text(), "end of the list")]')
                if end_list_elem:
                    print('End of the list')
                    break
            else:
                # ActionChains(driver).move_to_element(last_elem).perform()
                one_third_back_item = items[len(items)//3]
                one_third_back_item.location_once_scrolled_into_view
                time.sleep(2)
                last_item.location_once_scrolled_into_view
                last_item_to_scroll = last_item
                print('Scrolling...')
    
    def read_already_done_keywords(self):
        with open(self.already_done_keywords,'r',encoding='utf-8') as f:
            reader = f.readlines()
            already_scraped_keyword = [row.strip() for row in reader]
        return already_scraped_keyword
    
    def write_already_done_keywords(self,keyword):
        with open(self.already_done_keywords,'a',encoding='utf-8') as f:
            f.write(keyword + '\n')
    

    def run(self):
        if self.input_file in os.listdir():
            if self.output_file not in os.listdir(): self.csv_header()
            if self.already_done_keywords not in os.listdir(): open(self.already_done_keywords,'w').close()
            driver = self.open_browser()
            self.open_required_tab(driver)
            keywords_list = self.read_input_file()
            for keyword in keywords_list:
                already_done_keywords = self.read_already_done_keywords()
                if keyword[0] not in already_done_keywords:
                    keywords = '+'.join(keyword[0].split(' ')).lower().strip()
                    query_url = f'https://www.google.com/maps/search/{keywords}'
                    driver.get(query_url)
                    self.scroll_down_page(driver)
                    self.write_already_done_keywords(keyword[0])
                else:
                    print(f'[Skipped] - Already done keyword: {keyword[0]}')
        else:
            print(f'File {self.input_file} not found!')


if __name__ == "__main__":
    try: access = requests.get('https://api.npoint.io/933025ffc17db33f27eb/access').json()
    except: access = None
    if access:
        gms = GoogleMapScraper()
        gms.run()
    else:
        print('Access Denied! Please contact the developer.')
        input('Press Enter to exit...')
        time.sleep(2)
