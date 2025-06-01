from playwright.sync_api import sync_playwright, TimeoutError
import json
from datetime import datetime

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-web-security"])
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        try:
            page.goto("https://www.cccp13.fr/embouestV38/LoginServlet", timeout=60000)
            page.wait_for_selector('input[name="login"]', timeout=20000)

            page.fill('input[name="login"]', "013")
            page.fill('input[name="password"]', "EUROFOS")
            page.click('text=Embauche')

            page.wait_for_selector("table", timeout=15000)

            rows = page.query_selector_all("table tbody tr")

            renforts = {
                "S1": {"renfort": 0, "total": 0},
                "S2": {"renfort": 0, "total": 0},
                "S3": {"renfort": 0, "total": 0},
                "JV": {"renfort": 0, "total": 0},
                "JD": {"renfort": 0, "total": 0},
            }

            portiques = {
                "S1": [],
                "S2": [],
                "S3": [],
                "JV": [],
                "JD": []
            }

            for row in rows:
                cells = row.query_selector_all("td")
                if len(cells) < 4:
                    continue

                folio = cells[0].inner_text().strip()
                shift = cells[1].inner_text().strip().upper()
                zone = cells[2].inner_text().strip().upper()
                poste = cells[3].inner_text().strip().upper()
                lignes = [c.inner_text().strip() for c in cells[4:] if c.inner_text().strip().isdigit()]

                # Renforts PARC / CAVALIER STR
                if "PARC" in zone and "CAVALIER" in zone and poste == "STR" and shift in renforts:
                    if len(lignes) >= 3:
                        total = int(lignes[0])
                        renfort = int(lignes[2])
                        renforts[shift]["total"] += total
                        renforts[shift]["renfort"] += renfort

                # Équipes portiques
                elif "PORTIQUE" in zone and shift in portiques:
                    zone_parts = zone.replace("PORTIQUE", "").strip().split("/")
                    portique = zone_parts[0].strip() if len(zone_parts) > 0 else "?"
                    bateau = zone_parts[1].strip() if len(zone_parts) > 1 else "?"

                    if lignes:
                        effectif = sum(int(v) for v in lignes)
                        portiques[shift].append({
                            "portique": portique,
                            "bateau": bateau,
                            "nb": effectif
                        })

            final_output = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "parc": renforts,
                "portiques": portiques
            }

            with open("eurofos.json", "w") as f:
                json.dump(final_output, f, indent=2)
            print(json.dumps(final_output, indent=2))

        except TimeoutError as e:
            print("Erreur de chargement :", e)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
