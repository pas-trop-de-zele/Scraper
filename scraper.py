from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


chrome_options = webdriver.ChromeOptions()

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

# Check if item is added yet, if not click again
item_added = False
while not item_added:
    mouse = ActionChains(browser)
    mouse.click(size_button).click(add_to_cart).perform()
    cart_item = browser.find_element_by_class_name("cart-jewel")
    print(f"Item in cart count: {cart_item.text}")
    if cart_item.text != '0' and cart_item.text != '':
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
    expected_conditions.visibility_of_element_located((By.ID, "addressSuggestionOptOut"))
).click()

# FILLING IN ADDRESS FORMS
mouse = ActionChains(browser)
# Select enter address manually
# browser.find_element_by_id('addressSuggestionOptOut').click()
# Select to add address field 2
browser.find_element_by_css_selector("button[aria-controls='address2']").click()
# Find according fields to enter information
first_name = browser.find_element_by_id("firstName")
last_name = browser.find_element_by_id("lastName")
address1 = browser.find_element_by_id("address1")
address2 = browser.find_element_by_id("address2")
city = browser.find_element_by_id("city")


mouse.send_keys_to_element(first_name, 'Pablo')
mouse.send_keys_to_element(last_name, 'Escobar')
mouse.send_keys_to_element(address1, '9039 Bolsa Ave')
mouse.send_keys_to_element(address2, 'Suite 309')
mouse.send_keys_to_element(city, 'Westminster')
mouse.perform()


