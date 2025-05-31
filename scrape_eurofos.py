
import requests
from bs4 import BeautifulSoup
import json

# Identifiants de connexion
login_url = "https://www.cccp13.fr/embouestV38/"
login_data = {
    "login": "013",
    "password": "EUROFOS"
}

# Session pour conserver les cookies
session = requests.Session()

# Étape 1 : Charger la page de connexion
login_page = session.get(login_url)

# Étape 2 : Poster les identifiants
response = session.post(login_url, data=login_data)

# Vérifier si la connexion a réussi
if "embauche" not in response.text.lower():
    print("Connexion échouée. Vérifie les identifiants.")
    exit()

# Étape 3 : Accéder à la page d'embauche
# ATTENTION : L’URL exacte de la page “Embauche” est à confirmer
# Ceci est un exemple temporaire
embauche_url = "https://www.cccp13.fr/embouestV38/embauche.php"
embauche_page = session.get(embauche_url)

# Étape 4 : Analyser le HTML et extraire les données
soup = BeautifulSoup(embauche_page.text, "html.parser")

# Exemple de parsing - à adapter selon le vrai contenu HTML
chantiers = []
for row in soup.select("table tr")[1:]:  # On saute l'en-tête
    cols = row.find_all("td")
    if len(cols) >= 4:
        chantier = {
            "date": cols[0].text.strip(),
            "shift": cols[1].text.strip(),
            "nbSTR": int(cols[2].text.strip()),
            "portiques": [{"nom": p.strip(), "bateau": "Inconnu"} for p in cols[3].text.split(",")]
        }
        chantiers.append(chantier)

# Étape 5 : Sauvegarder dans un fichier JSON
with open("eurofos.json", "w", encoding="utf-8") as f:
    json.dump(chantiers, f, ensure_ascii=False, indent=2)

print("Fichier eurofos.json généré avec succès.")
