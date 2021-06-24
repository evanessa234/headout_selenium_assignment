from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, datetime



opts=webdriver.ChromeOptions()
opts.add_argument('--headless')
opts.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)

driver.maximize_window()
actions = ActionChains(driver)

driver.get("https://operaduomofirenze.skiperformance.com/en/store#/en/buy")

## closing cookies request ....................
## element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sitcookies"]/button')))
## element.click()
def click_xpath_element(xpath: str) -> str:
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        print("No such element : {}".format(xpath))
        exit()
    else:
        # actions.move_to_element(element).click().perform()
        element.click()
        return element

# checking available product .............
def click_link_element(link_text: str) -> bool:
    try:
        # element = driver.find_element_by_link_text(link_text)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))
    except:
        print("No such element : {}".format(link_text))
        exit()
    else:
        element.click()
        # actions.move_to_element(element).click().perform()
        # except:
        #     print("{} : not interactable".format(link_text))
        #     exit()

def product_existence(product_type: str, product_name: str) -> bool:
    try:
        time.sleep(4)
        click_link_element("Products")
        print("1 click")
        time.sleep(4)
        click_link_element(product_type)
        print("2 click")
        click_link_element(product_name)
        print("3 click")
        return True
    except:
        return False

# Checking datetime availabilty ..............
def is_datetime_valid(datetime_str: str) -> datetime:
    try:
        date_time_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except:
        print("Wrong datetime or format")
        exit()
    else:
        now = datetime.now()
        if (date_time_obj >= now):
            print("We are good to go")
            return date_time_obj
        else:
            print("selected datetime has already passed")
            exit()

def month(valid_date: datetime) -> str:
    return valid_date.strftime("%B")

def day(valid_date: datetime) -> str:
    return valid_date.day

def get_time(valid_date: datetime) -> datetime.time:
    return valid_date.time()

# send keys ........
def send_keys_to_xpath(xpath: str, key: str) -> bool:
    try:
        element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        element.click()
    except:
        print("no such element by xpath: {}".format(xpath))
    else:
        element.send_keys(key)

def create_account(email: str, password: str, uname_first: str, uname_last: str):
    click_xpath_element("//label[contains(text(),'I declare to be of legal age, to have read and und')]")
    send_keys_to_xpath("//input[@id='register-email']", email)
    send_keys_to_xpath("//input[@id='register-password']", password)
    send_keys_to_xpath("//input[@id='register-password2']", password)
    click_xpath_element("//input[@value='Create account']")
    # try:
    #     alert = driver.switch_to_alert()
    #     alert.accept()
    # except:
    #     pass
    send_keys_to_xpath("//input[@name='first_name']", uname_first)
    send_keys_to_xpath("//input[@name='last_name']", uname_last)
    click_xpath_element("//button[normalize-space()='Save']")
    # try:
    #     alert = driver.switch_to_alert()
    #     alert.accept()
    # except:
    #     pass

def login_account(email: str, password: str):
    click_xpath_element("//a[@class='button xs-width-full xs-my04 sm-w50p md-w70p lg-w60p']")
    send_keys_to_xpath("//input[@id='login-email']", email)
    send_keys_to_xpath("//input[@id='login-password']", password)
    click_xpath_element("//input[@value='Sign in']")

# date picker ...................
def calender_page(valid_date: datetime):
    click_xpath_element("//input[@id='js-validity_start-p_5131']")
    title_month = month(datetime.today())
    title_year = str(datetime.today().year)
    req_month = month(valid_date)
    req_year = str(valid_date.year)
    while not (title_month == req_month and title_year == req_year):
        try:
            click_xpath_element("//div[@id='zs-ui-datepicker-div']//span[@class='zs-ui-icon zs-ui-icon-circle-triangle-e'][normalize-space()='Next']")
        except:
            print("Date out of booking range")
            exit()
        else:
            title_date = click_xpath_element("//div[@id='zs-ui-datepicker-div']//div[@class='zs-ui-datepicker-title']").text
            title_month = title_date.split(" ")[0]
            title_year = title_date.split(" ")[1]

