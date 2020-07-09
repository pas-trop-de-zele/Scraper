from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select

# ======================== INFO ================================
"""
Preferences for efficiency
2 - block, 1 - allow, 0 - default

***Need to further read about chrome profile and these options
=>>>> These were forked from Dinuduke github
"""
PREFS = {"profile.managed_default_content_settings.images":2,
         "profile.default_content_setting_values.notifications":2,
         "profile.managed_default_content_settings.stylesheets":2,
         "profile.managed_default_content_settings.cookies":1,
         "profile.managed_default_content_settings.javascript":1,
         "profile.managed_default_content_settings.plugins":2,
         "profile.managed_default_content_settings.popups":2,
         "profile.managed_default_content_settings.geolocation":2,
         "profile.managed_default_content_settings.media_stream":2,
         }

# Potential classes name that Nike use for their size chart
POTENTIAL_CLASSES = ['css-1uentg', 'css-1gxjmmq']

# Billing Info
FIRST_NAME = "Pablo"
LAST_NAME = "Escobar"
ADDRESS1 = "9039 Bolsa Ave"
ADDRESS2 = "Suite 309"
CITY = "Westmisnter"
POSTAL_CODE = "92704"
EMAIL = "pescobar@yahoo.com"
PHONE_NUMBER = "7145359388"

# ========================================================



chrome_options = webdriver.ChromeOptions()

# Add reference defined above
chrome_options.add_experimental_option('prefs', PREFS)

browser = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\chromedriver.exe', options=chrome_options)

browser.get("https://www.nike.com/t/lebron-17-basketball-shoe-6LSXgh/BQ3177-601")

# find all divs with size's class name
for POTENTIAL_CLASS in POTENTIAL_CLASSES:
    """
    Look for divs with this classname
    """
    sizes = browser.find_elements_by_css_selector('div.' + POTENTIAL_CLASS)
    if sizes:
        break

# print("Available sizes:")

# Dict to hash size with number choice
size_options = {}
choice_number = 1
"""
Look inside found div
which are sizes that out of stock
"""
for size in sizes:
    size_display = size.find_element_by_tag_name('input')
    # if attribute 'disabled' exist means out out stock
    out_of_stock = size_display.get_attribute('disabled')
    # if out_of_stock:
    #     print(f"{choice_number}. {size.text} <= OUT OF STOCK")
    # else:
    #     print(f"{choice_number}. {size.text}")

    """
    save 'choice_number' : [size text, size display object] 

    size display object to perform actions later
    """ 
    size_options[choice_number] = [size.text, size_display]
    choice_number += 1

# Get size from user
# number_option = int(input("Please select number according to your desired size: "))

# ========================
# TESTING VALUE FIRST SIZE
number_option = 1
# ========================

# Get size button element saved from above
size_button = size_options[number_option][1]
# Free up space
size_options = {}

add_to_cart = browser.find_element_by_css_selector("button[aria-label='Add to Cart']")

item_added = False
# Check if item is added yet, if not click add to cart again
while not item_added:
    mouse = ActionChains(browser)
    mouse.click(size_button).click(add_to_cart).perform()
    """
    For some reason, could not use element.text to retrieve text 
    from cart span => use execute_script() to call js script instead 
    through attribute .textContent
    """
    item_count = browser.execute_script("return document.querySelector('span.cart-jewel').textContent")
    # Default is 0, if item added, this will change and stop loop
    if item_count != '0':
        item_added = True


# Go to cart
browser.get("https://www.nike.com/us/en/cart")

# wait until 'Go to checkout' option is available on checkout page then click
WebDriverWait(browser, 10).until(
    expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automation='go-to-checkout-button']"))
).click()

# wait until 'Check out as guest' option is available on checkout page then click
guest_checkout = WebDriverWait(browser, 10).until(
    expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automation='guest-checkout-button']"))
).click()

# wait until 'Enter address manually' option is available on checkout page
WebDriverWait(browser, 10).until(
    expected_conditions.element_to_be_clickable((By.ID, "addressSuggestionOptOut"))
).click()

# Select to add address field 2
browser.find_element_by_css_selector("button[aria-controls='address2']").click()

# FILLING IN STATES DROPDOWN
states = Select(browser.find_element_by_id("state"))
states.select_by_visible_text('California')

# FILLING IN ADDRESS FORMS
mouse = ActionChains(browser)

# Find according fields to enter information
first_name = browser.find_element_by_id("firstName")
last_name = browser.find_element_by_id("lastName")
address1 = browser.find_element_by_id("address1")
address2 = browser.find_element_by_id("address2")
city = browser.find_element_by_id("city")
postal_code = browser.find_element_by_id("postalCode")
email = browser.find_element_by_id("email")
phone_number = browser.find_element_by_id("phoneNumber")

mouse.send_keys_to_element(first_name, FIRST_NAME)
mouse.send_keys_to_element(last_name, LAST_NAME)
mouse.send_keys_to_element(address1, ADDRESS1)
mouse.send_keys_to_element(address2, ADDRESS2)
mouse.send_keys_to_element(city, CITY)
mouse.send_keys_to_element(postal_code, POSTAL_CODE)
mouse.send_keys_to_element(email, EMAIL)
mouse.send_keys_to_element(phone_number, PHONE_NUMBER)
mouse.perform()

browser.find_element_by_css_selector("button[type='submit']").click()



