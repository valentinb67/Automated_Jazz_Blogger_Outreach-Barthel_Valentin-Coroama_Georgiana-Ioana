# Automated Jazz Blogger Outreach

Projet de groupe, Technique de programmation

## Description:
Ce projet vise à automatiser l'envoi d'invitations par e-mail à 75 des blogueurs de Jazz les plus influents du monde, les conviant à participer à des festivals de Jazz dans leur pays d'origine. Utilisant des techniques de marketing ciblé, ce script segmente les blogueurs selon leur localisation et personnalise les invitations pour maximiser l'engagement et la participation.

Notre projet de Web scraping se structure autour de trois parties principales: <br>
-un premier script (scraping_blogs.py) comportant l'ensemble des commandes nécessaires pour scraper le site https://music.feedspot.com/jazz_blogs/ <br>
-un deuxième script (scraping_festivals.py) comportant l'ensemble des commandes nécessaires pour scraper le site https://www.smoothjazz.com/festivals <br>
-un troisième script (sending_mail.py) comportant l'ensemble des commandes nécessaires pour la création et l'envoi du mail automatique personnalisé aux blogueurs <br>

Nous avons également créé un quatrième script (calling_script_functions.py) qui importe et appelle les fonctions des 3 scripts précédents <br>
Ce dernier se compose de 4 sections, les trois premières visant à définir des fonctions qui appellent les fonctions des scripts précédents par partie (partie blogueurs, partie festivals, partie email) et une dernière section qui génère une fonction globale permettant d'appeler l'ensemble des fonctions par partie pour exécuter l'intégralité du code.


## Environnement de Développement:
Prérequis
Python 3.8+

## Dépendances

#### Pour installer les dépendances nécessaires, exécutez la commande suivante :  <br>
pip install beautifulsoup4 pandas numpy requests tqdm <br>
Installation <br>
Clonez ce dépôt sur votre machine locale :

git clone https://github.com/valentinb67/Automated_Jazz_Blogger_Outreach-Barthel_Valentin-Coroama_Georgiana-Ioana <br>
Naviguez dans le répertoire du projet et installez les dépendances : <br>

cd Automated_Jazz_Blogger_Outreach-Barthel_Valentin-Coroama_Georgiana-Ioana
pip install -r requirements.txt

## Utilisation
Pour lancer le script d'envoi d'e-mails, exécutez :

python sending_mail.py
Fonctionnalités
Scraping de données : Extrait les informations des blogueurs et des festivals depuis des sources en ligne.
Analyse et traitement de données : Segmente les données pour cibler les invitations en fonction du pays d'origine des blogueurs.
Envoi automatique d'e-mails : Génère et envoie des invitations personnalisées aux blogueurs sélectionnés.


#### Fork le projet:
Créez votre branche de fonctionnalité (git checkout -b feature/AmazingFeature) <br>
Commit vos changements (git commit -m 'Add some AmazingFeature') <br>
Push à la branche (git push origin feature/AmazingFeature) <br>
Ouvrez une Pull Request <br>

Auteurs: <br>
Valentin Barthel, Georgiana-Ioana Coroama


#### Contacts: <br>
Valentin Barthel - valentin.barthel@etu.unistra.fr <br>
Georgiana-Ioana Coroama - georgiana.coroama@etu.unistra.fr <br>

Projet Lien: https://github.com/valentinb67/Automated_Jazz_Blogger_Outreach-Barthel_Valentin-Coroama_Georgiana-Ioana
