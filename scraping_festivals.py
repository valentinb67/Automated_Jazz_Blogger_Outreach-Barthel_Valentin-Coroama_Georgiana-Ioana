import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

#Appel de la fonction get_url() depuis le script scraping_blogs
from scraping_blogs import get_url
print(get_url('https://www.smoothjazz.com/festivals'))

#Création d'une fonction permettant de scraper toutes les pages contenant les informations à scrapper sur les festivals 
def get_all_pages():
    urls = []
    page_number = 0
    for i in range(1, 16):  # Ajustez le 16 si nécessaire pour le nombre de pages total
        url = f"https://www.smoothjazz.com/festivals?page={page_number}"
        page_number += 1
        urls.append(url)
    return urls

#Création d'une fonction permettant de scraper le nom, la ville, la région, le pays et la date des festivals
def get_event_names(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="lxml")
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
    
#Création d'une fonction afin d'appliquer la fonction pour obtenir les informations de tout les festivals pour chacunes des pages (get_all_pages)
def scrape_all_events():
    urls = get_all_pages()
    all_events = []
    for url in urls:
        events = get_event_names(url)
        all_events.extend(events)
    return pd.DataFrame(all_events)

#Création d'un dataframe  TableEvent conservant l'ensemble des informations scrapées
TableEvent = scrape_all_events()

TableEvent["Pays_Event"] = TableEvent["Pays_Event"].replace({"United States": "USA"})
TableEvent

#Téléchargement de la database TableEvent en csv dans le même folder que celui du script et des autres scripts
nom_fichier = 'TableEvent.csv'
TableEvent.to_csv(nom_fichier, index=False)
