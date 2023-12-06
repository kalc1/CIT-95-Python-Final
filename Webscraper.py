from bs4 import BeautifulSoup
import requests
import os
import json
import csv

# First, os.makedirs() is used to create 2 folders/directories. One will house all the raw html data converted to .txt, and the other will contain the outputs. 
# Since I have to run this a few times for testing, an OSError will be raised if its value is False, so this is set to True. This is because the directory will already exist after the initial running of this code.
os.makedirs('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html', exist_ok=True) 
os.makedirs('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\output_files', exist_ok=True) 

# The following retrieves HTML data from the first page of yelp search results for "Tacos"
# This section is run only once to retrieve the HTML and saved to a .txt file and 
# It is commented out to prevent making unnecessary requests to the website:
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

# Beautifulsoup is used to parse the html in main_1
main_soup = BeautifulSoup(main_1, 'html.parser')

# This finds the 10 search result urls in the main.txt file. I have found the first one for reference: <a class="css-1hqkluu" href="/biz/tacos-brunos-fresno?osq=Tacos" rel="noopener" target="_blank">
links = main_soup.find_all("a", class_ = "css-1hqkluu") 

# These 3 lines of code just serve to show what I have extracted from the soup.find_all function above
# print(links) 
# for link in links:
#     print(link['href'])

# This creates a new file named links.txt which will be used to store a list of links extracted from main.txt and to provide a way to go directly to the site for ease of convenience. 
# As above, this also uses exception handling:
try:    
    with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\links.txt', 'w', encoding='utf-8') as links_file:
        for link in links:  # This extracts all the links to the taco places in the first page search results from the main url
            taco_place = 'https://www.yelp.com' + link['href']
            links_file.write(f'{taco_place}\n') # An escape character is used here to make the file more readable. I later end up removing '\n' when converting this to a list. 
except Exception as e:  # The use of 'Exception' is used to catch any errors during the process
    print("An error occurred while writing links to: c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\links.txt")

# This creates a list of the 10 links in links.txt and uses exception handling
try:
    with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\links.txt', 'r', encoding='utf-8') as links_txt:
        read_links = links_txt.readlines() 
except Exception as e:
    print("An error occurred while reading links from: c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\links.txt")

# The list from read_links above contains an escape character: '/n'
# The following block of code removes these and creates a new list:
links_list = []
for link in read_links:
    append_link = link.strip()
    links_list.append(append_link)
# print(links_list)  # This just used to verify it works as intended. 

# The following retrieves HTML data from each link in links_list 
# enumerate is used to iterate through each link in links_list and give each .txt file a unique name based on its index number
# This section is run only once to retrieve all the HTML and saved to 10 different .txt files and 
# It is commented out to prevent making unnecessary requests to the website:
# for i, link in enumerate(links_list):
#     link_result = requests.get(link)
#     link_soup = BeautifulSoup(link_result.text, 'html.parser')
#     with open(f'c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\taco_link_{i}.txt', 'w', encoding='utf-8') as taco_htmls:
#         taco_htmls.write(str(link_soup.prettify()))

