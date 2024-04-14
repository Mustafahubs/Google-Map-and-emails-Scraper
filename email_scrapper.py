import time,csv, os, sys, re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Automations import PopularDefs
from urllib.parse import urlparse

class Email_Extractor_App():
    def __init__(self):
        self.input_file = 'input_file.csv'
        self.output_file = 'output_file.csv'
        self.already_done_file = 'already_done.txt'
        self.no_emails_file = 'no_emails.txt'

    def open_browser(self):
        myClass = PopularDefs()
        driver = myClass.browserChrome(kill=True)
        return driver
    
    def read_website_urls(self):
        with open(self.input_file,'r',encoding='utf-8') as f:
            reader = f.readlines()
            urls = [row.split(',')[0].strip() for row in reader[1:]]
        return urls
    
    def extract_contact_urls(self,url,driver):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace('www.', '').strip()
        querry = f'https://www.bing.com/search?q=site:{domain} contact'
        driver.get(querry)
        time.sleep(3)
        contact_urls_tag = driver.find_elements('xpath','//main[@aria-label="Search Results"]/ol/li/div/a[contains(@href,"http")]')
        contact_urls = [url.get_attribute('href') for url in contact_urls_tag[:2]]
        return contact_urls
    
    def extract_emails(self,driver):
        emails_tags = driver.find_elements('xpath','//div[@class="container"]//tbody/tr')
        emails = [tag.find_element('xpath','./td[1]').get_attribute('textContent').strip() for tag in emails_tags]
        return emails
    
    def read_already_done(self):
        with open(self.already_done_file,'r',encoding='utf-8') as f:
            reader = f.readlines()
            already_scraped_urls = [row.strip() for row in reader]
        return already_scraped_urls
    
    def write_already_done(self,url):
        with open(self.already_done_file,'a',encoding='utf-8') as f:
            f.write(url + '\n')
    
    def write_no_emails(self,url):
        with open(self.no_emails_file,'a',encoding='utf-8') as f:
            f.write(url + '\n')

    def extract_data(self,driver,url):
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        print(f'[INFO] - Getting URL: {url}')
        driver.get(url)
        time.sleep(5)
        driver.get('chrome-extension://ejecpjcajdpbjbmlcojcohgenjngflac/app.html')
        time.sleep(2)
        emails = self.extract_emails(driver)
        if not emails:
            contact_urls = self.extract_contact_urls(url,driver)
            if contact_urls:
                for contact_url in contact_urls:
                    print(f'[INFO] - Getting URL: {contact_url}')
                    driver.get(contact_url)
                    time.sleep(5)
                    driver.get('chrome-extension://ejecpjcajdpbjbmlcojcohgenjngflac/app.html')
                    time.sleep(2)
                    emails_2 = self.extract_emails(driver)
                    if emails_2:
                        clear_history_btn = driver.find_elements('xpath','//button[text()="Clear"]')
                        if clear_history_btn: clear_history_btn[0].click()
                        time.sleep(.5)
                        driver.switch_to.alert.accept()
                        time.sleep(.5)
                        print(f'[INFO] - Found Emails: {emails_2} , URL: {url}')
                        return emails_2
                    else:
                        print(f'[INFO] No emails found for URL: {url}')
                        return []
            else:
                print(f'[INFO] No emails found for URL: {url}')
                return []
        else:
            clear_history_btn = driver.find_elements('xpath','//button[text()="Clear"]')
            if clear_history_btn: clear_history_btn[0].click()
            time.sleep(.5)
            driver.switch_to.alert.accept()
            time.sleep(.5)
            print(f'[INFO] - Found Emails: {emails[0]} , URL: {url}')
            return emails

    
    def save_data(self,row):
        with open(self.output_file,'a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    
    def csv_header(self):
        with open(self.output_file,'w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Website URL','Email-1','Email-2','Email-3','Email-4','Email-5'])
    
    def run(self):
        if self.input_file not in os.listdir(): sys.exit(f'\n[ERROR] - ({self.input_file}) not found in the current directory!\n')
        if self.output_file not in os.listdir(): self.csv_header()
        if self.already_done_file not in os.listdir(): open(self.already_done_file,'w').close()
        driver = self.open_browser()
        all_urls = self.read_website_urls()
        for url in all_urls:
            already_done = self.read_already_done()
            if url not in already_done:
                self.extract_data(driver,url)
            else:
                print(f'[Skipped] - Already done URL: {url}')
        
        print(f'\n[INFO] - Finished.....\n')

if __name__ == '__main__':
    app = Email_Extractor_App()
    app.run()