def select_date(valid_date: datetime):
    try:
        click_link_element(str(valid_date.day))
    except:
        print("Date not available")
        exit()

def date_picker(valid_date: str):
    calender_page(valid_date)
    select_date(valid_date)

# time slot selector.............
def time_slot_selector(req_time: datetime.time) -> str:
    try:
        element = driver.find_element_by_xpath("//li[contains(@class, 'gc xs-gc12 pointer js-booking-clickable') and contains(@data-time_from, '{}')]".format(req_time))
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
            # print(element.get_attribute("data-available_qty"))
            return int(element.get_attribute("data-available_qty"))
        except:
            try:
                button = driver.find_element_by_xpath("//div[contains(text(),'Next')]")
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()
                time.sleep(3)
                actions.move_to_element(element).click().perform()
                return int(element.get_attribute("data-available_qty"))
            except:
                print("All slots booked")
                exit()
    except:
        print("Please Enter exact available time")
        exit()

def tickets_needed(no_of_adult: int, no_of_paid_child: int, no_of_free_child: int) -> int:
    return no_of_adult + no_of_paid_child + no_of_free_child

def select_tickets(no_of_adult: int, no_of_paid_child: int, no_of_free_child: int, available_tickets: int, no_of_tickets_needed: int) -> bool:
    if (available_tickets >= no_of_tickets_needed):
        send_keys_to_xpath("//input[@name='sku_qty_20410']", no_of_adult)
        send_keys_to_xpath("//input[@name='sku_qty_20408']", no_of_paid_child)
        send_keys_to_xpath("//input[@name='sku_qty_20556']", no_of_free_child)
        return True
    else:
        print("number of Tickets not available")
        return False

def main():
    click_xpath_element("//*[@id='site-cookies']/button")
    input_datetime = input()
    input_product_type = input()
    input_product_name = input()
    no_of_adult, no_of_paid_child = map(int, input().split(" "))
    
    valid_date = is_datetime_valid(input_datetime)
    product_existence(input_product_type, input_product_name)
    time.sleep(5)
    date_picker(valid_date)
    req_time = get_time(valid_date)
    # print(type(req_time))

    # below line of code is just to handle code from breaking
    send_keys_to_xpath("//input[@name='sku_qty_20410']", 0)

    no_of_available_tickets = time_slot_selector(req_time)
    print(" total no of tickets available for selected slot : {}".format(no_of_available_tickets))

    no_of_req_tickets = tickets_needed(no_of_adult, no_of_paid_child, 0)
    print(" Total no of requires tickets : {} ".format(no_of_req_tickets))

    # if (no_of_available_tickets >= no_of_req_tickets):
    select_tickets(no_of_adult, no_of_paid_child, 0, no_of_available_tickets, no_of_req_tickets)

    try:
        click_link_element("Add to Cart")    
    except:
        print("Desired Quantity not available")
    else:
        click_link_element("Go to Cart")
        click_xpath_element("//div[@id='btn-checkout']") 
    time.sleep(4)

    is_account_already_created = int(input())
    email = input()
    password = input()
    if is_account_already_created:
        login_account(email, password)
        print("loggind in...")
    else:
        print("creating new account...")
        uname_first = input()
        uname_last = input()
        create_account(email, password, uname_first, uname_last)

    # time.sleep(4)
    # login_account("k@gmail.com", "12345")
    click_xpath_element("//button[normalize-space()='Save and continue']")
    time.sleep(2)
    click_xpath_element("//div[@class='buy-button button xs-width-full xs-block xs-mt1 xs-mb3 xs-mx-auto md-w50p lg-mt0 lg-mb2 lg-width-full js-register-payment']")
    time.sleep(4)
    driver.save_screenshot("headless_final_result.png")
    driver.close()
if __name__ == "__main__":
    main()



# from types import SimpleNamespace
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.alert import Alert
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from datetime import date, datetime

