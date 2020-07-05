from selenium import webdriver

browser = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\chromedriver.exe')

browser.get("https://www.nike.com/t/lebron-17-basketball-shoe-6LSXgh/BQ3177-601")

# find all divs that contains sizes
sizes = browser.find_elements_by_class_name('css-1gxjmmq')
# Look inside found divs in put to check for disabled class 
# which are sizes that out of stock
for size in sizes:
    size_display = size.find_element_by_tag_name('input')
    out_of_stock = size_display.get_attribute('disabled')
    if out_of_stock:
        print(f"{size.text} <= OUT OF STOCK")
    else:
        print(f"{size.text}")
