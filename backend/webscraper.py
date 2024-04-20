from selenium import webdriver 
from selenium.webdriver.common.by import By 
# from webdriver_manager.chrome import ChromeDriverManager 
# from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

title = [] 
data = []
urls = ["3M",
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
    "Walgreens Boots Alliance",
    "The Walt Disney Company"]

def main():
    counter = 1
    for url in urls:
        if (counter == 10): break

        page_url = f'https://www.nytimes.com/search?dropmab=false&endDate=2016-12-31&query={url}&sections=Technology%7Cnyt%3A%2F%2Fsection%2F4224240f-b1ab-50bd-881f-782d6a3bc527&sort=best&startDate=2006-01-01'
        driver = webdriver.Chrome()
        driver.get(page_url)
        title.append(driver.find_element(By.CSS_SELECTOR,"h4.css-2fgx4k").text)
        data.append(driver.find_element(By.CLASS_NAME,"css-17ubb9w").text)
        counter +=1
    print(data)
    print(title)
if __name__ == "__main__":
    main()