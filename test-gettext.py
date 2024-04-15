from playwright.sync_api import sync_playwright

URL = "https://lostore.vn/co-ve-pc428294.html?page=1"

with sync_playwright() as p:
    
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    browser.start_tracing

    # Navigate to the URL
    page.goto(URL, wait_until='load')
    print('Page loaded')
    locatorOfPaging = "//div[@class='paginator']/..//a"
    text = page.locator(locatorOfPaging)
    countItem = text.count()
    print(countItem)
    for indexItem in range(0, countItem):
        page.wait_for_timeout(2000)
        itemToBeClick = page.wait_for_selector(locatorOfPaging+(f"[{indexItem + 1}]"))
        itemToBeClick.focus()
        print("\nclick on item: " + itemToBeClick.inner_text())
    # text.focus()
    print(text.text_content())

    # Wait for navigation
    page.wait_for_timeout(1000)

    # Close the browser
    browser.close()
    print('Browser closed')