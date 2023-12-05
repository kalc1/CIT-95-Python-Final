from bs4 import BeautifulSoup
import requests
import os

output_directory = 'c:\\Users\\kalco\\Coding Projects\\Python\\CIT-95-Python-Final\\yelp_html'
os.makedirs(output_directory, exist_ok=True) # Since I have to run this a few times for testing, an OSError will be raised if its value is False, so this is set to True. This is because the directory will already exist after the initial running of this code. 

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

# The following is just a template for iterating through each .txt file that contains the html data and parsing through each one
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
        # <a href="/biz_redir?url=https%3A%2F%2Ffresnomexicanfood.com&amp;cachebuster=1701716554&amp;website_link_type=website&amp;src_bizid=-Ufu3Ha7V9Z6Z4YBx1yTfg&amp;s=91159ae84e4fd445df8daada241e54af990b8bf2bdc168212f103dcb02cdd4ad" 
        # class="css-1idmmu3" target="_blank" rel="noopener" role="link">fresnomexicanfood.com</a>
        restaurant_website_element = taco_soup.find('a', class_="css-1idmmu3", target="_blank")
        if restaurant_website_element is not None:
            restaurant_website = restaurant_website_element.get_text(strip=True)
        else:
            restaurant_website = 'no data'
                
        # <p class=" css-1p9ibgf" data-font-weight="semibold">(559) 618-1100</p>
        restaurant_phone_element = taco_soup.find()
        if restaurant_phone_element is not None:
            restaurant_phone = restaurant_phone_element.get_text(strip=True)
        else:
            restaurant_phone = 'no data'
                
        # <p class=" css-qyp8bo" data-font-weight="semibold">1329 S Hazelwood Blvd Fresno, CA 93702</p>
        # TODO handle outputs without real address such as {i} = 0 and 9
        restaurant_location_element = taco_soup.find('p', class_="css-qyp8bo")
        if restaurant_location_element is not None:
            restaurant_location = restaurant_location_element.get_text(strip=True)
        else:
            restaurant_location = 'no data'
        
        # <p class="day-of-the-week__09f24__JJea_ css-1p9ibgf" data-font-weight="semibold">Fri</p>
        # <p class="no-wrap__09f24__c3plq css-1p9ibgf" data-font-weight="semibold">7:00 AM - 5:00 PM</p>
        restaurant_hours_element = taco_soup.find()
        
        # <p class=" css-11k8aw1">Restaurante familiar especializado en comida mexicana de calidad. Tenemos 10 años de experiencia ofreciendo no solo una comida sabrosa, sino un servicio que lo hace sentir especial. La pasión por lo que hacemos marca una diferencia en nuestros servicios. Nuestras recetas conservan la tradición de nuestros ancestros, por lo que la autenticidad de los sabores mexicanos está impresa en cada plato.</p>
        # <div class=" css-1qn0b6x"><div class="section-heading__09f24__F0gJv css-1qn0b6x"><h5 class="css-agyoef">Specialties</h5></div><p class=" css-11k8aw1">Restaurante familiar especializado en comida mexicana de calidad. Tenemos 10 años de experiencia ofreciendo no solo una comida sabrosa, sino un servicio que lo hace sentir especial. La pasión por lo que hacemos marca una diferencia en nuestros servicios. Nuestras recetas conservan la tradición de nuestros ancestros, por lo que la autenticidad de los sabores mexicanos está impresa en cada plato.</p></div>
        # <div class=" css-1qn0b6x"><div class="section-heading__09f24__F0gJv css-1qn0b6x"><h5 class="css-agyoef">Meet the Business Owner</h5></div><div class="business-owner-passport__09f24__QTpe6 css-1qn0b6x"><div class=" css-1qn0b6x" aria-labelledby="businessOwner-:r1s:" role="region"><p class=" css-na3oda" id="businessOwner-:r1s:">Business owner information</p><div class="arrange__09f24__LDfbs gutter-1__09f24__yAbCL vertical-align-middle__09f24__zU9sE css-1qn0b6x"><div class="arrange-unit__09f24__rqHTg css-1qn0b6x"><div class="avatar__09f24__bUjfQ css-1qn0b6x"><div class="css-eqfjza"><img class=" css-xlzvdl" src="https://s3-media0.fl.yelpcdn.com/assets/srv0/yelp_styleguide/bf5ff8a79310/assets/img/default_avatars/user_medium_square.png" srcset="" alt="Photo of Allen J." height="40" width="40" loading="lazy" draggable="true"></div></div></div><div class="arrange-unit__09f24__rqHTg arrange-unit-fill__09f24__CUubG css-1qn0b6x"><p class=" css-ux5mu6" data-font-weight="bold">Allen J.</p><div class=" css-1qn0b6x"><p class=" css-chan6m" aria-hidden="true">Business Owner</p></div></div></div></div></div><p class=" css-11k8aw1"><span class=" raw__09f24__T4Ezm">Allen &amp; Anna we were inspired to bring great authentic Mexican flavors to our city.</span></p></div>
        restaurant_about_element = taco_soup.find()
        
        #These are print statements used to verify my scraping works:
        # print(restaurant_name)
        # print(restaurant_rating)
        # print(restaurant_review_count)
        print(restaurant_website)
        # print(restaurant_location)
            
    except Exception as e:
        print(f"An error occurred while reading html from {taco_html}")
        
        

# These .close() functions close out the .txt files used in the program.         
links_file.close() 
html.close()
links_txt.close()
m1.close()

