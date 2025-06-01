import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        await page.goto("https://www.cccp13.fr/embouestV38/", timeout=60000)

        # Attendre le champ de login
        await page.wait_for_selector('input[type="text"]', timeout=30000)
        await page.fill('input[type="text"]', "LOGIN")
        await page.fill('input[type="password"]', "PASSWORD")

        # Cliquer sur le bouton "Embauche"
        await page.click('text=Embauche')

        # Attendre le chargement de la page suivante
        await page.wait_for_timeout(3000)

        # Exemple de récupération de données, à adapter
        data = {"status": "connecté et embauche cliquée"}

        with open("eurofos.json", "w") as f:
            json.dump(data, f)

        await browser.close()

asyncio.run(run())