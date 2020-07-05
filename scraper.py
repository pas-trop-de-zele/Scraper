from selenium import webdriver

option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

browser = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\chromedriver.exe', chrome_options=option)

browser.get("https://www.nike.com/t/lebron-17-basketball-shoe-6LSXgh/BQ3177-601")

# find all divs that contains sizes
sizes = browser.find_elements_by_class_name('css-1gxjmmq')
# Look inside found divs in put to check for disabled class 
# which are sizes that out of stock
for size in sizes:
    size_display = size.find_element_by_tag_name('input')
    # if attribute 'disabled' exist means out out stock
    out_of_stock = size_display.get_attribute('disabled')
    if out_of_stock:
        print(f"{size.text} <= OUT OF STOCK")
    else:
        print(f"{size.text}")
