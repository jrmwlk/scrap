import json
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.cccp13.fr/embouestV38/")

        # Connexion (identifiants vides, interface ouverte)
        page.click("input[type='submit']")

        # Attente et clic sur le bouton "Embauche"
        page.wait_for_selector("text=Embauche", timeout=10000)
        page.click("text=Embauche")

        # Attente de la page chargée (à ajuster selon le DOM réel)
        page.wait_for_timeout(2000)

        # Extraction (exemple à ajuster selon la structure réelle de la page)
        data = {
            "2025-06-01": {
                "parc": {
                    "S1": 4,
                    "S2": 3,
                    "S3": 2,
                    "JV": 1,
                    "total_JV_JD": 2
                },
                "portiques": {
                    "S1": 6,
                    "S2": 5,
                    "S3": 3
                }
            }
        }

        with open("eurofos.json", "w") as f:
            json.dump(data, f)

        browser.close()

if __name__ == "__main__":
    run()