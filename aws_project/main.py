import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

import time

# from webscrapping import driver


def scrape_quotes(page):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://quotes.toscrape.com")
    # page +=1
    # start_time = time.time()

    for i in range(1, 11):
        quote_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[1]"
        author_xpath = f"/html/body/div[1]/div[2]/div[1]/div[{i}]/span[2]/small"
        quote_element = driver.find_element(By.XPATH, quote_xpath)
        quote_text = quote_element.text
        author_element = driver.find_element(By.XPATH, author_xpath)
        author_name = author_element.text
        print("Page Number :",i)
        print("Quote:", quote_text)
        print("Author:", author_name)
        print("Page :", page)
        # print("quote_id:", page * 10 + i)
        print()
        document = {
            'quote_id': page * 10 + i,
            'quote': quote_text,
            'author': author_name
        }
        collection.insert_one(document)
    try:
                next_button = driver.find_element(By.XPATH, "//li[@class='next']/page")
                next_button.click()
    except:
                print("No more pages available. Exiting loop.")
                # if stop_thread.is_set():
                driver.quit()
end_time = time.time()

# break
if __name__ == "__main__":
    # stop_thread = threading.Event()
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mcs_assignment']
    collection = db['quotes']
    # start_time = time.time()
    # result =[]
    # values = [1,2,3,4,5,6,7,8,9,10]
    with ThreadPoolExecutor(max_workers=10) as exe:
        # exe.submit(scrape_quotes,2)

        # Maps the method 'cube' with a list of values.
        exe.map(scrape_quotes)

    # for r in result:
    #     print(r)


    # for page in range(1, 11):
    #     t = threading.Thread(target=scrape_quotes, args=(page,))
    #     # threads.append(t)
    #     t.start()


    # x = threading.Thread(target=scrape_quotes, args=((range(1,10)),))
    # x.start()
    # x.join()
    # stop_thread.set()

    # page_no = [i for i in range(1, 11)]
    # total_pages = 10

    # with ThreadPoolExecutor(max_workers=total_pages) as executor:
    #
    #     executor.map(scrape_quotes())

    # end_time = time.time()
    #
    # print(end_time-start_time)
    #
    # threading.Event()
    # x.is_alive()
    # driver.quit()
