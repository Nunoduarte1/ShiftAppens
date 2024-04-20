from selenium import webdriver 
from selenium.webdriver.common.by import By 
# from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from unidecode import unidecode
import csv

# {{company, [date, title, abstract]}}
dict = {}

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
    # "Walgreens Boots Alliance", # shiftappens - empty page - won't work
    "Walmart",
    "The Walt Disney Company"
    ]

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Set Chrome to run in headless mode
    for url in urls:

        page_url = f'https://www.nytimes.com/search?dropmab=false&endDate=2016-12-31&query={url}&sections=Technology%7Cnyt%3A%2F%2Fsection%2F4224240f-b1ab-50bd-881f-782d6a3bc527&sort=best&startDate=2006-01-01'
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(page_url)
        
        results = driver.find_elements(By.CLASS_NAME, "css-2fgx4k")
        
        for result in results:
            title = result.text
            data = driver.find_element(By.CLASS_NAME, "css-17ubb9w").text
            abstract = driver.find_element(By.CLASS_NAME, "css-16nhkrn").text
            company = url
            # dict[title] = [data, abstract, company]
            # dict.update({company:[data,title,abstract]})
            if(url not in dict):
                dict[url] = []
            dict[url].append([data, title, abstract])
            print("-------------------------------------------------------")
            print(title)
            print(data)
            print(abstract)
            print(company)
            print("-------------------------------------------------------")

        driver.quit()

    
    def remove_accents(text):
        return unidecode(text)

    print(dict.items())
    with open('news.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Company', 'Date', 'Title', 'Abstract'])
        for company, results in dict.items():
            for result in results:
                company_without_accents = remove_accents(company)
                date_without_accents = remove_accents(result[0])
                title_without_accents = remove_accents(result[1])
                abstract_without_accents = remove_accents(result[2])
                writer.writerow([company_without_accents, date_without_accents, title_without_accents, abstract_without_accents]) 

if __name__ == "__main__":
    main()
    print('Finished')