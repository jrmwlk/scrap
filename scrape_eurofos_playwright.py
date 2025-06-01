from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Connexion au site
        page.goto("https://www.cccp13.fr/embouestV38/LoginServlet")
        page.fill('input[name="login"]', "013")
        page.fill('input[name="password"]', "EUROFOS")
        page.click('text=Embauche')

        # Attente du tableau (à ajuster si nécessaire)
        page.wait_for_selector("table")

        # Extraire les données du tableau
        rows = page.query_selector_all("table tbody tr")

        data = []
        current_shift = None

        for row in rows:
            cells = row.query_selector_all("td")
            if len(cells) < 4:
                continue

            zone = cells[1].inner_text().strip().upper()
            shift = cells[0].inner_text().strip().upper()
            poste = cells[2].inner_text().strip().upper()

            if "PARC" in zone and "CAVALIER" in zone and poste == "STR":
                str_values = [c.inner_text().strip() for c in cells[3:6]]
                if len(str_values) == 3 and all(v.isdigit() for v in str_values):
                    data.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "shift": shift,
                        "zone": zone,
                        "type": poste,
                        "lignes": str_values
                    })

        # Sauvegarde
        with open("eurofos_raw.json", "w") as f:
            json.dump(data, f, indent=2)
        print(json.dumps(data, indent=2))

        browser.close()

if __name__ == "__main__":
    run()
