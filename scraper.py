from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

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

print("Available sizes:")

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
    if out_of_stock:
        print(f"{choice_number}. {size.text} <= OUT OF STOCK")
    else:
        print(f"{choice_number}. {size.text}")

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
mouse = ActionChains(browser)
# Add item to cart
mouse.click(size_button).pause(1).click(add_to_cart).pause(1).perform()
# Go to cart
browser.get("https://www.nike.com/us/en/cart")

mouse = ActionChains(browser) 
browser.find_element_by_css_selector("button[data-automation='go-to-checkout-button']").click()
mouse.pause(2).perform()
browser.find_element_by_css_selector("button[data-automation='guest-checkout-button']").click()



