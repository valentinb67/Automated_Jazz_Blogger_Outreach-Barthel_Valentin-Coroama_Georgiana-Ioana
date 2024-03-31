#!/usr/bin/env python
# coding: utf-8

# In[10]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd



# In[2]:


url = 'https://www.smoothjazz.com/festivals'
url


# In[3]:


response = requests.get(url)
response


# In[4]:

if response.ok:
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup)


# In[5]:


def get_all_pages():
    urls = []
    page_number = 0
    for i in range(1, 16):  # Ajustez le 16 si nécessaire pour le nombre de pages total
        url = f"https://www.smoothjazz.com/festivals?page={page_number}"
        page_number += 1
        urls.append(url)
    return urls

def get_event_names(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    festivals = soup.find_all("tr")
    data = []
    for festival in festivals[1:]:
        event_details = {}
        event_details['Nom_Event'] = festival.find("td", headers="view-title-table-column", class_="views-field views-field-title is-active").text.strip() if festival.find("td", headers="view-title-table-column", class_="views-field views-field-title is-active") else ""
        event_details['Ville_Envent'] = festival.find("td", headers="view-field-city-table-column", class_="views-field views-field-field-city").text.strip() if festival.find("td", headers="view-field-city-table-column", class_="views-field views-field-field-city") else ""
        event_details['Region_Event'] = festival.find("td", headers="view-field-state-region-table-column", class_="views-field views-field-field-state-region").text.strip() if festival.find("td", headers="view-field-state-region-table-column", class_="views-field views-field-field-state-region") else ""
        event_details['Pays_Event'] = festival.find("td", headers="view-field-country-table-column", class_="views-field views-field-field-country").text.strip() if festival.find("td", headers="view-field-country-table-column", class_="views-field views-field-field-country") else ""
        event_details['Periode_Event'] = festival.find("td", headers="view-field-event-month-table-column", class_="views-field views-field-field-event-month").text.strip() if festival.find("td", headers="view-field-event-month-table-column", class_="views-field views-field-field-event-month") else ""
        data.append(event_details)
    return data

def scrape_all_events():
    urls = get_all_pages()
    all_events = []
    for url in urls:
        events = get_event_names(url)
        all_events.extend(events)
    return pd.DataFrame(all_events)

# Exécutez cette fonction pour récupérer les données de toutes les pages et les stocker dans un DataFrame
TableEvent = scrape_all_events()

# In[6]:


#Remplaçons les valeures doubles
TableEvent["Pays_Event"] = TableEvent["Pays_Event"].replace({"United States": "USA"})
TableEvent


# In[9]:

chemin ='C:\\Users\\valen\\Documents\\GitHub\\Projet-Barthel-Valentin-Coroama-Georgiana\\TableEvent.csv'
TableEvent.to_csv(chemin, index=False)


# In[11]:


def get_path(chemin):
    return TableEvent.to_csv(chemin, index=False)


# In[ ]:




