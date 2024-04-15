from bs4 import BeautifulSoup  
import requests 
import pandas as pd 
  
# URL to the scraped 
URL = "https://lostore.vn/dao-doc-giay-mau-den-p38404347.html"
  
# getting the contents of the website and parsing them 
webpage = requests.get(URL)  
soup = BeautifulSoup(webpage.content, "lxml")
  
# getting the h1 with id as firstHeading and printing it
# tableInfoData = soup.find("table", attrs={"class": 'ck-table-resized'})
# nameOfProductByHtml = soup.find("h1", attrs={"class":"product-title tp_product_detail_name"})
nameOfAttribute = soup.find("p", attrs={"class":"type-attr"})
textOfTag = []
if nameOfAttribute:
  for aTag in nameOfAttribute.find_all('a'):
      textOfTag.append(aTag.text)
      print(textOfTag)
else:
   print("no element found")
    
# nameOfProduct = nameOfProductByHtml.getText().strip()
# print("Table html:" + str(tableInfoData))
# print("Name Of Product :" + nameOfProduct)



# Create an empty list to store data
# data = []

# data.append([nameOfProduct, tableInfoData])

# # Create DataFrame from list
# df = pd.DataFrame(data, columns=["Name Of Product", "Table Info"])

# try:
#   # Try to read existing data
#   df_existing = pd.read_excel("data.xlsx")
#   # Append new data to existing DataFrame
# #   df = df.append(df_existing, ignore_index=True)

#   df = pd.concat([df_existing, df], ignore_index=True)
# except FileNotFoundError:
#   # If file not found, use the created DataFrame
#   pass

# # Save DataFrame to excel file
# df.to_excel("data.xlsx", index=False)

# print("Data saved to excel file successfully!")













  
# # getting the text/content inside the h1 tag we  
# # parsed on the previous line 
# cont = title.get_text() 
# print(cont) 
  
# # getting the HTML of the parent parent of  
# # the h1 tag we parsed earlier 
# parent = soup.find("span",  
#                    attrs={"id": 'Machine_learning_approaches'}).parent() 
# print(parent)