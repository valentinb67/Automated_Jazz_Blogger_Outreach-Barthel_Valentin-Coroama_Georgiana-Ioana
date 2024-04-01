import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def get_url(url):
    '''
    Function to retrieve the HTML content of a given URL using a fake user agent and handling exceptions.

    Args:
        url (str): The URL to retrieve the content from.

    Returns:
        BeautifulSoup object if the request was successful, None otherwise.
    '''
    user_agents_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    ]

    headers = {'User-Agent': random.choice(user_agents_list)}
    with requests.Session() as session:
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()  # Cela va lever une exception pour les codes 4xx/5xx
            return BeautifulSoup(response.text, features="lxml")
        except requests.RequestException as e:
            print(f"Error retrieving URL {url}: {e}")
            return None

print(get_url('https://www.smoothjazz.com/festivals'))

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

def scrape_all_events():
    urls = get_all_pages()
    all_events = []
    for url in urls:
        events = get_event_names(url)
        all_events.extend(events)
    return pd.DataFrame(all_events)

TableEvent = scrape_all_events()

TableEvent["Pays_Event"] = TableEvent["Pays_Event"].replace({"United States": "USA"})
TableEvent

nom_fichier = 'TableEvent.csv'
TableEvent.to_csv(nom_fichier, index=False)