import time
import praw
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id= os.getenv('client_id') ,
    client_secret=os.getenv('client_secret'),
    username=os.getenv('username'),
    password=os.getenv('password'),
    user_agent=os.getenv('user_agent')
)

subreddit = reddit.subreddit('Indiasocial')




flair_map = {
        '1':'3d51fefa-228d-11ee-9771-767bb70b1ec5', 
         '2':'5c495150-228d-11ee-954f-4a161e70705a', 
         '3':'7be926de-228d-11ee-9dae-d6805a45f6a1',
         '4':'941830b0-228d-11ee-a264-f6eea1dfc7ee',
         '5':'b44de398-228d-11ee-8743-4a7c569949a7',
         '6':'259208a4-228e-11ee-b519-d26e43d71287',
         '7':'f04a7518-228e-11ee-8077-1678acdcacfe', 
         '8':'b4aa4b24-22b5-11ee-979e-9ef4a87d59a1',
         '9':'0ae370a4-2727-11ee-8c8a-522399798dee',
         '10':'35fe86fa-28e1-11ee-9e8f-526b923d29fe'
        }

def take_ss(comment,title,flair):
    driver.implicitly_wait(5)
    parent_comment = comment.parent()
    url = parent_comment.permalink
    driver.get(f'https://www.reddit.com{parent_comment.permalink}?context=2&depth=1')
    
    try:
        print('chalrau')
        buttons = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.items-center > span:nth-child(1) > svg:nth-child(1) > path:nth-child(1)')))
        for i,elem in enumerate(buttons):
            if i==0:
                continue
            elem.click()
    except Exception as err:
        print(err)

    try:
        comment.parent().upvote()
        comment.parent().parent().upvote()
    except Exception as err:
        print(err)
    try:
        wait = WebDriverWait(driver,10)
        cross =wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.icon-close')))
        cross.click()
        driver.implicitly_wait(3)
        commentbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'._2M2wOqmeoPVvcSsJ6Po9-V')))
        driver.execute_script("arguments[0].scrollIntoView({block:'start'});",commentbox)
               
        screenshot_filename = f'/home/swetabhshreyam/programming/Python/reddit-bot/ss/{url.split("/")[-2]}.png'
        commentbox.screenshot(screenshot_filename)
        sub=reddit.subreddit("IndianBoysonLNRDT").submit_image(title, screenshot_filename)
        sub.flair.select(flair_map[flair])
        sub.reply(f'u/{comment.parent().parent().author.name} u/{parent_comment.author.name}')
        try:
            comment.reply(f'Thank you for reporting the jhatubaazi, good soldier.\n This jhaatubaazi has been reported here\n https://www.reddit.com{sub.permalink}')

        except Exception as err:
            print(err)
    except Exception as err:
        print(err)
    print('1 baar run hogya bhay') 
    
        
    
    
cookies = pickle.load(open('cookies.pkl','rb'))
firefox_options = Options()
firefox_options.add_argument("-headless")
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument("--disable-dev-shm-usage")
firefox_options.add_argument("--disable-infobars")
driver = webdriver.Firefox(options=firefox_options)
driver.maximize_window()
driver.get('https://www.reddit.com')
for cookie in cookies:
        driver.add_cookie(cookie)

for comment in subreddit.stream.comments(skip_existing=True):
    try:
        if '!reportjhatu' in str(comment.body).lower() or '!reportjhantu' in str(comment.body).lower():
            title = str(comment.body).split('-t ')
            flair = str(comment.body).split('-f ')
            if len(title)==1 and len(flair) ==1:
                take_ss(comment,'Simping hori bahut bhayankar','3')
            elif len(title)==1 and len(flair)!=1:
                take_ss(comment,'Simping hori bahut bhayankar',flair[1])
            elif len(title)!=1 and len(flair)==1:
                take_ss(comment,title[1],'3')
            else:
                titletext = title[1].split('-f')[0]
                flairtext = title[1].split('f ')[1]
                take_ss(comment,titletext,flairtext)

    except Exception as err:
        print(err)

