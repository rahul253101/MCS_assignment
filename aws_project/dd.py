from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

def scrape_quotes(page):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Remote(command_executor='http://<selenium_grid_ip>:4444/wd/hub',
                              options=chrome_options)  # Replace <selenium_grid_ip> with the IP address of your Selenium Grid hub
    driver.get(f"http://quotes.toscrape.com/page/{page}")
    quotes = []

    for i in range(1, 11):
        quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
        author_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"
        quote_element = driver.find_element(By.XPATH, quote_xpath)
        quote_text = quote_element.text
        author_element = driver.find_element(By.XPATH, author_xpath)
        author_name = author_element.text
        print("Quote:", quote_text)
        print("Author:", author_name)
        print("quote_id:", page * 10 + i)
        print()
        # quotes.append({
        #     'quote_id': (page - 1) * 10 + i,
        #     'quote': quote_text,
        #     'author': author_name
        # })

    driver.quit()
    # return quotes

if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mcs_assignment']
    collection = db['quotes']

    total_pages = 10

    with ThreadPoolExecutor(max_workers=total_pages) as executor:
        all_quotes = executor.map(scrape_quotes, range(1, total_pages + 1))

    # flattened_quotes = [quote for page_quotes in all_quotes for quote in page_quotes]

    # collection.insert_many(flattened_quotes)
