# - abstraction programming
# - error handling
# - use function definition properly with all return types and comments
# -

# driver
# open link

# check product availabilty (products > tickets > product name > pass date > pass time > then 2 clicks), 
# checkout (go to checkout > (create account / log in) > save and continue > pay now)
# take screenshot

# driver
# open link


from datetime import datetime
from typing import Literal

debug = True

def click_element(driver, element_locator: Literal,element_name: str) -> bool:    
    try:
        elem = element_name
        return True
    except:
        print("no such element found")
        return False
    pass

def click_link_element(driver, link_text: str) -> bool:
    try:
        element = driver.find_element_by_link_text(link_text)
    except:
        print("No such element : {}".format(link_text))

def date_picker(driver, date) -> bool:
    click_element("Calender")
    try:
        driver.send_keys(date)
    except:
        print("Date not available")
    pass

def no_of_tickets(driver, adult: int, child: int) -> bool:
    click_element("Adult selection").send_keys(adult)
    click_element("Child selection").send_keys(child)
    pass

def select_time(driver, time):
    click_element("Time row which contains {time}")
    pass

def handle_alerts(driver):
    try:
        alert = driver.switch_to.alert
        alert.accept()
        print("alert accepted")
    except:
        # timeout_exception
        print("no alert")
    pass

def take_screenshot(driver, img_name: str) -> bool:
    driver.save_screenshot(img_name)
    pass

def create_account(driver, email: str, password: str, username_first: str, username_last: str) -> bool:    
    click_element("Create Account")
    click_element("Check box")
    click_element("email").send_keys(email)
    click_element("password").send_keys(password)
    click_element("retype password").send_keys(password)
    click_element("Create Account")
    handle_alerts(driver)
    click_element("First name").send_keys(username_first)
    click_element("Last name").send_keys(username_last)
    click_element("Save")
    pass    

def login_account(driver, email: str, password: str) -> bool:
    click_element("email").send_keys(email)
    click_element("password").send_keys(password)
    click_element("Sign in")
    handle_alerts(driver)
    pass

def product_existence(product_type: str, product_name: str) -> bool:
    try:
        click_link_element("Products")
        click_link_element(product_type)
        click_link_element(product_name)
        return True
    except:
        pass
        return False
        
# def product_existence(driver, product_type: str, product_name: str) -> bool:
#     click_element(driver, "products")
#     click_element(driver, product_type)
#     click_element(driver, product_name)    
#     # if desired product available result = true 
#     # if desired product unavailable result = false
#     exist = True/False
#     # Exception_nosuchelement -> print("no such product available")
#     return exist

def product_availabilty(driver, no_of_adult: int, no_of_child: int, date: datetime.date, time: datetime.time) -> bool:
    date_picker(driver, date)
    no_of_tickets(driver, no_of_adult, no_of_child)
    select_time(driver, time)
    click_element("Add to Cart")
    available = click_element("Go to Cart")
    # Exception_nosuchelement -> print("product not available for given date/time or no of tourists")
    return available

def checkout(driver) -> bool:
    click_element("Go to Checkout")
    if not debug:
        create_account(1, 2, 3)
        error = 'account creation failed'
    else:
        login_account(1, 2, 3)
        error = 'account login failed'

    handle_alerts()
    click_element("Save and Continue")
    click_element("Pay now")
    take_screenshot("payment_page.png")
    pass

def main():
    # driver
    # open link
    product_existence(driver, "tickets", "BRUNELLESCHI'S DOME")
    product_availabilty(driver, 2, 1, 2021-06-21, 12:00:00)
    checkout(driver)
    # driver.close()