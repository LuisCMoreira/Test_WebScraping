import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dbInputEGs import insert_to_mongodb
from dbInputEGs import insert_to_mysql


# Search information - specific to the site url and page structure
search_cat = "site category path"
search_words = "q-word1-word2"
top_price="100"
page="page=1&" # "" for null and "page=2&"

# Define the number of pages to scrape
total_pages = 3  # Change this to the number of pages you want to scrape


def scrape_web_products():

    for page_number in range(1, total_pages + 1):
        # Construct the URL with pagination
        page = f"page={page_number}&"
        url = f"https://www.someSite.pt/{search_cat}/{search_words}/?{page}search%5Bfilter_float_price:to%5D={top_price}"

        response = requests.get(url)

        if response.status_code != 200:
            print("Failed to fetch the page. Check the URL or website availability.")
            return

        soup = BeautifulSoup(response.content, "html.parser")

        # Replace the CSS selector with the correct one for individual product elements
        product_elements = soup.select("div[data-cy='l-card']")

        for product_element in product_elements:
            # Within each product element, extract and print the product characteristic (find elements by page inspection)
            name_element = product_element.select_one("h6.css-16v5mdi.er34gjf0")
            price_element = product_element.select_one("p.css-10b0gli.er34gjf0")
            location_element = product_element.select_one("p.css-veheph.er34gjf0")        


            name = name_element.text.strip() if name_element else "N/A"
            price = price_element.text.strip() if price_element else "N/A"
            if price != "N/A":
                price_parts=price.split(" €")
                price=price_parts[0]

                
                
            location = location_element.text.strip() if price_element else "N/A"
            if location != "N/A":
                location_parts=location.split(" - ")
                location =location_parts[0]
                updated_at = location_parts[1]

            # Create a custom schema
            custom_schema = {
                "item":{
                    "name": name,
                    "price": price,
                    "location": location
                },
                "updated_at": updated_at,
                "timestamp": datetime.now()
            }

            # Uncomment to input to MongoDB
            #insert_to_mongodb("someColection", "someDB",custom_schema, mongodb_uri="mongodb://localhost:27017/")

            # Uncomment to input to mySQL
            #insert_to_mysql("localhost", "user", "pass", "database", custom_schema)
            
            print(f"Inserted Record from page {page_number}:", custom_schema)
            print("=" * 60)

if __name__ == "__main__":
    scrape_web_products()