from bs4 import BeautifulSoup
import requests

# The following retrieves HTML data from the first page of yelp search results for "Tacos"
# This section is run only once to retrieve the HTML and saved to a .txt file and 
# commented out to prevent making unnecessary requests to the website. 

# # url = "https://www.yelp.com/search?find_desc=Tacos&find_loc=Fresno%2C%20CA&sortby=rating&start=0"
# result = requests.get(url)
# soup = BeautifulSoup(result.text, 'html.parser')
# with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\main.txt', 'w', encoding='utf-8') as main_file:
#     main_file.write(str(soup.prettify()))
    
with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\main.txt', 'r', encoding='utf-8') as m1:
    main_1 = m1.read()


# print(main_1)     # This serves only to verify my main_1 functions as intended.

soup = BeautifulSoup(main_1, 'html.parser')



links = soup.find_all("a", class_ = "css-1hqkluu") # This finds the 10 search result urls in the main.txt file. I have found the first one for reference: <a class="css-1hqkluu" href="/biz/tacos-brunos-fresno?osq=Tacos" rel="noopener" target="_blank">

print(links)
        

