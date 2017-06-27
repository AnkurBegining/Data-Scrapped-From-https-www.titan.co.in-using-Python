from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd

# Url from which i will scrap my data
myUrl = "https://www.titan.co.in/shop-online/watches/titan"

'''OPENING THE CONNECTION and GRABBING THE PAGE'''

# Open the website and grap inside my script
openUrl = uReq(myUrl)

# Now i would like to see my graped site
page_html = openUrl.read()

# As it is open connection i need to close it
openUrl.close()

# Make CSV file for data scrapped
fileName = "Product.csv"
f = open(fileName, 'w')
header = "Model Number, Brand, Gender, Function, Sub Function, Movement, Dial Color, Strap Color, Strap Material, " \
         "Glass Material, " \
         "Product, Case Shape, Case Material, Case Thickness, Case length, Case Width, Lock Mechanism, " \
         "Water Resistance, Warranty Period, Short Description, " \
         "Active Image, First Side Image, Second Side Image, Third Side Image, " \
         "Fourth Side Image \n "
f.write(header)

'''HTML PARSING'''

# Parse html
page_soup = soup(page_html, 'html.parser')
print(page_soup.h1)

# Grab all products
containers = page_soup.find_all("div", {"class": "product"})
print("Number of watches found:: ", len(containers))

newUrl = []
m = 0
for contains in containers:
    brand = contains.div.a.img['title']
    productDetailsContainer = contains.find('div', {'class': 'prodDetails'})
    product_name = productDetailsContainer['data-title']
    product_old_price = productDetailsContainer['data-oldprice']
    product_new_price = productDetailsContainer['data-newprice']
    product_page_link_container = contains.find('a', {'class': 'product_page_link'})
    product_detail_url = product_page_link_container['href']
    newUrl.append(myUrl + product_detail_url)

    print(newUrl[m])

    openurl = uReq(newUrl[m])
    pageHtml = openurl.read()
    openurl.close()
    pageSoup = soup(pageHtml, 'html.parser')

    # Model Number
    ContainersForModel = pageSoup.find('p', {'class': 'stock'}).getText()
    ModelNumber = ContainersForModel.strip()
    PrefectModelNumber = ModelNumber[1:ModelNumber.index(')')]
    f.write(PrefectModelNumber + ",")

    # Specification Of product
    ContainerForEachSpecification = pageSoup.find_all('div', {'class': 'each-spec clearfix'})
    # print(ContainerForEachSpecification)


    for contains in ContainerForEachSpecification:

        Conatiner = contains.find('p', {'class': 'value'}).getText()

        if Conatiner == "":
            f.write("Null" + ",")
        else:
            f.write(Conatiner + ",")

    ContainersForDescription = pageSoup.find('p', {'class': 'title'}).getText()
    f.write(ContainersForDescription + ",")

    # Containers For Image
    ContainersForImage = pageSoup.find_all('li', {'class': 'thumbnail_image'})

    for contains in ContainersForImage:
        Image = contains.img['src']
        f.write(Image + ",")
    f.write("\n")

    m = m + 1

print("Ankur")