# opts=webdriver.ChromeOptions()
# opts.add_argument('--headless')
# opts.add_argument('window-size=1920x1080')
# # driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
# driver.maximize_window()
# actions = ActionChains(driver)

# driver.get("https://operaduomofirenze.skiperformance.com/en/store#/en/buy")

# ## closing cookies request ....................
# ## element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sitcookies"]/button')))
# ## element.click()
# def click_xpath_element(xpath: str) -> str:
#     try:
#         element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
#     except:
#         print("No such element : {}".format(xpath))
#         exit()
#     else:
#         # actions.move_to_element(element).click().perform()
#         element.click()
#         return element

# # checking available product .............
# def click_link_element(link_text: str) -> bool:
#     try:
#         # element = driver.find_element_by_link_text(link_text)
#         element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))
#     except:
#         print("No such element : {}".format(link_text))
#         exit()
#     else:
#         element.click()
#         # actions.move_to_element(element).click().perform()
#         # except:
#         #     print("{} : not interactable".format(link_text))
#         #     exit()

# def product_existence(product_type: str, product_name: str) -> bool:
#     try:
#         time.sleep(4)
#         click_link_element("Products")
#         print("1 click")
#         time.sleep(4)
#         click_link_element(product_type)
#         print("2 click")
#         click_link_element(product_name)
#         print("3 click")
#         return True
#     except:
#         return False

# # Checking datetime availabilty ..............
# def is_datetime_valid(datetime_str: str) -> datetime:
#     try:
#         date_time_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
#     except:
#         print("Wrong datetime or format")
#         exit()
#     else:
#         now = datetime.now()
#         if (date_time_obj >= now):
#             print("We are good to go")
#             return date_time_obj
#         else:
#             print("selected datetime has already passed")
#             exit()

# def month(valid_date: datetime) -> str:
#     return valid_date.strftime("%B")

# def day(valid_date: datetime) -> str:
#     return valid_date.day

# def get_time(valid_date: datetime) -> datetime.time:
#     return valid_date.time()

# # send keys ........
# def send_keys_to_xpath(xpath: str, key: str) -> bool:
#     try:
#         element = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
#         element.click()
#     except:
#         print("no such element by xpath: {}".format(xpath))
#     else:
#         element.send_keys(key)

# def create_account(email: str, password: str, uname_first: str, uname_last: str):
#     click_xpath_element("//label[contains(text(),'I declare to be of legal age, to have read and und')]")
#     send_keys_to_xpath("//input[@id='register-email']", email)
#     send_keys_to_xpath("//input[@id='register-password']", password)
#     send_keys_to_xpath("//input[@id='register-password2']", password)
#     click_xpath_element("//input[@value='Create account']")
#     try:
#         alert = driver.switch_to_alert()
#         alert.accept()
#     except:
#         pass
#     send_keys_to_xpath("//input[@name='first_name']", uname_first)
#     send_keys_to_xpath("//input[@name='last_name']", uname_last)
#     click_xpath_element("//button[normalize-space()='Save']")
#     try:
#         alert = driver.switch_to_alert()
#         alert.accept()
#     except:
#         pass

# def login_account(email: str, password: str):
#     click_xpath_element("//a[@class='button xs-width-full xs-my04 sm-w50p md-w70p lg-w60p']")
#     send_keys_to_xpath("//input[@id='login-email']", email)
#     send_keys_to_xpath("//input[@id='login-password']", password)
#     click_xpath_element("//input[@value='Sign in']")

# # date picker ...................
# def calender_page(valid_date: datetime):
#     click_xpath_element("//input[@id='js-validity_start-p_5131']")
#     title_month = month(datetime.today())
#     title_year = str(datetime.today().year)
#     req_month = month(valid_date)
#     req_year = str(valid_date.year)
#     while not (title_month == req_month and title_year == req_year):
#         try:
#             click_xpath_element("//div[@id='zs-ui-datepicker-div']//span[@class='zs-ui-icon zs-ui-icon-circle-triangle-e'][normalize-space()='Next']")
#         except:
#             print("Date out of booking range")
#             exit()
#         else:
#             title_date = click_xpath_element("//div[@id='zs-ui-datepicker-div']//div[@class='zs-ui-datepicker-title']").text
#             title_month = title_date.split(" ")[0]
#             title_year = title_date.split(" ")[1]

