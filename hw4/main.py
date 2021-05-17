#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

# URL to querry
# Make sure to have 'en' for English!
def main(URL):
    # Instantiate list to populate with data
    data = []

    # Instantiate a page count
    index = 1

    while True:

        with urlopen(URL + "/page-" + str(index)) as response:

            # Instantiate parser
            soup = BeautifulSoup(response, "html.parser")

            # Look for the last page
            # If got to the last page, break out of the loop
            last_page = soup.find("article", class_="main-article")

            # Class 'main-article' only exists on the last page
            # So a legit page with items will return None
            if last_page is not None:

                # If page says "No products found"
                # The last page has been reached
                if last_page.get_text().lstrip().rstrip() \
                        == "No products found":
                    break

            # Loop through list of 
            for item in soup.find_all("div", class_="offer-thumb__content"):
                print(item)
                # Get "buy now" price
                price = item.find("div", class_="offer-thumb__price--group")
                # If "buy now" price is unavailable, get "current bid" price
                if price is None:
                    price = item.find("div", class_="offer-thumb__price--current")
                if price is not None:
                    print("AAAAAAa")
                    data.append({
                        "Title": item.find("h3", class_="offer-thumb__title").find("a").get_text(),
                        "Price": price.get_text().replace(" ", ""),
                        "Picture href": item.find("a", class_="lazy").find("img").get("data-original"),
                    })
                # print(type(price))
                # Add data to the list

                # Increment index to get to the next page on next loop iteration
            index += 1

            # Save list as json
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)


if __name__ == "__main__":
    main("https://ordi.eu/lauaarvutid")
