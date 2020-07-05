from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
"""
***Need to further read about chrome profile and these options
=>>>> These were forked from Dinuduke github

Add some experimental options to increase efficiency
2 - block, 1 - allow, 0 - default
"""
prefs = {"profile.managed_default_content_settings.images":2,
         "profile.default_content_setting_values.notifications":2,
         "profile.managed_default_content_settings.stylesheets":2,
         "profile.managed_default_content_settings.cookies":2,
         "profile.managed_default_content_settings.javascript":1,
         "profile.managed_default_content_settings.plugins":1,
         "profile.managed_default_content_settings.popups":2,
         "profile.managed_default_content_settings.geolocation":2,
         "profile.managed_default_content_settings.media_stream":2,
         }
chrome_options.add_experimental_option('prefs', prefs)

browser = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\chromedriver.exe', options=chrome_options)

browser.get("https://www.nike.com/t/lebron-17-basketball-shoe-6LSXgh/BQ3177-601")

# find all divs that contains sizes
sizes = browser.find_elements_by_class_name('css-1gxjmmq')

"""
Look inside found divs in put to check for disabled class 
which are sizes that out of stock
"""
for size in sizes:
    size_display = size.find_element_by_tag_name('input')
    # if attribute 'disabled' exist means out out stock
    out_of_stock = size_display.get_attribute('disabled')
    if out_of_stock:
        print(f"{size.text} <= OUT OF STOCK")
    else:
        print(f"{size.text}")
