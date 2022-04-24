from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
import pandas as pd
import json
from datetime import datetime
from pygooglenews import GoogleNews
from pretty_html_table import build_table


#Get the email info
get_info = pd.read_json('your_config_json_path',typ='series')
get_email = get_info['email']
get_pwd = get_info['password']

#Get the time now
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

#Get the crypto news
gn = GoogleNews(country = 'UK')
crypto = ['Bitcoin','Solana']

#Create df
df = pd.DataFrame(columns=['Crypto','News', 'Link'])

#function
def coin_news(_coin, time):
    global df

    #Search news
    search = gn.search(_coin,when=time)

    #Get number of news
    number_of_news = len(search['entries'])

    #Get news title & link
    for item in search['entries']:
        title = item['title'].encode(encoding='UTF-8')
        df = df.append({'Crypto':_coin,'News':title,'Link':item['link']},ignore_index=True)

    #Change all data to string & cleaning
    new_df = df.astype('string')

    for line in new_df['News']:
        new_df['News'] = new_df['News'].str.replace("b'",'')
        new_df['News'] = new_df['News'].str.replace('b"','')
    
    #Gmail info
    recipients = [get_email] 
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['Subject'] = f"{_coin} {number_of_news} News at {dt_string}"
    msg['From'] = get_email

    #df to HTML style
    html = """\
    <html>
        <head></head>
        <body>
            {0}
        </body>
    </html>
    """.format(build_table(new_df,'yellow_light'))

    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    #Login Gmail & Send emails
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(get_email, get_pwd)
    server.sendmail(msg['From'], emaillist , msg.as_string())

    df = df.iloc[0:0]
    new_df = new_df.iloc[0:0]
    print(f'{_coin} Email sent!')

#Get the coin name & run function
for coin in crypto:
    coin_news(coin,'6h')
