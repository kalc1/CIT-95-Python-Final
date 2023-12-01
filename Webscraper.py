from bs4 import BeautifulSoup
import requests
import os

output_directory = 'c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html'
os.makedirs(output_directory, exist_ok=True) # Since I have to run this a few times for testing an OSError will be raised if its value is False, so this is set to True

# The following retrieves HTML data from the first page of yelp search results for "Tacos"
# This section is run only once to retrieve the HTML and saved to a .txt file and 
# commented out to prevent making unnecessary requests to the website. 

# url = "https://www.yelp.com/search?find_desc=Tacos&find_loc=Fresno%2C%20CA&sortby=rating&start=0"
# result = requests.get(url)
# soup = BeautifulSoup(result.text, 'html.parser')
# with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\main.txt', 'w', encoding='utf-8') as main_file:
#     main_file.write(str(soup.prettify()))

try:    # Exception Handling will let me know if the file doesn't exist. This issue kept happening for some reason so this will let me know immediately if it happens again. 
    with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\main.txt', 'r', encoding='utf-8') as m1:
        main_1 = m1.read()
except FileNotFoundError:
    print("File not found: c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\main.txt")

# print(main_1)     # This serves only to verify my main_1 functions as intended.

main_soup = BeautifulSoup(main_1, 'html.parser')

# This finds the 10 search result urls in the main.txt file. I have found the first one for reference: <a class="css-1hqkluu" href="/biz/tacos-brunos-fresno?osq=Tacos" rel="noopener" target="_blank">
links = main_soup.find_all("a", class_ = "css-1hqkluu") 

# These 3 lines of code just serve to show what I have extracted from the soup.find_all function above
# print(links) 
# for link in links:
#     print(link['href'])


# This creates a new file named links.txt which will be used to store a list of links extracted from main.txt and to provide a way to go directly to the site for ease of convenience. 
# As above, this is only run once to retrieve the links from main.txt and uses exception handling.
try:    
    with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\links.txt', 'w', encoding='utf-8') as links_file:
        for link in links:  # This extracts all the links to the taco places in the first page search results from the main url
            taco_place = 'https://www.yelp.com' + link['href']
            links_file.write(f'{taco_place}\n')
except Exception as e:  # The use of 'Exception' is used to catch any errors during the process
    print("An error occurred while writing links to: c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\links.txt")
        

