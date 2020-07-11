from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from settings import PREFS, CHROME_DRIVER_PATH, POTENTIAL_CLASSES
import billing_info

class Scraper:
    def __init__(self):
        # Set preference
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('prefs', PREFS)
        self.browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=self.chrome_options)
        # set billing info
        self.FIRST_NAME = billing_info.FIRST_NAME
        self.LAST_NAME = billing_info.LAST_NAME
        self.ADDRESS1 = billing_info.ADDRESS1
        self.ADDRESS2 = billing_info.ADDRESS2
        self.CITY = billing_info.CITY
        self.STATE = billing_info.STATE
        self.POSTAL_CODE = billing_info.POSTAL_CODE
        self.EMAIL = billing_info.EMAIL
        self.PHONE_NUMBER = billing_info.PHONE_NUMBER
        self.size_options = {}
    
    def go_to_product(self, product_url):
        """
        Go to product page

        Args:
          url: url of product page
        """
        self.browser.get(product_url)

    def go_to_cart(self):
        """
        Go to cart page
        """
        cart_url = "https://www.nike.com/us/en/cart"
        self.browser.get(cart_url)

    def get_sizes(self):
        """
        Find all divs containing sizes
        Look for inner element that hold the size element
        Add to size_options dict
        """
        for potentials_class in POTENTIAL_CLASSES:
            size_containing_divs = self.browser.find_elements_by_css_selector('div.' + potentials_class)
        for div in size_containing_divs:
            size_button = div.find_element_by_tag_name('input')
            self.size_options[div.text] = size_button

    def choose_size(self, your_size):
        """
        Get size button from size_option dict and click on it

        Arg: 
            your_size: your desired size
        """
        try:
            if self.is_available(your_size):
                return self.size_options[your_size]
            print("Size out of stock")
        except KeyError:
            print("Size does not exist")

    def is_available(self, your_size):
        """
        Check if a size is available

        Args:
            your_size: your desired size
        """
        size_button = self.size_options[your_size]
        out_of_stock = size_button.get_attribute("disabled")
        if out_of_stock:
            return False
        return True

    def add_to_cart(self, size_button):
        """
        Select size and add to cart
        Check if item is added through cart-item count, if not keep trying to add

        Args:
            size_button: size button element
        """
        add_to_cart = self.browser.find_element_by_css_selector("button[aria-label='Add to Cart']")
        item_added = False
        while not item_added:
            mouse = ActionChains(self.browser)
            mouse.click(size_button).click(add_to_cart).perform()
            """
            For some reason, could not use element.text to retrieve text 
            from cart span => use execute_script() to call js script instead 
            through attribute .textContent
            """
            item_count = self.browser.execute_script("return document.querySelector('span.cart-jewel').textContent")
            # Default is 0, if item added, this will change and stop loop
            if item_count != '0':
                item_added = True

    def click_when_avaialble(self, css_selector):
        WebDriverWait(self.browser, 10).until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        ).click()

    def fillout_billing_info(self):
        # FILLING IN STATES DROPDOWN
        states = Select(self.browser.find_element_by_id("state"))
        states.select_by_visible_text(self.STATE)

        # FILLING IN ADDRESS FORMS
        mouse = ActionChains(self.browser)

        # Find according fields to enter information
        first_name =self.browser.find_element_by_id("firstName")
        last_name =self.browser.find_element_by_id("lastName")
        address1 =self.browser.find_element_by_id("address1")
        address2 =self.browser.find_element_by_id("address2")
        city =self.browser.find_element_by_id("city")
        postal_code =self.browser.find_element_by_id("postalCode")
        email =self.browser.find_element_by_id("email")
        phone_number =self.browser.find_element_by_id("phoneNumber")

        mouse.send_keys_to_element(first_name, self.FIRST_NAME)
        mouse.send_keys_to_element(last_name, self.LAST_NAME)
        mouse.send_keys_to_element(address1, self.ADDRESS1)
        mouse.send_keys_to_element(address2, self.ADDRESS2)
        mouse.send_keys_to_element(city, self.CITY)
        mouse.send_keys_to_element(postal_code, self.POSTAL_CODE)
        mouse.send_keys_to_element(email, self.EMAIL)
        mouse.send_keys_to_element(phone_number, self.PHONE_NUMBER)
        mouse.perform()

    def submit(self):
        self.browser.find_element_by_css_selector("button[type='submit']").click()


jordan = Scraper()
jordan.go_to_product("https://www.nike.com/t/lebron-17-basketball-shoe-6LSXgh/BQ3177-601")
jordan.get_sizes()
size = jordan.choose_size('M 3.5 / W 5')
jordan.add_to_cart(size)
jordan.go_to_cart()
jordan.click_when_avaialble("button[data-automation='go-to-checkout-button']")
jordan.click_when_avaialble("button[data-automation='guest-checkout-button']")
jordan.click_when_avaialble("a[id='addressSuggestionOptOut']")
jordan.click_when_avaialble("button[aria-controls='address2']")
jordan.fillout_billing_info()
jordan.submit()