# def select_date(valid_date: datetime):
#     try:
#         click_link_element(str(valid_date.day))
#     except:
#         print("Date not available")
#         exit()

# def date_picker(valid_date: str):
#     calender_page(valid_date)
#     select_date(valid_date)

# # time slot selector.............
# def time_slot_selector(req_time: datetime.time) -> str:
#     try:
#         element = driver.find_element_by_xpath("//li[contains(@class, 'gc xs-gc12 pointer js-booking-clickable') and contains(@data-time_from, '{}')]".format(req_time))
#         try:
#             driver.execute_script("arguments[0].scrollIntoView(true);", element)
#             element.click()
#             # print(element.get_attribute("data-available_qty"))
#             return int(element.get_attribute("data-available_qty"))
#         except:
#             try:
#                 button = driver.find_element_by_xpath("//div[contains(text(),'Next')]")
#                 driver.execute_script("arguments[0].scrollIntoView(true);", button)
#                 button.click()
#                 time.sleep(3)
#                 actions.move_to_element(element).click().perform()
#                 return int(element.get_attribute("data-available_qty"))
#             except:
#                 print("All slots booked")
#                 exit()
#     except:
#         print("Please Enter exact available time")
#         exit()

# def tickets_needed(no_of_adult: int, no_of_paid_child: int, no_of_free_child: int) -> int:
#     return no_of_adult + no_of_paid_child + no_of_free_child

# def select_tickets(no_of_adult: int, no_of_paid_child: int, no_of_free_child: int, available_tickets: int, no_of_tickets_needed: int) -> bool:
#     if (available_tickets >= no_of_tickets_needed):
#         send_keys_to_xpath("//input[@name='sku_qty_20410']", no_of_adult)
#         send_keys_to_xpath("//input[@name='sku_qty_20408']", no_of_paid_child)
#         send_keys_to_xpath("//input[@name='sku_qty_20556']", no_of_free_child)
#         return True
#     else:
#         print("number of Tickets not available")
#         return False

# def main():
#     click_xpath_element("//*[@id='site-cookies']/button")
#     valid_date = is_datetime_valid("2021-10-29 17:15:00")
#     product_existence("Tickets", "Brunelleschi's Dome")
#     time.sleep(5)
#     date_picker(valid_date)
#     req_time = get_time(valid_date)
#     print(type(req_time))
#     # exit()
#     send_keys_to_xpath("//input[@name='sku_qty_20410']", 0)
#     no_of_available_tickets = time_slot_selector(req_time)
#     print(no_of_available_tickets)

#     no_of_req_tickets = tickets_needed(2, 3, 0)
#     print(no_of_req_tickets)

#     # if (no_of_available_tickets >= no_of_req_tickets):
#     select_tickets(2, 3, 0, no_of_available_tickets, no_of_req_tickets)

#     try:
#         click_link_element("Add to Cart")    
#     except:
#         print("Desired Quantity not available")
#     else:
#         click_link_element("Go to Cart")
#         click_xpath_element("//div[@id='btn-checkout']")   
#     time.sleep(4)
#     login_account("k@gmail.com", "12345")
#     click_xpath_element("//button[normalize-space()='Save and continue']")
#     time.sleep(4)
#     click_xpath_element("//div[@class='buy-button button xs-width-full xs-block xs-mt1 xs-mb3 xs-mx-auto md-w50p lg-mt0 lg-mb2 lg-width-full js-register-payment']")
#     # driver.get(url)
#     time.sleep(4)
#     driver.save_screenshot("headless_final_result.png")
# if __name__ == "__main__":
#     main()
