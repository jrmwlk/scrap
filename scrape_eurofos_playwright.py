
import json
import os
from playwright.sync_api import sync_playwright
from datetime import datetime

OUTPUT_FILE = "eurofos.json"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.cccp13.fr/embouestV38/")

    # Connexion
    page.fill('input[name="login"]', "013")
    page.fill('input[name="mdp"]', "EUROFOS")
    page.click("text=EMBAUCHE")
    page.wait_for_timeout(2000)

    # Attendre que les tableaux soient chargés
    page.wait_for_selector("table")
    tables = page.query_selector_all("table")

    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "parc": {
            "S1": {"renfort": 0, "total": 0},
            "S2": {"renfort": 0, "total": 0},
            "S3": {"renfort": 0, "total": 0},
            "JV": {"renfort": 0, "total": 0},
        }
    }

    for table in tables:
        html = table.inner_html()
        if "PARC / CAVALIER" in html:
            rows = table.query_selector_all("tr")
            shift = None
            for row in rows:
                cells = row.query_selector_all("td")
                if not cells:
                    continue
                row_text = row.inner_text()
                if "PARC / CAVALIER" in row_text:
                    if "S1" in row_text:
                        shift = "S1"
                    elif "S2" in row_text:
                        shift = "S2"
                    elif "S3" in row_text:
                        shift = "S3"
                    elif "JV" in row_text or "JD" in row_text:
                        shift = "JV"
                elif shift and ("TOTAL" in row_text or cells[0].inner_text().strip().upper() == "TOTAL"):
                    try:
                        total = int(cells[2].inner_text().strip())
                        data["parc"][shift]["total"] = total
                    except:
                        pass
                elif shift and ("GEMFOS" in row_text or cells[0].inner_text().strip().upper() == "GEMFOS"):
                    try:
                        renfort = int(cells[2].inner_text().strip())
                        data["parc"][shift]["renfort"] = renfort
                    except:
                        pass

    # Nettoyage des shifts sans données
    data["parc"] = {k: v for k, v in data["parc"].items() if v["total"] > 0}

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    browser.close()
