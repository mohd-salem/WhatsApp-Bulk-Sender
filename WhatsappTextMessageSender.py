# -*- coding: utf-8 -*-
import time
from time import sleep
import random
import os
from csv import DictReader
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from emoji.unicode_codes import UNICODE_EMOJI
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.webdriver import FirefoxProfile



#options = Options()
#headless= False

Num = []
errorNum = []
msg = []

image = 'C:\\Users\\NoVa\\OneDrive\\Desktop\\py\\whatsapp-send\\img.jpg'

# إحضار الأسماء و الأرقام
Num = [i for i in DictReader(open('contacts.csv', encoding = 'UTF-8'))]

with open("msg.txt",'r', encoding='UTF-8-sig') as txt :
    for line in txt :
        msg.append(line[:len(line)-1])

    print("Connecting ...")

#chromeOptions = webdriver.ChromeOptions()

prefs={'disk-cache-size': 4096 }
#chromeOptions.add_experimental_option("prefs", prefs)
#profile = FirefoxProfile("C:\\Users\\NoVa\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
#print(profile)
# Link chromedriver
#driver = webdriver.Chrome('chromedriver', options = chromeOptions)


driver = webdriver.Firefox()
#options.add_argument("--headless")
print('You are using Gecko with version '+ (driver.capabilities['browserVersion']))


print("Going to Whatsapp page")

driver.implicitly_wait(20)

driver.get('https://web.whatsapp.com')

sent = 0 # Sent masseges

# Waiting you to enter QRcode
print("Scan QRcode...")
input("Press Enter")
print("QRcode Done")
    
total = len(Num)

print("I will send "+str(len(Num))+" masseges")

con = False

contact = ''

send_button = EC.presence_of_element_located(('xpath', '//*[@id="main"]/header/div[2]/div/div/span'))
msg_field = EC.presence_of_element_located(('xpath','//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/span/div/div[2]/div/div[3]/div[1]/div[2]')) 

# _2Vo52 class
def img_add():
    driver.find_elements_by_class_name('_3ndVb')[5].click()
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input').send_keys(image)
    time.sleep(3)


def text_add():
    WebDriverWait(driver, 30).until(msg_field)  
    text_place = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')
    for m in range(len(msg)) :
        text_place.send_keys(msg[m])
        #if(m==1) :
            #text_place.send_keys(' '+num[len])
        text_place.send_keys(Keys.SHIFT, Keys.ENTER)
    time.sleep(3)
    text_place.send_keys(Keys.ENTER)
def process():
    for num in Num :
        print(num['Name'], str(num['Phone 1 - Value']), end=': ')
        newName = False
        network = True
        while(not newName) :
            try :
                driver.get('https://web.whatsapp.com/send?phone='+str(num['Phone 1 - Value'])+'&text=&source=&data=')
                WebDriverWait(driver, 40).until(send_button)

                print(contact, driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div/div/span').text)

                if(driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div/div/span').text != contact) :
                    newName = True

                time.sleep(2)
            except TimeoutException :
                errorNum.append(num)
                network = False
                newName = True
                print("⛔")          
            except NoSuchElementException :
                errorNum.append(num)
                network = False
                newName = True
                print("⛔")
            except :
                time.sleep(2)
                
        if (not network) : continue
        # إضافة الصورة
        img_add()

        #إضافة الرسالة

        text_add()
        delay=random.randint(10, 85)
        print(delay)

        time.sleep(delay)
        
        sent += 1
        contact = driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div/div/span').text
        print('✅')

        if(con != True) :
            user = input("أرسل تم لتفعيل الإنتقال التلقائي")
            if (user == "تم") :
                con = True

process()

print("تم كتابة الأرقام التي حدث فيها خطأ في ملف error.txt")
with open("error.txt", 'w') as errorFile :
    for i in errorNum :
        errorFile.write(i[0]+','+str(i[1]))

print("تم إرسال "+str(sent)+" رسالة")

input("Press Enter to quit")
driver.quit()





