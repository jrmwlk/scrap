
from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, ignore_https_errors=True)
        page = browser.new_page()
        page.goto("https://cccpi13.fr", timeout=60000)

        page.fill('input[name="login"]', "913")
        page.fill('input[name="password"]', "EUROFOS")
        page.click('input[type="submit"]')
        page.wait_for_timeout(3000)
        page.click('text="Embauche"')

        page.wait_for_selector('text="PARC / CAVALIER"', timeout=10000)

        rows = page.query_selector_all("table tr")
        parc = {}
        portiques = []
        shifts = ["S1", "S2", "S3", "JV", "JD"]

        for row in rows:
            cells = row.query_selector_all("td")
            if len(cells) < 3:
                continue

            shift = cells[1].inner_text().strip()
            navire_parc = cells[2].inner_text().strip()
            poste = cells[3].inner_text().strip()
            valeurs = [c.inner_text().strip() for c in cells[2].query_selector_all("td")]

            if shift not in shifts:
                continue

            if "PARC / CAVALIER" in navire_parc and "STR" in navire_parc:
                total = int(valeurs[0]) if valeurs else 0
                renfort = int(valeurs[2]) if len(valeurs) > 2 else 0
                parc[shift] = {"renfort": renfort, "total": total}

            if "PORTIQUE" in navire_parc and "PI" in navire_parc:
                portiques.append({
                    "shift": shift,
                    "portique": "PI1",
                    "bateau": navire_parc.split("/")[-1].strip(),
                    "nb": int(valeurs[0]) if valeurs else 1
                })

        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "parc": parc,
            "portiques": portiques
        }

        with open("eurofos.json", "w") as f:
            json.dump(data, f, indent=2)

        print(json.dumps(data, indent=2))
        browser.close()

if __name__ == "__main__":
    run()
