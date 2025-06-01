
import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        await page.goto("https://www.cccp13.fr/embouestV38/", timeout=60000)

        # Connexion
        await page.fill('input[type="text"]', "013")
        await page.fill('input[type="password"]', "EUROFOS")
        await page.click('input[type="submit"]')

        # Clic sur le bouton "Embauche"
        await page.get_by_role("link", name="Embauche").click()

        # Attente du tableau
        await page.wait_for_selector("table")

        # Récupération des données
        rows = await page.locator("table tr").all()
        data = {"gemfos": {}, "portiques": []}

        for row in rows:
            html = await row.inner_html()
            if "PARC / CAVALIER" in html:
                cells = await row.locator("td").all()
                if len(cells) >= 2:
                    shift = await cells[1].inner_text()
                    numbers = await row.locator("td >> nth=1 >> table tr").all()
                    if len(numbers) >= 3:
                        total = await numbers[0].inner_text()
                        gemfos = await numbers[2].inner_text()
                        data["gemfos"][shift.strip()] = {
                            "total": total.strip(),
                            "gemfos": gemfos.strip()
                        }

            if any(p in html for p in ["P07", "P08", "PS0", "PS1", "PS2", "PS3", "PS4", "PS5"]):
                shift = await row.locator("td >> nth=1").inner_text()
                bateau = await row.locator("td >> nth=2").inner_text()
                data["portiques"].append({
                    "shift": shift.strip(),
                    "bateau": bateau.strip()
                })

        with open("eurofos.json", "w") as f:
            json.dump(data, f)

        await browser.close()

asyncio.run(run())
