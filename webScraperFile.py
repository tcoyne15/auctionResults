from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urlparse

url = "https://www.christies.com/auction/auction-22044-nyr/browse-lots"

# Extract the host from the URL
parsed_url = urlparse(url)
host = parsed_url.netloc

# Configure the WebDriver
driver_path = "/path/to/chromedriver"  # Replace with the actual path to the WebDriver executable
driver = webdriver.Chrome(executable_path=driver_path)  # Replace with the appropriate WebDriver class and path

# Navigate to the webpage
driver.get(url)

# Get the page source
page_source = driver.page_source

# Create a BeautifulSoup object from the page source
soup = BeautifulSoup(page_source, "html.parser")

qualifying_lots = []
non_qualifying_lots = []

lots = soup.find_all("div", class_="lot-details-container")
for lot in lots:
    estimate = lot.find("span", class_="estimate-value")
    price_realized = lot.find("span", class_="price-realized-value")
    if estimate and price_realized:
        estimate_price = float(estimate.text.strip().replace(",", "").replace("$", ""))
        price_realized_value = float(price_realized.text.strip().replace(",", "").replace("$", ""))
        if price_realized_value >= (5 * estimate_price):
            qualifying_lots.append(lot)
        else:
            non_qualifying_lots.append(lot)

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
