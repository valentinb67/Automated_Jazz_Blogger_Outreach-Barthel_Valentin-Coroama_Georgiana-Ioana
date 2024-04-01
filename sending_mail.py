import re
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

TableBlog = pd.read_csv('TableBlog.csv')
TableEvent = pd.read_csv('TableEvent.csv')
TableBlog
TableEvent

#Création du mail automatique personnalisé
#Création d'une boucle afin de tester l'envoie des mails dans un print() sans l'envoie réelle aux adresses mails
for country in TableBlog['Pays'].unique():
    country_events = TableEvent[TableEvent['Pays_Event'].str.contains(country, case=False, na=False)]
    if not country_events.empty:
        country_blogs = TableBlog[TableBlog['Pays'] == country]
        for _, blog in country_blogs.iterrows():
            # Déterminer le nombre d'abonnés Facebook ou Twitter
            facebook_followers = blog['Abonnées Facebook']
            twitter_followers = blog['Abonnées Twitter']
            followers = facebook_followers if facebook_followers > 0 else twitter_followers
            
            # Construire le message du texte en incluant les éléments personnalisés
            email_subject = f"Invitation to Jazz Events in {country}"
            email_body = f"Dear {blog['Nom Blog']},\n\nIt's time for some good jazz! With more than {followers} jazz lovers following you, it seems like your community is growing by each day.\n\nThat's why we thought you might be interested in the jazz festivals taking place in your area soon.\n\n Check out all the festivals organized in {country}:"
            
            # Construction de la liste des événements avec le nom, la ville et la période des festivals
            event_list = []
            for _, event in country_events.iterrows():
                event_info = f"{event['Nom_Event']}"
                if not pd.isnull(event['Ville_Envent']) and not pd.isnull(event['Periode_Event']):
                    event_info += f" ({event['Ville_Envent']} - {event['Periode_Event']})"
                elif not pd.isnull(event['Ville_Envent']):
                    event_info += f" ({event['Ville_Envent']})"
                elif not pd.isnull(event['Periode_Event']):
                    event_info += f" ({event['Periode_Event']})"
                event_list.append(event_info)
            
            email_body += "\n\n- " + "\n- ".join(event_list)  # Liste des événements avec des puces
            if len(event_list)>1: #créer une boucle qui permet de générer un paragraphe différent selon le nombre de festivals de la liste
                email_body += "\n\nAnd that's not all. As we appreciate your effort to spread the jazzy vibes across your passionate community, we'd love to offer you a free full access ticket to your favorite festival from the list.\n\n Find the full list of the festivals taking place all around the world at the following address:\n\nFeel free to write us back for more details.\n\nBest regards,\n The Jazzy World Team"
            else:
                 email_body += "\n\nAnd that's not all. As we appreciate your effort to spread the jazzy vibes across your passionate community, we'd love to offer you a free full access ticket to this festival.\n\n Find the full list of the festivals taking place all around the world at the following address:\n\n\nFeel free to write us back for more details.\n\nBest regards,\n The Jazzy World Team 🎵🎹"
            # Imprimer l'e-mail au lieu de l'envoyer
            print(f"To: {blog['Adresse Email']}\nSubject: {email_subject}\n{email_body}\n")

#créer une fonction qui génère le sujet et le contenu personnalisé du mail pour chaque bloguer 
def format_blogger_email(blog_name, followers, country):
    email_subject = f"Invitation to Jazz Events in {country}🎶🎷"
    email_body = f"Dear {blog_name},\n\nIt's time for some good jazz! With more than {followers} jazz lovers following you, it seems like your community is growing by each day.\n\nThat's why we thought you might be interested in the jazz festivals taking place in your area soon.\n\n Check out all the festivals organized in {country}:"
    return email_subject, email_body

