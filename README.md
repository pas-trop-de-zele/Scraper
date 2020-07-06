First project simple sneaker web scraper

Initially was going to use requests, bs4 but foundout that for pages that use js to load need to use selenium instead to stimulate browser activity. Requests does not work since it does not load those elements, also could not find api call)

Successful in scraping but will need to find a different method prolly with regex since for some products, shoe size div has a different class. Also, need to speed up selenium, since this wouldn't be too competitive in buying fast

Added some optimization such as disable js, pictures, plugins, etc. Would need to further investigate chrome profile and how it works since

Added option to for user to select size, program would add to cart
New issue arise when looking for checking out button "STALEELEMENT EXCEPTION"