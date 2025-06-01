import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        await page.goto("https://www.cccp13.fr/embouestV38/", timeout=30000)

        # Connexion
        await page.locator("input[name='identog']").fill("013")
        await page.locator("input[name='mdp']").fill("EUROFOS")

        # Clic sur "Embauche"
        await page.locator("button[onclick*=\"Function.value='E'\"]").click()

        # Attente du tableau
        await page.wait_for_selector("table")

        # Debug HTML
        html_content = await page.content()
        with open("debug.html", "w") as f:
            f.write(html_content)

        # Récupération des données
        rows = await page.locator("table tr").all()
        data = {"gemfos": [], "portiques": []}

        for row in rows:
            html = await row.inner_html()

            if "PARC / CAVALIER" in html:
                cells = await row.locator("td >> nth=2").all()
                shift = await row.locator("td >> nth=1").inner_text()

                if len(cells) >= 2:
                    numbers = await row.locator("td >> nth=2").all_inner_texts()
                    if len(numbers) >= 3:
                        total = numbers[0]
                        gemfos = numbers[2]
                        data["gemfos"].append({
                            "shift": shift.strip(),
                            "total": total.strip(),
                            "gemfos": gemfos.strip()
                        })

            if any(p in html for p in ["P07", "P08", "PS0", "PS1", "PS2", "PS3", "PS4", "PS5"]):
                shift = await row.locator("td >> nth=1").inner_text()
                bateau = await row.locator("td >> nth=2").inner_text()
                portique = await row.locator("td >> nth=0").inner_text()
                data["portiques"].append({
                    "shift": shift.strip(),
                    "bateau": bateau.strip(),
                    "portique": portique.strip()
                })

        with open("eurofos.json", "w") as f:
            json.dump(data, f, indent=2)

        await browser.close()

if __name
