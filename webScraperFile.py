from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = "https://www.christies.com/auction/auction-22044-nyr/browse-lots?loadall=true&page=2&sortby=lotnumber"

# Extract the host from the URL
print("0")
parsed_url = urlparse(url)
host = parsed_url.netloc

driver = webdriver.Firefox()  # Replace with the appropriate WebDriver class and path

print("0.5")

# Navigate to the webpage
driver.get(url)
print("1")

# Get the page source
page_source = driver.page_source

# Create a BeautifulSoup object from the page source
soup = BeautifulSoup(page_source, "html.parser")
print("2")

qualifying_lots = []
non_qualifying_lots = []

paintings = soup.find_all("div", class_="chr-lot-tile__content")
#chr-lot-tile__content to see if both realized and estimate exist

lots = soup.find_all("div", class_="chr-lot-tile__price-container")

curRealized = None
curEstimate = None

for lot in lots:
    #loop throught paintings with another find call in here
    if "chr-lot-tile__price-container--secondary" in lot["class"]:
        curRealized = lot.find("span", class_="chr-lot-tile__secondary-price-value").text

        parsedEstimate = curEstimate[curEstimate.find("-")+1:].strip()
        numberEstimate = int(parsedEstimate.replace(",", ""))
        parsedRealized = curRealized[curRealized.find("D")+1:].strip()
        numberRealized = int(parsedRealized.replace(",", ""))
        print(parsedEstimate + ", " + parsedRealized)
        if numberEstimate * 5 <= numberRealized:
            print("FOUND ONE")
        continue
    curEstimate = lot.find("span", class_="chr-lot-tile__price-value").text


print("Qualifying Lots:")
for lot in qualifying_lots:
    print(lot.text.strip())
    print("-" * 50)

print("Non-Qualifying Lots:")
for lot in non_qualifying_lots:
    print(lot.text.strip())
    print("-" * 50)

print("Number of Qualifying Lots:", len(qualifying_lots))
print("Number of Non-Qualifying Lots:", len(non_qualifying_lots))

# Close the WebDriver
driver.quit()
