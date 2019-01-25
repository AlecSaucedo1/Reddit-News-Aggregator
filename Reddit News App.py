import praw
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob as tb
from unidecode import unidecode
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os



class redditScraper():

    def __init__(self):
        self.headers = {'User-Agent': 'newsApp (by ""name"")'}
        self.secrets = """login info"""
        self.reddit = praw.Reddit(client_id=self.new_id, user_agent=self.headers, client_secret=self.new_secret,
                                  password=self.password, username=self.username)

    def subreddit_maker(self):
        subreddit = input('subreddit to search? ')
        self.sub = self.reddit.subreddit(subreddit)

    def get_titles(self):
        limit = int(input('number of posts to review? '))
        self.titles_list = [submission.title for submission in self.sub.hot(limit=limit)]
        self.urls_list = [submission.url for submission in self.sub.hot(limit=limit)]

    def get_url_descriptions(self):
        self.url_desc = dict()
        for url, title in zip(self.urls_list, self.titles_list):
            r = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup = BeautifulSoup(r.text, "html5lib")
            paras = soup.find_all('p')
            parasList = list()
            for i in paras:
                s = str(i)
                if re.search('<p>', s) is not None:
                    parasList.append(s)
            self.url_desc[title] = parasList

    def clean_url_desc(self):
        tag_re = re.compile(r'<[^>]+>')
        for i in self.url_desc:
            temp_list = list()
            for j in self.url_desc[i]:
                temp_string = j
                temp_string = tag_re.sub('', temp_string)
                temp_string = tb(unidecode(temp_string))
                temp_list.append((str(temp_string), round(temp_string.subjectivity, 2)))
            self.url_desc[i] = temp_list
            
    def unpack_url_desc(self):
      self.mass_string = ''
      for key, val in zip(self.url_desc, self.url_desc.values()):
        self.mass_string += str(key) + '\n' + ' ' + '\r' + ' ' + '\n'  + ' ' + str(val)
        
    def send_email(self):
      filepath = 'my_email.txt'
      with open(filepath, 'w') as fp:
        fp.write(unidecode(self.mass_string))
        
      fp.close()
      fp = open(filepath, 'r')
      
      msg = MIMEText(fp.read())
      fp.close()
      
      me = """sender email"""
      
      msg['Subject'] = 'Recap'
      msg['From'] = me
      msg['To'] = """email here"""
      
      
      server = smtplib.SMTP('smtp.gmail.com', 587)
      server.starttls()
      server.login(me, """password""")
      text = msg.as_string()
      server.sendmail(me, """sender""", text)
      server.quit()
      


k = redditScraper()
k.subreddit_maker()
k.get_titles()

print('use clean_url_desc() function to clean text')

k.get_url_descriptions()