# This is an empty list which will be appended with information from the iteration below.
export_data = []
# An output.txt file is created and iteration is used to write to it. 
with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\output_files\\output.txt', 'w', encoding='utf-8') as output: 
    output.write(f'The following data was scraped from the top 10 search results for "tacos" from yelp.\n\n')
    for i in range(10): # This iterates through taco_link_0.txt through taco_link_9.txt
        taco_html = f'c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html\\taco_link_{i}.txt'

        try:
            with open(taco_html, 'r', encoding='utf-8') as html:
                taco_contents = html.read()
                
            ### HTML parsing using Beautifulsoup ###
            taco_soup = BeautifulSoup(taco_contents, 'html.parser')
            
            # This finds the name of the restuarant. I have found the first one for reference: <h1 class="css-1se8maq">Tacos Brunos</h1>
            # The HTML structure for each taco_link_{i} should be the same so this scrapes the restaurant name from each of the files while stripping the white space.
            restaurant_name_element = taco_soup.find('h1', class_="css-1se8maq")
            if restaurant_name_element is not None:
                restaurant_name = restaurant_name_element.get_text(strip=True)
            else:
                restaurant_name = 'no data'
            
            # This finds the restaurant rating and how many reviews it has. HTML snippet for reference: <span class=" css-1fdy0l5" data-font-weight="semibold">5.0 </span>
            restaurant_rating_element = taco_soup.find('span', class_="css-1fdy0l5")
            if restaurant_rating_element is not None:
                restaurant_rating = restaurant_rating_element.get_text(strip=True)
            else:
                restaurant_rating = 'no data'        
            # This finds the number of reviews the restaurant has. HTML snippet: <a href="#reviews" class="css-19v1rkv">(9 reviews)</a>
            restaurant_review_count_element = taco_soup.find('a', class_="css-19v1rkv")
            if restaurant_review_count_element is not None:
                restaurant_review_count = restaurant_review_count_element.get_text(strip=True).strip('() reviews')
            else:
                restaurant_review_count = 'no data' 
                
            # This retrieves the website if available. Otherwise saves as 'no data'. HTML snippet for reference:       
            # <a href="/biz_redir?url=https%3A%2F%2Ffresnomexicanfood.com&amp;cachebuster=1701716554&amp;website_link_type=website&amp;src_bizid=-Ufu3Ha7V9Z6Z4YBx1yTfg&amp;s=91159ae84e4fd445df8daada241e54af990b8bf2bdc168212f103dcb02cdd4ad" 
            # class="css-1idmmu3" target="_blank" rel="noopener" role="link">fresnomexicanfood.com</a>
            restaurant_website_element = taco_soup.find('a', class_="css-1idmmu3", target="_blank")
            if restaurant_website_element is not None:
                restaurant_website = restaurant_website_element.get_text(strip=True)
            else:
                restaurant_website = 'no data'
            
            # Retrieving the phone numbers was tricky because the <p class="css-1p9ibgf"> contains both the website info and the phone number. 
            # A nested if-statement was used to make sure a phone number was being scraped rather than a website.
            # Websites were within a seperate <a class_="css-1idmmu3"> within the same <div> and <p>
            #<div class="css-djo2w"><div class="arrange__09f24__LDfbs gutter-2__09f24__CCmUo vertical-align-middle__09f24__zU9sE css-1qn0b6x">
            # <div class="arrange-unit__09f24__rqHTg arrange-unit-fill__09f24__CUubG css-1qn0b6x">
            # <p class=" css-na3oda">Phone number</p><p class=" css-1p9ibgf" data-font-weight="semibold">(559) 449-3331</p></div>
            # <div class="arrange-unit__09f24__rqHTg css-1qn0b6x"><span alt="" aria-hidden="true" role="img" class="icon--24-phone-v2 icon__09f24__zr17A css-147xtl9"><svg width="24" height="24" class="icon_svg"><path d="M13.59 23.07A7 7 0 0 1 8.64 21L3 15.36a7 7 0 0 1 0-9.9l1.39-1.41a1 1 0 0 1 1.42 0l5 5a1 1 0 0 1 0 1.41 2.001 2.001 0 0 0 2.83 2.83 1 1 0 0 1 1.41 0l4.95 5a1 1 0 0 1 0 1.42L18.54 21a7 7 0 0 1-4.95 2.07ZM5.1 6.17l-.71.71a5 5 0 0 0 0 7.07l5.66 5.66a5 5 0 0 0 7.07 0l.71-.71-3.63-3.63a4 4 0 0 1-4.86-.61 4 4 0 0 1-.61-4.86L5.1 6.17Zm12.78 5.95a1 1 0 0 1-1-1 4 4 0 0 0-4-4 1 1 0 0 1 0-2 6 6 0 0 1 6 6 1 1 0 0 1-1 1Zm4.19 0a1 1 0 0 1-1-1 8.19 8.19 0 0 0-8.19-8.19 1 1 0 0 1 0-2c5.625.006 10.184 4.565 10.19 10.19a1 1 0 0 1-1 1Z"></path></svg></span></div></div></div>
            restaurant_phone_element = taco_soup.find('div', class_="css-djo2w").find('p', class_="css-1p9ibgf") 
            if restaurant_phone_element is not None:
                possible_website = restaurant_phone_element.find('a', class_="css-1idmmu3")
                if possible_website is not None: # Check to see if the program is scraping the website address, not the phone number
                    restaurant_phone = 'no data' # This is because the website address and phone number are contained in the same <div>
                else:
                    restaurant_phone = restaurant_phone_element.get_text(strip=True)
            else:
                restaurant_phone = 'no data'
            
            # Retrieves the address given on the webpage. An HTML snippet is shown for reference:        
            # <p class=" css-qyp8bo" data-font-weight="semibold">1329 S Hazelwood Blvd Fresno, CA 93702</p>
            restaurant_location_element = taco_soup.find('p', class_="css-qyp8bo")
            if restaurant_location_element is not None:
                restaurant_location = restaurant_location_element.get_text(strip=True)
            else:
                restaurant_location = 'no data'
            
            # The html blocks where business hours are stored are all within: <tr class=" css-29kerx">
            tr_blocks = taco_soup.find_all('tr', class_="css-29kerx")
            restaurant_hours = []
            restaurant_times = []
            
            for block in tr_blocks: # Iterates through each block in tr_blocks to extract the string which contains the business hour information
                restaurant_hours.append(block.get_text(strip=True))
            
            # This removes empty strings and adds them to a new list. The HTML block contained text indicating if the business was closed or open now at the time of the original webscrape.  
            for time in restaurant_hours: # I remembered a question in the discord chat about removing empty elements in a list
                if (time != ''): 
                    if 'closed now' in time.lower(): # Removes 'closed now' from string
                        time = time[:-10]  
                    elif 'open now' in time.lower(): # Removes 'open now' from string
                        time = time[:-8]  
                    if '(next day)' in time.lower():  # Removes '(next day)' from string
                        time = time[:-10]
                    restaurant_times.append((time[:3] + ' ' + time[3:]).strip()) # For readability, a space is added to seperate the day from the times using concatenation and slicing.
            
            #These are print statements used to verify my scraping works:     
            # print(f'restaurant name: {restaurant_name}')      
            # print(f'restaurant rating: {restaurant_rating}')  
            # print(f'restaurant review count: {restaurant_review_count}')     
            # print(f'restaurant website: {restaurant_website}')     
            # print(f'restaurant phone: {restaurant_phone}')     
            # print(f'restaurant location: {restaurant_location}')        
            # print(f'restaurant times: {restaurant_times}')
            # print('')
            
            # These write the information scraped above to a .txt file
            output.write(f'Restaurant Name: {restaurant_name}\n')
            output.write(f'Restaurant Rating: {restaurant_rating}\n')
            output.write(f'Restaurant Review Count: {restaurant_review_count}\n')
            output.write(f'Restaurant Website: {restaurant_website}\n')
            output.write(f'Restaurant Phone: {restaurant_phone}\n')
            output.write(f'Restaurant Address: {restaurant_location}\n')
            output.write(f'Restaurant Business Hours: {restaurant_times}\n')
            output.write('\n')
            
            # This creates a dictionary of the scraped data, which is then appended to 'export_data' through each iteration. 
            scraped_data = {
                                "Restaurant Name": restaurant_name,
                                "Restaurant Rating": restaurant_rating,
                                "Restaurant Review Count": restaurant_review_count,
                                "Restaurant Website": restaurant_website,
                                "Restaurant Phone": restaurant_phone,
                                "Restaurant Address": restaurant_location,
                                "Restaurant Business Hours": restaurant_times
            }
            export_data.append(scraped_data) 
            
            # As each file iterates, it is closed before opening the next one.               
            html.close()  
                
        except Exception as e:
            print(f"An error occurred while reading html from {taco_html}")
            
# Used to visually verify the dictionary works as intended. 
# print(export_data) 

# This exports 'export_data' into a json file.
with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\output_files\\output.json', 'w') as json_output:       
    json.dump(export_data, json_output, indent=2) 
    
# This exports 'export_data' into a .csv file which can then be exported to excel, a jupiter notebook, sql, etc. 
with open('c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\output_files\\output.csv', 'w', newline="", encoding="utf-8") as csv_output:
    field_names = export_data[0].keys() # Creates the field names from the dictionary keys. Only one is needed since they all have the same format.
    csv_writer = csv.DictWriter(csv_output, fieldnames = field_names)
    csv_writer.writeheader()
    csv_writer.writerows(export_data)

# These .close() functions close out the .txt files used in the program.
csv_output.close()
json_output.close()
output.close()      
links_file.close() 
links_txt.close()
m1.close()

