from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def cleanPrice(x):
    bad = " |,–$"
    for char in bad:
        x = x.replace(char, "")
    return x


# variables
myURL = 'https://www.newegg.com/p/pl?Submit=StoreIM&Depa=1&Category=38&PageSize=96'
tempURL = ''
filename = 'graphicsCards.csv'
header = 'brand, price, rebated_price, product_name, shipping\n'
print(myURL)

# getting the html information
uClient = uReq(myURL)                   # open connection
pageHTML = uClient.read()               # put content in variable
uClient.close()                         # close the connetion

pageS = soup(pageHTML, 'html.parser')   # parse html

# grabbing all the products on page
gContainers = pageS.findAll('div', {'class': 'item-container'})

print('number of products:', len(gContainers))

# opening file
f = open(filename, 'w')
f.write(header)

g = open('src.txt', 'w')
g.write(str(gContainers))
g.close()

h = open('cardInfoHTML.txt', 'w')

# loop through all the products/ grab info
for container in gContainers:
    # entering prodcut page for each result
    tempURL = container.find('a', {'class': 'item-title'})['href']
    tempClient = uReq(tempURL)
    tempHTML = tempClient.read()
    tempClient.close()
    pageT = soup(tempHTML, 'html.parser')
    # info container
    infoContain = pageT.find('div', {'id': 'detailSpecContent'})
    # chipset = infoContain.find(
    #     'a', {'data-t-e-var78': 'Specification Popup:GPU'})
    # chipInfo = chipset.parent
    # print('chip info:', chipInfo)
    # h.write(str(infoContain))

    # grab variables
    title = container.a.img['title']
    brand = container.find('div', {'class': 'item-branding'}).img['title']
    shipping = container.find(
        'li', {'class': 'price-ship'}).getText('', strip=True)
    priceContainer = container.find('li', {'class': 'price-current'})
    price = cleanPrice(priceContainer.getText('', strip=True))
    rebate = ''
    if (container.find(
            'span', {'class': 'price-note-dollar'})):
        rebate = container.find(
            'span', {'class': 'price-note-dollar'}).getText()

    # print to console
    # print('\n************************************************************************************************************************************************************************')
    # print('title:', title)
    # print('brand:', brand)
    # print('price:', price)
    # print('rebated:', rebate)
    # print('shipping:', shipping.strip('Shipping'))
    # print('temp URL:', tempURL)

    # write to file
    f.write(brand + ',' + price.replace(',', ';') + ',' + rebate.replace(',', '') + ',' + title.replace(',', '|') +
            ',' + shipping.strip('Shipping') + '\n')

f.close()
h.close()
print('\n_______________________________________________the code has worked_______________________________________________\n')
