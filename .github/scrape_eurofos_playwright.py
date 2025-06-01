
import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="/tmp/playwright",
            headless=True,
            ignore_https_errors=True
        )
        page = await browser.new_page()

        await page.goto("https://cccp13.fr/")
        await page.fill('input[name="login"]', "votre_identifiant")
        await page.fill('input[name="password"]', "votre_mot_de_passe")
        await page.click('input[type="submit"]')
        await page.wait_for_selector("text=Embauche")

        await page.click("text=Embauche")
        await page.wait_for_timeout(2000)

        # Ajoute ici ton code pour extraire les données et les structurer
        data = {
            "date": datetime.today().strftime('%Y-%m-%d'),
            "message": "Scraping réussi"
        }

        with open("eurofos.json", "w") as f:
            json.dump(data, f, indent=2)

        await browser.close()

asyncio.run(run())
