from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup  
import requests  
import pandas as pd 
from unidecode import unidecode

URL = "https://lostore.vn/"
# listOfMainProduct = ["MÀU VẼ", "GIẤY VẼ", "BÚT VẼ, CỌ VẼ", "PHÁC THẢO", "THỦ CÔNG (DIY)", "DỤNG CỤ BỔ TRỢ", "VĂN PHÒNG PHẨM", "TÚI VẢI CANVAS"]
listOfMainProduct = ["GIẤY VẼ"]

#Xpath of element
mainMenuElement = "//ul[@class='list-menu vertical-menu-list']/.//a[@title='{}']"
categoryOfProductElement = "//ul[@class='list-menu vertical-menu-list']/.//a[@title='{}']/..//li[@class='tp_menu_item child-item']"
itemOfCategoryElement = "//div[@class='product-list']/..//li[@class='item_product ivt']"


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
        mainProductItem = page.locator(mainMenuElement.format(value))
        print("[ MAIN PRODUCT: " + mainProductItem.inner_text().upper() + "]")
        mainProductItem.hover()

        # click each category of main menu
        categoryOfProduct = (categoryOfProductElement.format(value))
        countSelectorOfCategory = page.locator(categoryOfProduct).count()
        for indexCategory in range(0, countSelectorOfCategory):
            page.wait_for_timeout(2000)
            selectorToBeClick = page.wait_for_selector(categoryOfProduct+(f"[{indexCategory + 1}]"))
            selectorToBeClick.focus()
            print("\nCLICK ON Category: " + selectorToBeClick.inner_text())
            selectorToBeClick.click()
            page.wait_for_timeout(1000)

            # click each item of category
            countItem = page.locator(itemOfCategoryElement).count()
            for indexItem in range(0, countItem):
                page.wait_for_timeout(2000)
                itemToBeClick = page.wait_for_selector(itemOfCategoryElement+(f"[{indexItem + 1}]"))
                itemToBeClick.focus()
                print("\nclick on item: " + itemToBeClick.inner_text())
                page.wait_for_timeout(1000)
                itemToBeClick.click()

                #Get html of table
                pageUrl = page.url
                webpage = requests.get(pageUrl)  
                soup = BeautifulSoup(webpage.content, "lxml") 

                # Get Table html content and Name of product
                tableInfoData = soup.find("table", attrs={"class": 'ck-table-resized'})
                nameOfProductByHtml = soup.find("h1", attrs={"class":"product-title tp_product_detail_name"})
                nameOfProduct = nameOfProductByHtml.getText().strip()
                nameOfAttribute = soup.find("p", attrs={"class":"type-attr"})
                linkOfPicture = soup.find("div", attrs={"class":"tab-main-content"}) 
                aliasOfProduct = unidecode(nameOfProduct).replace(" - ","-").replace(" ", "-").replace("_","-").replace(",","-").replace(".","-")

                textOfTag = []
                if nameOfAttribute:
                    for aTag in nameOfAttribute.find_all('a'):
                        textOfTag.append(aTag.get_text().strip())
                        print("Attribute of product: " + str(textOfTag))
                else:
                    print("no element found for attribute of product")

                listLinkOfPicture = []
                if linkOfPicture:
                    for aTag in linkOfPicture.find_all('img'):
                        imgUrl = aTag.get('src')
                        listLinkOfPicture.append(imgUrl)
                        print(imgUrl)
                else:
                    print("no element found for attribute of product")
                allLinkOfPicture = ",\n".join(listLinkOfPicture)

                print("Table html:" + str(tableInfoData))
                print("Name Of Product :" + nameOfProduct)

                # Data to store content
                data = {'Duong Dan SP/Alias': [aliasOfProduct] * len(textOfTag),
                        'Ten San Pham': [nameOfProduct if idx == 0 else '' for idx in range(len(textOfTag))],
                        'Noi Dung': [tableInfoData if idx == 0 else '' for idx in range(len(textOfTag))],
                        'Thuoc Tinh': textOfTag,
                        'Link Hinh San Pham': [allLinkOfPicture if idx == 0 else '' for idx in range(len(textOfTag))]
                        }
                dataFrame = pd.DataFrame(data)
                try:
                    dataFrameExisting = pd.read_excel("data.xlsx")
                    dataFrame = pd.concat([dataFrameExisting, dataFrame], ignore_index=True)
                except FileNotFoundError:
                    pass

                # Save DataFrame to file
                dataFrame.to_excel("data.xlsx", index=False)

                print("Data saved to excel file successfully!")

                page.wait_for_timeout(2000)
                page.go_back()

            # Back to main menu
            logoElement = page.wait_for_selector("//div[@class='header-logo']")
            logoElement.click()
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_selector(mainMenuElement.format(value))
            mainProductItem.hover()
            

    
    # Wait for navigation
    page.wait_for_timeout(1000)

    browser.close()
    print('Browser closed')

 