from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urlparse

THRESHOLD = 5
url = "https://www.christies.com/auction/auction-22044-nyr/browse-lots?loadall=true&page=2&sortby=lotnumber"

# Extract the host from the URL
parsed_url = urlparse(url)
host = parsed_url.netloc

#driver = webdriver.Firefox()  # Replace with the appropriate WebDriver class and path
opts = webdriver.FirefoxOptions()
opts.add_argument("-headless")
driver = webdriver.Firefox(options=opts)

# Navigate to the webpage
driver.get(url)
page_source = driver.page_source

# Create a BeautifulSoup object from the page source
soup = BeautifulSoup(page_source, "html.parser")

qualifying_lots = []
non_qualifying_lots = []

paintings = soup.find_all("div", class_="chr-lot-tile__content")
#chr-lot-tile__content to see if both realized and estimate exist

#lots = soup.find_all("div", class_="chr-lot-tile__price-container")

curRealized = None
curEstimate = None
title = None
artist = None

for painting in paintings:
    curRealized = painting.find("span", class_="chr-lot-tile__secondary-price-value")
    artist = painting.find("a", class_="chr-lot-tile__link").text.strip()
    #print(artist)

    title = painting.find("p", class_="chr-lot-tile__secondary-title").text.strip()
    #print(title)

    if curRealized:
        curRealized = curRealized.text
        curEstimate = painting.find("span", class_="chr-lot-tile__price-value").text
        parsedEstimate = curEstimate[curEstimate.find("-")+1:].strip()
        numberEstimate = int(parsedEstimate.replace(",", ""))
        parsedRealized = curRealized[curRealized.find("D")+1:].strip()
        numberRealized = int(parsedRealized.replace(",", ""))
        #print(parsedEstimate + ", " + parsedRealized)
        if numberEstimate * THRESHOLD <= numberRealized:
            qualifying_lots.append((title, artist))
        else:
            non_qualifying_lots.append((title, artist))
    else:
        non_qualifying_lots.append((title, artist))


# for lot in lots:
#     #loop throught paintings with another find call in here
#     if "chr-lot-tile__price-container--secondary" in lot["class"]:
#         curRealized = lot.find("span", class_="chr-lot-tile__secondary-price-value").text

#         parsedEstimate = curEstimate[curEstimate.find("-")+1:].strip()
#         numberEstimate = int(parsedEstimate.replace(",", ""))
#         parsedRealized = curRealized[curRealized.find("D")+1:].strip()
#         numberRealized = int(parsedRealized.replace(",", ""))
#         print(parsedEstimate + ", " + parsedRealized)
#         if numberEstimate * 5 <= numberRealized:
#             print("FOUND ONE")
#         continue
#     curEstimate = lot.find("span", class_="chr-lot-tile__price-value").text


print("Qualifying Lots:")
for lot in qualifying_lots:
    print(lot)
    print("-" * 64)

print("Number of Qualifying Lots:", len(qualifying_lots))
print("Number of Non-Qualifying Lots:", len(non_qualifying_lots))

# Close the WebDriver
driver.quit()