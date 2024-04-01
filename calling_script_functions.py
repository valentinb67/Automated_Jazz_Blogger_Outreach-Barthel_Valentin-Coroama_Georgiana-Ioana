# STRUCTURE du script: 4 parties
# partie 1: importer et appeller les fonctions du script correspondant au scrapping du site des bloguers; créer une fonction get_bloggers(url) qui appelle toutes ces fonctions
# partie 2: importer et appeller les fonctions du script correspondant au scrapping du site des festivals; créer une fonction get_festivals() qui appelle toutes ces fonctions
# partie 3: importer les 3 fonctions du script correspondant à la création du mail automatique
# partie 4: créer une fonction globale get_everything() qui appelle les fonctions des 3 parties précédentes pour executer l'ensemble du code.

#importation des packages
import sys
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Importer les fonctions du script scraping_blogs
from scraping_blogs import get_url, get_names, get_locals, get_webs, get_followers, create_email

# url du site avec les blogueurs
url = "https://music.feedspot.com/jazz_blogs/"

# la fonction qui récupère les urls des sites des blogueurs
blog_urls = get_url(url) 

# Appeler les fonctions
names = get_names(url)
locals = get_locals(url)
webs = get_webs(url)

# Les fonctions avec plus d'un argument
twitter_followers = get_followers(url, "fs-twitter")
facebook_followers = get_followers(url, "fs-facebook")
instagram_followers = get_followers(url, "fs-instagram")

emails = create_email()

# Création d'une fonction globale qui appelle l'ensemble des fonctions du script des blogueurs pour extraire les données

def get_bloggers(url):  

    get_url(url)
    nom_blog = get_names(url) #nom des blogs
    localisation = get_locals(url) #localisation des blogeurs
    site_web = get_webs(url) #sites web des blogeurs

    # abonnés sur Twitter, Facebook et Instagram
    twitsub = get_followers(url, "fs-twitter")
    fbsub = get_followers(url, "fs-facebook")
    instasub = get_followers(url, "fs-instagram")

    # abonnés convertis en nombre
    fbsub_num = [convertir_en_nombre(abonne) for abonne in fbsub]
    twitsub_num = [convertir_en_nombre(abonne) for abonne in twitsub]
    instasub_num = [convertir_en_nombre(abonne) for abonne in instasub]

    adresses_email = create_email()  # création des adresses mail pour chaque blogueur
    return [nom_blog, localisation, site_web, fbsub_num, twitsub_num, instasub_num, adresses_email]

# Appel de la fonction pour extraire les données
url = "https://music.feedspot.com/jazz_blogs/"
get_bloggers(url)

#Créer une fonction qui permet d'ajouter des lignes dans le tableau créé

def add_row_to_table(table, new_row):
    # Créer un DataFrame à partir de la nouvelle ligne
    new_df = pd.DataFrame([new_row])
    
    # Concaténer le DataFrame existant avec le nouveau DataFrame
    table = pd.concat([table, new_df], ignore_index=True)
    
    return table

# Mettre les commandes permetant de générer le tableau contenant l'ensemble des données des bloguers à l'intérieur d'une fonction
def create_datablog():
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
    TableBlog["Pays"] = TableBlog["Pays"].replace({"US": "USA"})
    
    return TableBlog

# Créer le DataFrame initial
TableBlog = create_datablog()

# Ajouter des nouvelles lignes dans le tableau (pour vérifier par la suite si l'envoi des mails fonctionne correctement en utilisant des adresses mail réelles)
new_rowG = {'Nom Blog': "Georgiana", 'Pays': "Romania" ,'Région': "none", 'Ville': "none", 'Adresse Email': "iogecor02@gmail.com", 
            'Site web': "none" ,'Abonnées Facebook': 0, 'Abonnées Twitter': 0, 'Abonnées Instagram': 0}
new_rowV = {'Nom Blog': "Valentin", 'Pays': "France" ,'Région': "none", 'Ville': "none", 'Adresse Email': "valentin.barthel@etu.unistra.fr", 
            'Site web': "none" ,'Abonnées Facebook': 0, 'Abonnées Twitter': 0, 'Abonnées Instagram': 0}
#new_rowP = {'Nom Blog': "Pierre Pelletier", 'Pays': "France" ,'Région': "none", 'Ville': "none", 'Adresse Email': "p.pelletier@unistra.fr", 
#           'Site web': "none" ,'Abonnées Facebook': 0, 'Abonnées Twitter': 0, 'Abonnées Instagram': 0}
TableBlog = add_row_to_table(TableBlog, new_rowG)
TableBlog = add_row_to_table(TableBlog, new_rowV)
#TableBlog = add_row_to_table(TableBlog, new_rowP)

print(TableBlog)


# # PARTIE 2. Scrapper le site des festivals

# i,porter les fonctions du script correspondant au scrapping du site des festivals
from scraping_festivals import get_all_pages, get_event_names, scrape_all_events

#creer une fonction qui appelle les fonctions du script des festivals pour récupérer l'ensemble des données:
def get_festivals():
    get_all_pages() # récupérer toutes les pages du site
    get_event_names(url) #récuperer les noms des festivals
    TableEvent = scrape_all_events() #générer un tableau qui comporte les informations sur les festivals (nom, pays, période, ville etc.)
    TableEvent["Pays_Event"] = TableEvent["Pays_Event"].replace({"United States": "USA"}) #remplacer United States par USA
    print(TableEvent)

get_festivals()  


# # PARTIE 3: mail automatique
# importer les fonctions du script correspondant à l'envoi automatique du mail
from sending_mail import format_blogger_email, format_event_list, send_jazz_event_invitations 

# # PARTIE 4: appeller les 3 parties pour tout afficher

# Créer la fonction finale qui permet d'appeller l'ensemble des fonctions créées précédemment et d'exécuter l'intégralité du code des trois parties
def get_everything():
    get_bloggers(url) #fonction qui appelle l'ensemble des fonctions du script des bloguers pour récuperer les données
    create_datablog() #fonction qui crée le tableau TableBlog
    get_festivals() #fonction qui appelle l'ensemble des fonctions du script des festivals pour récuperer les données
    format_blogger_email(blog['Nom Blog'], followers, country) #fonction qui permet de personnaliser le mail automatique
    format_event_list(country_events) #fonction qui permet de personnaliser le mail automatique
    send_jazz_event_invitations("smtp.gmail.com", 465, "jazzyworld67@gmail.com", "ogunqrpjhigzwpfc", TableBlog, TableEvent) #fonction qui assure la connexion au serveur SMTP, l'envoi du mail à l'ensemble des adresses et la déconnexion du serveurs
    
get_everything() 