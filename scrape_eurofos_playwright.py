import json

# Exemple simulé d'extraction (à remplacer par ton vrai scraping Playwright)
data = [
    {
        "date": "2025-06-02",
        "shift": "S1",
        "zone": "PARC / CAVALIER",
        "type": "STR",
        "lignes": ["8", "7", "1"]
    },
    {
        "date": "2025-06-02",
        "shift": "S2",
        "zone": "PARC / CAVALIER",
        "type": "STR",
        "lignes": ["8", "4", "4"]
    }
]

# Enregistrement
with open("eurofos_raw.json", "w") as f:
    json.dump(data, f, indent=2)

# Affichage console (pour GitHub Actions logs)
print(json.dumps(data, indent=2))
