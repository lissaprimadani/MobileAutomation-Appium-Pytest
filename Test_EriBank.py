from cgitb import text
from time import time
from appium import webdriver
from h11 import Data
from pyparsing import empty
import pytest
from _pytest import mark
from _pytest.mark.structures import Mark

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['appium:deviceName'] = 'vivo vivo 1919'
desired_caps['appium:udid'] = '597e74ec'
#desired_caps['appium:deviceName'] = 'VirtualDevice'
#desired_caps['appium:udid'] = 'emulator-5554'
desired_caps['appium:appPackage'] = 'com.experitest.ExperiBank'
desired_caps['appium:appActivity'] = 'LoginActivity t12455 d0'


driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(10)

def test_success_view_popup():
    tx = driver.find_element_by_id ("android:id/message").text
    driver.implicitly_wait(10)
    assert tx == "Aplikasi ini dibuat untuk Android versi lama dan mungkin tidak berfungsi sebagaimana mestinya. Coba periksa apakah ada update, atau hubungi developer."
    driver.implicitly_wait(10)

def test_skip_popup():
    driver.find_element_by_id("android:id/button1").click()
    driver.implicitly_wait(10)
    BankTitle = driver.find_element_by_id("android:id/title").text
    assert BankTitle == "EriBank"
    driver.implicitly_wait(10)

datas_login_invalid = [
    ("" , ""), #empty input
    ("company", ""), #empty password
    ("", "company"), #empty username
    ("company", "company12345"), #password wrong
    ("comp", "company") #username wrong
]

@pytest.mark.parametrize('a,b', datas_login_invalid)
def test_login_invalid(a,b):
    driver.find_element_by_id("com.experitest.ExperiBank:id/usernameTextField").send_keys(a)
    driver.find_element_by_id("com.experitest.ExperiBank:id/passwordTextField").send_keys(b)
    driver.find_element_by_id("com.experitest.ExperiBank:id/loginButton").click()
    loginbutton = driver.find_element_by_id("com.experitest.ExperiBank:id/loginButton").text 
    assert loginbutton == "Login"

def test_login_valid():
    driver.find_element_by_id("com.experitest.ExperiBank:id/usernameTextField").send_keys("company")
    driver.find_element_by_id("com.experitest.ExperiBank:id/passwordTextField").send_keys("company")
    driver.find_element_by_id("com.experitest.ExperiBank:id/loginButton").click()
    loginbutton = driver.find_element_by_id("com.experitest.ExperiBank:id/makePaymentButton").text 
    assert loginbutton == "Make Payment"

@pytest.fixture
def test_predcondition_sendpayment():
    driver.find_element_by_id("com.experitest.ExperiBank:id/makePaymentButton").click()
    driver.find_element_by_id("com.experitest.ExperiBank:id/phoneTextField").send_keys("083123456789")
    driver.find_element_by_id("com.experitest.ExperiBank:id/nameTextField").send_keys("Lissa")
    driver.find_element_by_id("com.experitest.ExperiBank:id/amount").send_keys("10")
    driver.find_element_by_id("com.experitest.ExperiBank:id/countryButton").click()
    driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.widget.TextView[2]").click()
    driver.find_element_by_id("com.experitest.ExperiBank:id/sendPaymentButton").click()

def test_send_payment(test_predcondition_sendpayment):
    driver.find_element_by_id("android:id/button1").click()
    last_amount = driver.find_element_by_class_name("android.view.View").text
    assert last_amount == "Your balance is: 90,00$"

def test_cance_send_payment(test_predcondition_sendpayment):
    driver.find_element_by_id("android:id/button2").click()
    payment_home = driver.find_element_by_id("com.experitest.ExperiBank:id/sendPaymentButton").text
    assert payment_home == "Send Payment"

def test_close_payment_page():
    driver.find_element_by_id("com.experitest.ExperiBank:id/cancelButton").click()
    last_amount = driver.find_element_by_class_name("android.view.View").text
    assert last_amount == "Your balance is: 90,00$"

def test_logout():
    driver.find_element_by_id("com.experitest.ExperiBank:id/logoutButton").click()
    login_page = driver.find_element_by_id("com.experitest.ExperiBank:id/loginButton").text
    assert login_page == "Login"
