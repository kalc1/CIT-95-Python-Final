from bs4 import BeautifulSoup
import requests

url = ""

result = requests.get(url)
soup = BeautifulSoup(result, 'html.parser')

main_file = open('main.txt', 'w')
main_file = write(str(soup.prettify()))