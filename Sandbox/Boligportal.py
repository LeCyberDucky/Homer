from bs4 import BeautifulSoup as bs
import requests
import time
import random

### Settings ###
base_URL = "https://www.boligportal.dk/lejeboliger/k%C3%B8benhavn/"
sleep_time_range = (10, 20)
result_step_size = 10

### Initial scrape
page = requests.get(URL)
soup = bs(page.content, "html.parser")
number_of_results = int(soup.find("span", class_ = "css-1rz49ey").text.split()[0])
time.sleep(random.uniform(*sleep_time_range))

### Obtaining links to all available apartments
apartment_links = set()
seen_results = 0
while (seen_results < number_of_results):
    print("Scraping apartments!")
    URL = base_URL + f"?offset={seen_results}"
    page = requests.get(URL)
    soup = bs(page.content, "html.parser")
    apartment_links.update(get_apartment_links(soup))
    seen_results += result_step_size
    time.sleep(random.uniform(*sleep_time_range))

apartment_links = list(apartment_links)

# Parse apartment
# Title
# Address
# Insertion date
# Availability date
# Price
# Detail tables
# Description
# Images

apartment_URL = apartment_links[0]
apartment_URL
apartment = requests.get(apartment_URL)
soup = bs(apartment.content, "html.parser")
title = soup.find("span", class_ = "css-yhs3uk").text
(ad_date, address) = [element.text for element in soup.find_all("div", class_ = "css-1bbi9fj")[0:2]]

info_box = soup.find("div", class_ = "css-wi20xz")
price = int(info_box.find("span", class_ = "css-goiemm").text.strip().replace('.', ''))
(aconto, move_in_price, duration) = [element.text for element in info_box.find_all("span", class_ = "css-v9pymm")[0:3]]
aconto = int(aconto.split()[0])
move_in_price = int(move_in_price.split()[0].replace('.', ''))
move_in_date = info_box.find("span", class_ = "css-z58ebh").text

# Description title and description
description = soup.find("div", class_ = "css-ysv6ho")
description_title = description.find("h3", class_ = "css-1hg8deg").text
description_content = description.find("div", class_ = "css-1f7mpex").text

# Details
detail_boxes = soup.find("div", class_ = "css-11rix5h")

detail_boxes_contents = detail_boxes.find_all("div", class_ = ["temporaryFlexColumnClassName", "css-etn5cp"])
details = {}

for detail in detail_boxes_contents:
    (measure, value) = [element.text for element in detail.find_all("span")[0:2]]
    details[measure] = value

# Images
images = soup.find("div", class_ = "css-vxonxb").find_all("img")
images = [image["data-flickity-lazyload-src"].split("?")[0] for image in images]




def get_apartment_links(soup):
    apartment_column = soup.find_all("div", class_ = "css-16jggh1")[0]
    apartment_column = apartment_column.find("div", class_ = "css-ho2tek")
    apartments = apartment_column.find_all("a", class_ = "AdCardSrp__Link css-1gsgxxt")
    apartment_links = ["https://www.boligportal.dk" + apartment["href"] for apartment in apartments]
    return apartment_links