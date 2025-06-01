import json
from playwright.sync_api import sync_playwright

USERNAME = "013"
PASSWORD = "EUROFOS"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.goto("https://www.cccp13.fr/embouestV38/")

        # Connexion
        page.fill("input[type='text']", USERNAME)
        page.fill("input[type='password']", PASSWORD)
        page.click("input[type='submit']")

        # Clique sur le bouton "Embauche"
        page.click("text=Embauche")

        page.wait_for_load_state("networkidle")

        # Extraction
        rows = page.locator("table tr").all()
        shifts = {}
        portiques = []

        for row in rows:
            text = row.inner_text()
            if "PARC / CAVALIER" in text:
                columns = text.split("\n")
                folio = columns[0].strip()
                shift = columns[1].strip()
                values = list(map(int, columns[4:7]))
                if shift not in shifts:
                    shifts[shift] = {"TOTAL": 0, "GEMFOS": 0}
                shifts[shift]["TOTAL"] += values[0]
                shifts[shift]["GEMFOS"] += values[2]
            elif any(p in text for p in ["P07", "P08", "PS0", "PS1", "PS2", "PS3", "PS4", "PS5"]):
                columns = text.split("\n")
                shift = columns[1].strip()
                navire = columns[3].strip() if len(columns) > 3 else ""
                portiques.append({"shift": shift, "navire": navire})

        with open("eurofos.json", "w") as f:
            json.dump({
                "cavalier": shifts,
                "portiques": portiques
            }, f, indent=2)

        browser.close()

if __name__ == "__main__":
    run()