# créer une fonction qui génère la liste personnalisée des festivals pour chaque blogueur (en fonction de son pays d'origine)
def format_event_list(events):
    event_list = []
    for _, event in events.iterrows():
        event_info = f"{event['Nom_Event']}"
        if not pd.isnull(event['Ville_Envent']) and not pd.isnull(event['Periode_Event']):
            event_info += f" ({event['Ville_Envent']} - {event['Periode_Event']})"
        elif not pd.isnull(event['Ville_Envent']):
            event_info += f" ({event['Ville_Envent']})"
        elif not pd.isnull(event['Periode_Event']):
            event_info += f" ({event['Periode_Event']})"
        event_list.append(event_info)
    
    formatted_list = "- " + "\n- ".join(event_list)
    return formatted_list

# Connexion au serveur SMTP #Création de la fonction pour envoyer les mails automatiquement en incluant les 2 fonctions créées ci-dessus
def send_jazz_event_invitations(smtp_server, smtp_port, smtp_username, smtp_password, TableBlog, TableEvent):
    #Gestion des erreurs à la connection au serveur de la boîte mail choisie
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)
        print("Connexion au serveur SMTP réussie.")
    except Exception as e:
        print(f"Erreur de connexion au serveur SMTP: {e}")
        return
    #Initiation de la boucle pour créer un message personnalisé en fonction du blogueur, de son nombre d'abonnées 
    # et de sa localisation
    for country in TableBlog['Pays'].unique():
        country_events = TableEvent[TableEvent['Pays_Event'].str.contains(country, case=False, na=False)]
        if not country_events.empty:
            country_blogs = TableBlog[TableBlog['Pays'] == country]
            for _, blog in country_blogs.iterrows():
                # Déterminer le nombre d'abonnés Facebook ou Twitter
                facebook_followers = blog['Abonnées Facebook']
                twitter_followers = blog['Abonnées Twitter']
                followers = facebook_followers if facebook_followers > 0 else twitter_followers
            
            # Utilisation de la fonction format_blogger_email pour formater le texte de l'email
                email_subject, email_body = format_blogger_email(blog['Nom Blog'], followers, country)
            
            # Construction de la liste des événements avec des informations supplémentaires
                formatted_event_list = format_event_list(country_events)
                email_body += f"\n\n{formatted_event_list}"  # Liste des événements avec des puces
    
            # Ajout du reste du texte de l'email
                if len(country_events) > 1:
                    email_body += "\n\nAnd that's not all. As we appreciate your effort to spread the jazzy vibes across your passionate community, we'd love to offer you a free full access ticket to your favorite festival from the list.\n\n Find the full list of the festivals taking place all around the world at the following address: https://www.smoothjazz.com/festivals \n\nFeel free to write us back for more details.\n\nBest regards,\n The Jazzy World Team 🎹🎵"
                else:
                    email_body += "\n\nAnd that's not all. As we appreciate your effort to spread the jazzy vibes across your passionate community, we'd love to offer you a free full access ticket to this festival.\n\n Find the full list of the festivals taking place all around the world at the following address: https://www.smoothjazz.com/festivals \n\n\nFeel free to write us back for more details.\n\nBest regards,\n The Jazzy World Team 🎹🎵 "

                msg = MIMEMultipart()
                msg['From'] = smtp_username
                msg['To'] = blog['Adresse Email']
                msg['Subject'] = email_subject
                msg.attach(MIMEText(email_body, 'plain'))
                #Gestion des erreurs dans le cadre de l'envoie des mails
                try:
                    server.sendmail(smtp_username, blog['Adresse Email'], msg.as_string())
                    print(f"Email sent to {blog['Adresse Email']}")
                except Exception as e:
                    print(f"Failed to send email to {blog['Adresse Email']}: {e}")
    #Gestion des erreurs dans le cadre de la fermeture du serveur
    try:
        server.quit()
        print("Connexion SMTP fermée.")
    except Exception as e:
        print(f"Erreur lors de la fermeture de la connexion SMTP: {e}")

# Appel de la fonction pour l'envoie de mail
send_jazz_event_invitations("smtp.gmail.com", 465, "jazzyworld67@gmail.com", "ogunqrpjhigzwpfc", TableBlog, TableEvent)
