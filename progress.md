First project simple sneaker web scraper process log

07/04/20
Initially was going to use requests, bs4 but foundout that for pages that use js to load need to use selenium instead to stimulate browser activity. Requests does not work since it does not load those elements, also could not find api call)

Successful in scraping but will need to find a different method prolly with regex since for some products, shoe size div has a different class. Also, need to speed up selenium, since this wouldn't be too competitive in buying fast

07/05/20
Added some optimization such as disable js, pictures, plugins, etc. Would need to further investigate chrome profile and how it works since

07/06/20
Added option to for user to select size, program would add to cart
New issue arise when looking for checking out button "STALEELEMENT EXCEPTION"
=> turns out stale element is resolved when declare a new ActionChains object after going to a new URL => waiting to verify reason on Stackoverflow

07/07/20
Got to checkout site and filling out forms, need to find out how to select options from a dropdown

07/08/20
Add waiting for method to be clickable for a few items instead of pausing for some seconds
=> Need to work on how to find text within the cart items count in order to verify that item was added to cart
=> for some reason element.text does not return text instead undefined,
However, calling js script may work

07/09/20
=> Successfully use .execute_script() to retrieve inner text showing
numbers of item in cart