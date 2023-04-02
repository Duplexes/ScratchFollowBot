import random
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import faker as faker
from selenium.webdriver.support.ui import Select
from TempMail import TempMail
import time


def gen_email():
    inbox = TempMail.generateInbox()
    return inbox.address, inbox.token, inbox


def create_account(user):
    driver = uc.Chrome()
    password = faker.Faker().password()
    driver.get('https://scratch.mit.edu/join')
    username = faker.Faker().user_name() + str(random.randint(1, 10000))
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'passwordConfirm').send_keys(password)
    driver.find_element(By.XPATH,'/html/body/div[2]/div/div/main/div/form/div/div[2]/button').click()
    time.sleep(5)
    select = Select(driver.find_element(By.ID, 'country'))
    time.sleep(4)
    select.select_by_value('United States')
    time.sleep(5)
    driver.find_element(By.XPATH,'/html/body/div[2]/div/div/main/div/form/div/div[3]/button').click()
    time.sleep(5)
    select = Select(driver.find_element(By.ID, 'birth_month'))
    select.select_by_value('1')
    select = Select(driver.find_element(By.ID, 'birth_year'))
    select.select_by_value('1978')
    driver.find_element(By.XPATH,'/html/body/div[2]/div/div/main/div/form/div/div[3]/button').click()
    time.sleep(4)
    driver.find_element(By.ID,'GenderRadioOptionPreferNot').click()
    driver.find_element(By.XPATH,'/html/body/div[2]/div/div/main/div/form/div/div[2]/button').click()
    time.sleep(4)
    email, token,inbox = gen_email()
    driver.find_element(By.ID,'email').send_keys(email)
    driver.find_element(By.XPATH,'/html/body/div[2]/div/div/main/div/form/div/div[3]/button').click()
    time.sleep(2)
    for x in range(100):
        emails = TempMail.getEmails(inbox)
        pattern = r'https://scratch\.mit\.edu/accounts/email_verify/\S+'
        try:
            match = re.search(pattern, emails[0].body)
            if match:
                url = match.group()
                print(f"Email: {email}, Password: {password},Username: {username}, URL: {url}")
                driver.get(url)
                with open('accounts.txt', 'a') as f:
                    f.write(f"{email}:{password}:{username}\n")
                time.sleep(5)
                driver.get(f'https://scratch.mit.edu/users/{user}/')
                time.sleep(2)
                driver.find_element(By.ID,'follow-button').click()
                break
            else:
                continue
        except:
            continue
    driver.quit()

if __name__ == '__main__':
    print("""
 _______    _ _             _______ 
(_______)  | | |           (_______)
 _____ ___ | | | ___  _ _ _   __    
|  ___) _ \| | |/ _ \| | | | / /    
| |  | |_| | | | |_| | | | |/ /____ 
|_|   \___/|_|_|\___/ \____(_______)
                                    
    """)
    user = input("Enter Username to follow: ")
    amount = int(input("Enter amount of accounts to attempt to create: "))
    for x in range(amount):
        try:
            create_account(user)
        except:
            continue
