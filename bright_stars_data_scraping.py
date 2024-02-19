from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# WIKIPEDIA Bright STARS DATA URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

# Webdriver
browser = webdriver.Chrome("chromedriver-win64\chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

scarped_data = []


# Define Data Scrapping Method
def scrape(hyperlink):
        print(hyperlink)
               
        # BeautifulSoup Object     
        soup = BeautifulSoup(browser.page_source, "html.parser")

        # VERY IMP: The class "wikitable" and <tr> data is at the time of creation of this code. 
        # This may be updated in future as page is maintained by Wikipedia. 
        # Understand the page structure as discussed in the class & perform Web Scraping from scratch.

        # Find <table>
        bright_star_table = soup.find("table", attrs={"class", "wikitable"})
        
        # Find <tbody>
        table_body = bright_star_table.find('tbody')

        # Find <tr>
        table_rows = table_body.find_all('tr')

        # Get data from <td>
        for row in table_rows:
            table_cols = row.find_all('td')
            print(table_cols)
            
            temp_list = []

            for col_data in table_cols:
                # Print Only colums textual data using ".text" property
                # print(col_data.text)

                # Remove Extra white spaces using strip() method
                data = col_data.text.strip()
                # print(data)

                temp_list.append(data)

            # Append data to star_data list
            scarped_data.append(temp_list)

            try:
                page = requests.get(hyperlink)
                soup = BeautifulSoup(page.content,"html.parser")
                temp_list=[]
                for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
                    td_tags = tr_tag.find_all("td")
                    for td_tag in td_tags:
                        try:
                            temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                        except:
                            temp_list.append("")
                stars_data.append(temp_list)
            except:
                time.sleep(1)
                scrape(hyperlink)  
            

        star_df_1= pd.read_csv("updated_scraped_data.csv")


       
# Calling Method    
scrape()

################################################################
for index, row in star_df_1.iterrows():
    print(row['hyperlink'])
    scrape(row['hyperlink'])

    print(f"Data Scraping at hyperlink {index+1} completed")

print(scrape)

# IMPORT DATA to CSV

stars_data = []


for i in range(0,len(scarped_data)):
    
    Star_names = scarped_data[i][1]
    Distance = scarped_data[i][3]
    Mass = scarped_data[i][5]
    Radius = scarped_data[i][6]
    Lum = scarped_data[i][7]

    required_data = [Star_names, Distance, Mass, Radius, Lum]
    stars_data.append(required_data)

print(stars_data)


# Define Header
headers = ['Star_name','Distance','Mass','Radius','Luminosity']  

# Define pandas DataFrame   
star_df_1 = pd.DataFrame(stars_data, columns=headers)

#Convert to CSV
star_df_1.to_csv('scraped_data.csv',index=True, index_label="id")
