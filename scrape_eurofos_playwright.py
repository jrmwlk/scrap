
from playwright.sync_api import sync_playwright, TimeoutError
import json
from datetime import datetime

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            print("Connexion au site...")
            page.goto("https://cccp13.fr", timeout=60000)
            page.locator("input[name='login']").wait_for(timeout=60000)

            page.fill("input[name='login']", "813")
            page.fill("input[name='password']", "EUROFOS")
            page.click("input[type='submit']")

            print("Connexion réussie. Navigation vers Embauche...")
            page.click("text=Embauche")

            print("Chargement des données...")
            page.wait_for_selector("table", timeout=60000)

            rows = page.query_selector_all("table tr")
            parc_data = {"S1": {"renfort": 0, "total": 0}, "S2": {"renfort": 0, "total": 0}, "S3": {"renfort": 0, "total": 0}, "JV": {"renfort": 0, "total": 0}, "JD": {"renfort": 0, "total": 0}}
            portiques = []

            for row in rows:
                cells = row.query_selector_all("td")
                if len(cells) < 3:
                    continue
                shift = cells[1].inner_text().strip()
                navire = cells[2].inner_text().strip()
                if "PARC / CAVALIER" in navire and shift in parc_data:
                    sous_lignes = row.query_selector_all("td >> text=STR")
                    if sous_lignes:
                        effectifs = [int(c.inner_text()) for c in row.query_selector_all("td >> nth=1 >> div") if c.inner_text().isdigit()]
                        if effectifs:
                            parc_data[shift]["total"] += effectifs[0]
                            if len(effectifs) > 2:
                                parc_data[shift]["renfort"] += effectifs[2]

                if "PORTIQUE" in navire.upper():
                    portique = cells[2].inner_text().strip()
                    bateau = cells[2].inner_text().strip()
                    nb = 0
                    try:
                        nb = int(cells[3].inner_text().strip())
                    except:
                        pass
                    portiques.append({"portique": portique, "bateau": bateau, "nb": nb})

            data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "parc": {shift: {"renfort": parc_data[shift]["renfort"], "total": parc_data[shift]["total"]} for shift in parc_data if parc_data[shift]["total"] > 0},
                "portiques": portiques,
            }

            with open("eurofos.json", "w") as f:
                json.dump(data, f, indent=2)
            print("✅ eurofos.json généré avec succès.")

        except TimeoutError as e:
            print("❌ Timeout lors du chargement : ", str(e))
        finally:
            browser.close()

if __name__ == "__main__":
    run()
