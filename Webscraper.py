from bs4 import BeautifulSoup
import requests

url = "https://www.yelp.com/search?find_desc=Tacos&find_loc=Fresno%2C%20CA&sortby=rating&start=0"

result = requests.get(url)
soup = BeautifulSoup(result.text, 'html.parser')

with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\main.txt', 'w', encoding='utf-8') as main_file:
    main_file.write(str(soup.prettify()))