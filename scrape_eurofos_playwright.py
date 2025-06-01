import asyncio
import json
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        await page.goto("https://www.cccp13.fr/embouestV38/", timeout=60000)
        await page.wait_for_selector('input[type="text"]', timeout=30000)

        # Connexion
        await page.fill('input[type="text"]', "cccp13")
        await page.fill('input[type="password"]', "dockers")
        await page.click('input[type="submit"]')

        # Attente du tableau
        await page.wait_for_selector("table", timeout=10000)

        # Extraction
        table = await page.query_selector("table")
        rows = await table.query_selector_all("tr")

        data = {"shifts": []}
        for row in rows[1:]:
            cells = await row.query_selector_all("td")
            if len(cells) >= 3:
                shift = await cells[0].inner_text()
                equipe = await cells[1].inner_text()
                parc = await cells[2].inner_text()
                data["shifts"].append({
                    "shift": shift.strip(),
                    "equipe": equipe.strip(),
                    "parc": parc.strip()
                })

        # Sauvegarde en JSON
        with open("eurofos.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        await browser.close()

asyncio.run(run())
