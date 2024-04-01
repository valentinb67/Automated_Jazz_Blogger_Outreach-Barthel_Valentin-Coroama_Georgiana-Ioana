#!/usr/bin/env python
# coding: utf-8

# In[38]:


import requests 
import random 
import pprint
import re
import time
from collections import defaultdict
from bs4 import BeautifulSoup
import numpy as np
import tqdm
import pandas as pd


# In[39]:


url = "https://music.feedspot.com/jazz_blogs/"


# In[40]:


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


# In[41]:


def get_names(url):
    soup = get_url(url)
    h3s = soup.find_all('h3', attrs={'class':'feed_heading'})
    
    noms = []
    
    for h3 in h3s:
        nns = h3.find_all('a', class_='tlink fd_lk')
        
        if len(nns) > 0:
            # Accès direct au texte de chaque élément span trouvé
            for nn in nns:
                noms.append(nn.get_text())
        else:
            noms.append('none')
    return noms

nom_blog = get_names("https://music.feedspot.com/jazz_blogs/")
print(len(nom_blog))
print(nom_blog)


# In[42]:


#Création d'une liste contenant les adresses emails fictives "{nom_blog}@exemple.com":
def create_email():
    adresses_email = []
    for blog in nom_blog:
    # Nettoyer et remplacer les espaces et caractères spéciaux
        nom_simplifie = blog.strip().replace(' ', '_').replace('&', 'and').replace('»', '').replace('|', '').replace('.', '').lower()
    # Ajouter un domaine fictif
        adresse_email = nom_simplifie + "@exemple.com"
        adresses_email.append(adresse_email)

# Afficher les adresses e-mail créées
    for adresse in adresses_email:
        return adresses_email
create_email()  


# In[43]:


def get_locals(url):
    soup = get_url(url)
    h3s = soup.find_all('p', attrs={'class':'trow trow-wrap'})
    
    locals_ = []
    
    for h3 in h3s:
        nns = h3.find_all('span', class_='location_new')
        
        if len(nns) > 0:
            # Accès direct au texte de chaque élément span trouvé
            for nn in nns:
                locals_.append(nn.get_text())
        else:
            locals_.append('none')
    return locals_

localisation = get_locals("https://music.feedspot.com/jazz_blogs/")
print(len(localisation))
print(localisation)


# In[44]:


Ville = []
Region = []
Pays = []

for loc in localisation:
    parts = loc.split(', ')
    
    # Gestion des cas spéciaux
    if loc == 'none' or len(parts) == 1:
        Ville.append('none')
        Region.append('none')
        Pays.append(parts[0] if loc != 'none' else 'none')
    elif len(parts) == 2:
        # Supposition: format "Ville, Pays"
        Ville.append(parts[0])
        Region.append('none')
        Pays.append(parts[1])
    elif len(parts) >= 3:
        # Format complet "Ville, Région, Pays"
        Ville.append(parts[0])
        Region.append(parts[1])
        Pays.append(parts[2])

# Affichage pour vérification
print("Villes:", Ville)
print("Regions:", Region)
print("Pays:", Pays)


# In[45]:


def get_webs(url):
    soup = get_url(url)
    h3s = soup.find_all('p', attrs={'class':'trow trow-wrap'})
    
    webs = []
    
    for h3 in h3s:
        nns = h3.find_all('a', class_='ext')
        
        if len(nns) > 0:
            # Accès direct au texte de chaque élément span trouvé
            for nn in nns:
                webs.append(nn.get_text())
        else:
            webs.append('none')
    return webs
site_web = get_webs("https://music.feedspot.com/jazz_blogs/")
print(len(site_web))
print(site_web)


# In[46]:


def get_followers(url, name_class):
    
    soup = get_url(url)
    spans = soup.find_all('span', attrs={'class':'eng-outer-wrapper eng-outer-wrapper eng-outer-nodot eng-outer-wrapper--free'})

    abo = []
   
    for span in spans:

        imgs = span.find_all('span', class_=f'{name_class}')
        
        if len(imgs) > 0:
            lst = [img.find_all("span", class_='eng_v') for img in imgs] 
            abo.append(lst[0][0].get_text())   
        else : abo.append('none')

    return abo

twitsub = get_followers("https://music.feedspot.com/jazz_blogs/", "fs-twitter")
fbsub = get_followers("https://music.feedspot.com/jazz_blogs/", "fs-facebook")
instasub = get_followers("https://music.feedspot.com/jazz_blogs/", "fs-instagram")
                      
print(len(twitsub))
print(twitsub)

print(len(fbsub))
print(fbsub)

print(len(instasub))
print(instasub)


# In[47]:


def convertir_en_nombre(abonnes_str):
    # Gère le cas spécial où la chaîne est 'none'
    if abonnes_str == 'none':
        return 0  # Retourne 0 ou une autre valeur par défaut appropriée
    # Supprime 'K', multiplie par 1000 si 'K' était présent
    if 'K' in abonnes_str:
        return int(float(abonnes_str.replace('K', '')) * 1000)
    # Ajoute une condition pour gérer les cas où 'M' est présent
    elif 'M' in abonnes_str:
        return int(float(abonnes_str.replace('M', '')) * 1000000)
    # Supprime les points et les virgules avant de convertir en int
    return int(abonnes_str.replace('.', '').replace(',', ''))

# Application de la fonction à tous les éléments des listes
fbsub_num = [convertir_en_nombre(abonne) for abonne in fbsub]
twitsub_num = [convertir_en_nombre(abonne) for abonne in twitsub]
instasub_num = [convertir_en_nombre(abonne) for abonne in instasub]
len(instasub_num)


# In[48]:


DataBlog = {"Nom Blog": nom_blog,
                "Pays": Pays,
                "Région": Region,
                "Ville": Ville,
                "Adresse Email": create_email(),
                "Site web": site_web,
                "Abonnées Facebook": fbsub_num,
                "Abonnées Twitter": twitsub_num,
                "Abonnées Instagram": instasub_num
                }

TableBlog = pd.DataFrame(DataBlog)


# In[49]:


TableBlog["Pays"] = TableBlog["Pays"].replace({"US": "USA"})
TableBlog


# In[50]:


nom_fichier = 'TableBlog.csv'
TableBlog.to_csv(nom_fichier, index=False)
