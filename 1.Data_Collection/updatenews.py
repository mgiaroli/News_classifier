#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Updating data news from rss feeds
"""

import csv
from time import sleep
from datetime import datetime, timedelta
from lxml import etree
import pandas as pd
import requests


def req(url, sec=1):
    """Function to make tolerant server requests."""
    status_code = 500
    while status_code != 200:
        sleep(sec)
        try:
            result = requests.get(url)
            status_code = result.status_code
            if status_code != 200:
                print("Error - Response Code %i - Retrying" % (result.status_code))
        except: #Exception, probably loss of connection
            print("Exception occurred - Check connection! - Waiting three seconds")
            sleep(3)
    return result

def string_to_date(string):
    """Function to convert strings to date. We have two formats, depend on the newspaper."""
    dummy=string.split(', ')[1].rsplit(' ',1)[0]
    timezone=string.split(', ')[1].rsplit(' ',1)[1]
    if timezone=='-0300':
        date = datetime.strptime(dummy, '%d %b %Y %H:%M:%S')
    elif timezone in ('GMT','+0000'):
        date= datetime.strptime(dummy, '%d %b %Y %H:%M:%S')-timedelta(hours=3)
    return date


#We load the previous data as a panda data frame.
df_news=pd.read_csv('news_data.csv')
df_news.Fecha=df_news.Fecha.apply(pd.to_datetime) #we convert the string date to datetime format

#List to save the new news.
new_news=[]

pages={'https://www.telam.com.ar/rss2/politica.xml':('Política','Télam'),
       'https://www.telam.com.ar/rss2/economia.xml':('Economía','Télam'),
       'https://www.telam.com.ar/rss2/sociedad.xml':('Sociedad','Télam'),
       'https://www.telam.com.ar/rss2/deportes.xml':('Deportes','Télam'),
       'https://www.telam.com.ar/rss2/policiales.xml':('Policiales','Télam'),
       'https://www.telam.com.ar/rss2/internacional.xml':('Internacional','Télam'),
       'https://www.telam.com.ar/rss2/tecnologia.xml':('Ciencia y tecnología','Télam'),
       'https://www.telam.com.ar/rss2/cultura.xml':('Cultura y Espectáculos','Télam'),
       'https://www.telam.com.ar/rss2/espectaculos.xml':('Cultura y Espectáculos','Télam'),
       'https://www.clarin.com/rss/politica/':('Política','Clarín'),
       'https://www.clarin.com/rss/mundo/':('Internacional','Clarín'),
       'https://www.clarin.com/rss/sociedad/':('Sociedad','Clarín'),
       'https://www.clarin.com/rss/policiales/':('Policiales','Clarín'),
       'https://www.clarin.com/rss/cultura/':('Cultura y Espectáculos','Clarín'),
       'https://www.clarin.com/rss/economia/':('Economía','Clarín'),
       'https://www.clarin.com/rss/tecnologia/':('Ciencia y tecnología','Clarín'),
       'https://www.clarin.com/rss/deportes/':('Deportes','Clarín'),
       'https://www.clarin.com/rss/espectaculos/':('Cultura y Espectáculos','Clarín'),
       'https://www.pagina12.com.ar/rss/secciones/el-pais/notas':('Política','Página 12'),
       'https://www.pagina12.com.ar/rss/secciones/economia/notas':('Economía','Página 12'),
       'https://www.pagina12.com.ar/rss/secciones/sociedad/notas':('Sociedad','Página 12'),
       'https://www.pagina12.com.ar/rss/secciones/el-mundo/notas':('Internacional','Página 12'),
       'https://www.pagina12.com.ar/rss/secciones/deportes/notas':('Deportes','Página 12'),
       'https://www.pagina12.com.ar/rss/secciones/cultura/notas':('Cultura y Espectáculos','Página 12'),
       'https://www.pagina12.com.ar/rss/secciones/ciencia/notas':('Ciencia y tecnología','Página 12'),
       'https://www.ambito.com/rss/economia.xml':('Economía','Ámbito Financiero'),
       'https://www.ambito.com/rss/politica.xml':('Política','Ámbito Financiero'),
       'https://www.ambito.com/rss/mundo.xml':('Internacional','Ámbito Financiero'),
       'https://www.ambito.com/rss/deportes.xml':('Deportes','Ámbito Financiero'),
       'https://www.ambito.com/rss/espectaculos.xml':('Cultura y Espectáculos','Ámbito Financiero'),
       'https://www.perfil.com/feed/politica':('Política','Perfil'),
       'https://www.perfil.com/feed/policia':('Policiales','Perfil'),
       'https://www.perfil.com/feed/economia':('Economía','Perfil'),
       'https://www.perfil.com/feed/deportes':('Deportes','Perfil'),
       'https://www.perfil.com/feed/sociedad':('Sociedad','Perfil'),
       'https://www.perfil.com/feed/espectaculos':('Cultura y Espectáculos','Perfil'),
       'https://www.perfil.com/feed/ciencia':('Ciencia y tecnología','Perfil'),
       'https://www.perfil.com/feed/tecnologia':('Ciencia y tecnología','Perfil'),
       'https://www.eldiarioar.com/rss/politica':('Política','Diario AR'),
       'https://www.eldiarioar.com/rss/sociedad':('Sociedad','Diario AR'),
       'https://www.eldiarioar.com/rss/economia':('Economía','Diario AR'),
       'https://www.eldiarioar.com/rss/mundo':('Internacional','Diario AR'),
       'https://www.eldiarioar.com/rss/deportes':('Deportes','Diario AR'),
       'https://www.eldiarioar.com/rss/cultura':('Cultura y Espectáculos','Diario AR'),
       'https://www.eldiarioar.com/rss/tecnologia':('Ciencia y tecnología','Diario AR')
       }


#We parse each new in the xml file (from each url) using lxml, and we keep only the new news.
for item in pages.items():
    print(item)
    url=item[0]
    result=req(url)
    root=etree.fromstring(result.content)
    channel = root.find("channel")
    for key in channel.findall("item"):
        #print(key.find('link').text)
        if string_to_date(key.find('pubDate').text)>df_news.Fecha.max(): #we only keep new news.
            try:
                new_news.append([key.find('title').text,key.find('link').text,key.find('description').text,
                                 string_to_date(key.find('pubDate').text),item[1][1],item[1][0]])
            except:
                new_news.append([key.find('title').text,key.find('link').text,None,
                                 string_to_date(key.find('pubDate').text),item[1][1],item[1][0]])
                print('Description is missing')

print("We have " + str(len(new_news)) + " new news.")


#we update the csv file with the new data
with open("news_data.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(new_news)
    f.close()

df_news=pd.read_csv('news_data.csv')
df_news.Fecha=df_news.Fecha.apply(pd.to_datetime)
print("Total news: " + str(df_news.shape[0]))
