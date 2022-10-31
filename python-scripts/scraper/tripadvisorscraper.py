from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

url = 'https://www.tripadvisor.nl/Hotel_Review-g188575-d230890-Reviews-Amrath_Grand_Hotel_de_l_Empereur-Maastricht_Limburg_Province.html#REVIEWS'

def hotelScraper(url):
    # opties instellen voor driver 
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    ## options.add_argument("--headless") NOTE! toevoegen als op achtergrond laten draaien

    # start driver
    drv = webdriver.Chrome(options=options)

    # go to website
    drv.get(url)

    # ZZZZZzzzz even slapen rustig laten laden
    sleep(1)

    # cookies accepteren
    drv.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()

      # ff geduld hebbe
    sleep(1)

    import pandas as pd
    rev_df = pd.DataFrame()

    # start loop over alle reviews heen
    end = False
    while end == False: 
        # haal reviews binnen
        reviews = drv.find_elements(By.XPATH,'//*[@id="component_16"]/div/div[3]/div[*]') 
        
        try:
            rev = []
            for r in reviews:
                rev += [r.get_attribute('innerHTML')]

            if 'Deze beoordelingen zijn machinevertalingen' in rev[2]:
                print('einde van de scraper')
                end = True

            import pandas as pd
            # elements to dataframe
            df = pd.DataFrame({'element':rev[2:7]})

            # get rating
            df['rating'] = df['element'].str.extract(r'(ui_bubble_rating bubble_[0-5]{2})')
            df['rating'] = df['rating'].str.extract(r'([0-5]{2})').astype(int)

            # get review
            df['review'] = df['element'].str.extract(r'(<q class="QewHA H4 _a"><span>.*?</span></q></div><div class="lszDU" style=.line-height: 20px)') 
            df['review'] = df['review'].str.replace(r'(<q class="QewHA H4 _a"><span>)','')
            df['review'] = df['review'].str.replace(r'(</span></q></div><div class="lszDU" style=.line-height: 20px)','')    

            # drop element kolom
            df = df.drop(columns=['element'])
            rev_df = rev_df.append(df)

            # we hebben geen haast
            sleep(1.5)
            
            # vast naar de volgende pagina gaan
            try:
                #proberen om naar de volgende pagina te gaan, indien niet lukt error als inpunt om de while loop te doorbreken
                drv.find_element(By.LINK_TEXT,'Volgende').click()
            except:
                print('einde van de scraper')
                end = True

            # even bijkomen
            sleep(1.5)
        except Exception as e:
            print('einde van de scraper met de volgende error:\n',e)
            end = True

    df = rev_df.copy()

    return df

