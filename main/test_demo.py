from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup  
import requests  
import pandas as pd 

URL = "https://lostore.vn/"
# listOfMainProduct = ["MÀU VẼ", "GIẤY VẼ", "BÚT VẼ, CỌ VẼ", "PHÁC THẢO", "THỦ CÔNG (DIY)", "DỤNG CỤ BỔ TRỢ", "VĂN PHÒNG PHẨM", "TÚI VẢI CANVAS"]
listOfMainProduct = ["GIẤY VẼ"]


with sync_playwright() as p:
    
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    browser.start_tracing

    # Navigate to the URL
    page.goto(URL, wait_until='load')
    print('Page loaded')

    # Click main Menu
    for value in listOfMainProduct:
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, 0)")
        mainProductItem = page.locator(f"//ul[@class='list-menu vertical-menu-list']/.//a[@title='{value}']")
        print("[ MAIN PRODUCT: " + mainProductItem.inner_text().upper() + "]")
        mainProductItem.hover()

        # click each category of main menu
        elementOfMainMenu = (f"//ul[@class='list-menu vertical-menu-list']/.//a[@title='{value}']/..//li[@class='tp_menu_item child-item']")
        countSelector = page.locator(elementOfMainMenu).count()
        for indexCategory in range(0, countSelector):
            page.wait_for_timeout(2000)
            selectorToBeClick = page.wait_for_selector(elementOfMainMenu+(f"[{indexCategory + 1}]"))
            selectorToBeClick.focus()
            print("\nCLICK ON Category: " + selectorToBeClick.inner_text())
            selectorToBeClick.click()
            page.wait_for_timeout(1000)

            # click each item of category
            elementOfItemCategory = "//div[@class='product-list']/..//li[@class='item_product ivt']"
            countItem = page.locator(elementOfItemCategory).count()
            for indexItem in range(0, countItem):
                page.wait_for_timeout(2000)
                itemToBeClick = page.wait_for_selector(elementOfItemCategory+(f"[{indexItem + 1}]"))
                itemToBeClick.focus()
                print("\nclick on item: " + itemToBeClick.inner_text())
                page.wait_for_timeout(1000)
                itemToBeClick.click()

                #Get element of table
                pageUrl = page.url
                webpage = requests.get(pageUrl)  
                soup = BeautifulSoup(webpage.content, "lxml") 

                # Get Table html content and Name of product
                tableInfoData = soup.find("table", attrs={"class": 'ck-table-resized'})
                nameOfProductByHtml = soup.find("h1", attrs={"class":"product-title tp_product_detail_name"})
                nameOfProduct = nameOfProductByHtml.getText().strip()
                print("Table html:" + str(tableInfoData))
                print("Name Of Product :" + nameOfProduct)

                # Data to store content
                data = []

                data.append([nameOfProduct, tableInfoData])
                dataFrame = pd.DataFrame(data, columns=["Name Of Product", "Table Info"])

                try:
                    dataFrameExisting = pd.read_excel("data.xlsx")
                    dataFrame = pd.concat([dataFrameExisting, dataFrame], ignore_index=True)
                except FileNotFoundError:
                    pass

                # Save DataFrame
                dataFrame.to_excel("data.xlsx", index=False)

                print("Data saved to excel file successfully!")


                page.wait_for_timeout(2000)
                page.go_back()
                # page.wait_for_timeout(2000)
                # page.evaluate("window.scrollTo(0, 0)")

            # Back to main menu
            page.go_back()
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, 0)")
            # mainProductItem.wait_for(state="visible")
            page.wait_for_selector(f"//ul[@class='list-menu vertical-menu-list']/.//a[@title='{value}']")
            mainProductItem.hover()
            

    
        # Wait for navigation
    page.wait_for_timeout(1000)

    # Close the browser
    browser.close()
    print('Browser closed')

# def selectToItemOfCategory(value):
#     elementOfMainProduct = (f"//ul[@class='list-menu vertical-menu-list']/.//a[@title='{value}']/..//li[@class='tp_menu_item child-item']")
#     countSelector = page.locator(elementOfMainProduct).count()
#     for i in range(0, countSelector):
#         page.wait_for_timeout(2000)
#         selectorToBeClick = page.wait_for_selector(elementOfMainProduct+(f"[{i+1}]"))
#         print("click on: " + selectorToBeClick.inner_text())
#         selectorToBeClick.click()
#         page.go_back()
#         page.wait_for_timeout(2000)
#         page.evaluate("window.scrollTo(0, 0)")
#         # mainProductItem.wait_for(state="visible")
#         page.wait_for_selector(f"//ul[@class='list-menu vertical-menu-list']/.//a[@title='{value}']")
#         mainProductItem.hover()
 