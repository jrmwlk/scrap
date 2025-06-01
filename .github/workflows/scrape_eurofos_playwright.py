
import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime, timedelta

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.cccp13.fr/embouestV38/LoginServlet")
        await page.fill('input[type="text"]', "013")
        await page.fill('input[type="password"]', "EUROFOS")
        await page.click('text=Embauche')
        await page.wait_for_selector("table", timeout=10000)

        rows = await page.query_selector_all("table tr")
        chantiers = []
        date_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        for row in rows[1:]:
            cols = await row.query_selector_all("td")
            if len(cols) < 3:
                continue

            shift = await cols[1].inner_text()
            zone = await cols[2].inner_text()

            types = {}
            type_cells = await cols[2].query_selector_all("table tr")
            current_label = None
            current_values = []

            for type_row in type_cells:
                tds = await type_row.query_selector_all("td")
                if len(tds) == 1:
                    current_label = (await tds[0].inner_text()).strip()
                    current_values = []
                elif len(tds) == 1 and current_label:
                    current_values.append((await tds[0].inner_text()).strip())
                elif len(tds) == 2:
                    current_label = (await tds[0].inner_text()).strip()
                    value = (await tds[1].inner_text()).strip()
                    current_values = [value]

                if current_label and current_values:
                    try:
                        last_value = int(current_values[-1])
                        types[current_label] = last_value
                    except ValueError:
                        continue

            chantier = {
                "date": date_str,
                "shift": shift.strip(),
                "zone": zone.split("\n")[0].strip(),
                "types": types
            }
            chantiers.append(chantier)

        with open("eurofos.json", "w", encoding="utf-8") as f:
            json.dump(chantiers, f, ensure_ascii=False, indent=2)

        print("Fichier eurofos.json généré avec succès.")
        await browser.close()

asyncio.run(run())
