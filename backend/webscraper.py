import threading
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from unidecode import unidecode
import csv

# debug = False
debug = True

# Dictionary to store results
results_dict = {}
lock = threading.Lock()

tags = ["Technology","World","U.S.","Business"]
urls = [
    "3M",
    "American Express",
    "Amgen",
    "Apple",
    "Boeing",
    "Caterpillar",
    "Chevron",
    "Cisco Systems",
    "Coca-Cola",
    "Dow Inc.",
    "Goldman Sachs",
    "The Home Depot",
    "Honeywell",
    "IBM",
    "Intel",
    "Johnson & Johnson",
    "JPMorgan Chase",
    "McDonald's",
    "Merck",
    "Microsoft",
    "Nike",
    "Procter & Gamble",
    "Salesforce",
    "The Travelers Companies",
    "UnitedHealth Group",
    "Verizon",
    "Visa",
    "Walmart",
    "The Walt Disney Company"
]

def scrape_tag(tag):
    for url in urls:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Set Chrome to run in headless mode
        page_url = f'https://www.nytimes.com/search?dropmab=false&endDate=2016-12-31&query={url}&sections={tag}%7Cnyt%3A%2F%2Fsection%2F4224240f-b1ab-50bd-881f-782d6a3bc527&sort=newest&startDate=2006-01-01'
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(page_url)

        
        # Function to click the "Show More" button
        def click_show_more():
            for _ in range(200):
                try:
                    show_more_button = driver.find_element(By.XPATH, "//button[@data-testid='search-show-more-button']")
                    # driver.execute_script("arguments[0].scrollIntoView();", show_more_button)  # Scroll to the button
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    driver.execute_script("arguments[0].click();", show_more_button)  # Click the button
                except Exception as e:
                    print(f"An exception occurred: {e}")
                    break

        click_show_more()
        
        title_results = driver.find_elements(By.CLASS_NAME, "css-2fgx4k")
        data_results = driver.find_elements(By.CLASS_NAME, "css-17ubb9w")
        abstract_results = driver.find_elements(By.CLASS_NAME, "css-16nhkrn")

        for title_result, data_result, abstract_result in zip(title_results, data_results, abstract_results):
            title = title_result.text
            data = data_result.text
            abstract = abstract_result.text
            company = url
            with lock:
                if url not in results_dict:
                    results_dict[url] = []
                results_dict[url].append([data, title, abstract])
            if debug:
                print("-------------------------------------------------------")
                print(company)
                print(title)
                print(data)
                print(abstract)
                print("-------------------------------------------------------")

        driver.quit()

def main():
    threads = []
    for tag in tags:
        t = threading.Thread(target=scrape_tag, args=(tag,))
        threads.append(t)
        t.start()
        

    for thread in threads:
        thread.join()

    def remove_accents(text):
        return unidecode(text)

    unique_results = set()  # Set to store unique results

    with open('news.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Company', 'Date', 'Title', 'Abstract'])
        for company, results in results_dict.items():
            for result in results:
                company_without_accents = remove_accents(company)
                date_without_accents = remove_accents(result[0])
                title_without_accents = remove_accents(result[1])
                abstract_without_accents = remove_accents(result[2])
                # Check if result is unique
                unique_result_key = (company_without_accents, date_without_accents, title_without_accents, abstract_without_accents)
                if unique_result_key not in unique_results:
                    # Write to CSV if it's unique
                    writer.writerow([company_without_accents, date_without_accents, title_without_accents, abstract_without_accents]) 
                    unique_results.add(unique_result_key)  # Add to set of unique results

    

if __name__ == "__main__":
    main()
    print('Finished')