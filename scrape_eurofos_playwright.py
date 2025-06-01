import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import json
from datetime import datetime

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(user_data_dir="/tmp/playwright", headless=True, ignore_https_errors=True)
        page = await browser.new_page()
        try:
            await page.goto("https://cccp13.fr", timeout=60000)
            await page.fill('input[name="login"]', "identifiant")
            await page.fill('input[name="password"]', "motdepasse")
            await page.click('input[type="submit"]')
            await page.wait_for_selector('text="Embauche"', timeout=60000)
            await page.click('text="Embauche"')
            await page.wait_for_timeout(3000)
            html = await page.content()

            # Traitement fictif simplifié
            data = {
                "date": datetime.today().strftime('%Y-%m-%d'),
                "parc": {
                    "S1": {"renfort": 1, "total": 8},
                    "S2": {"renfort": 4, "total": 8},
                    "JD": {"renfort": 0, "total": 10}
                },
                "portiques": {
                    "S1": [{"portique": "P1", "bateau": "NAVIRE A", "nb": 3}]
                }
            }

            with open("eurofos.json", "w") as f:
                json.dump(data, f, indent=2)

        except PlaywrightTimeoutError as e:
            print(f"Erreur de timeout : {e}")
        except Exception as e:
            print(f"Erreur générale : {e}")
        await browser.close()

asyncio.run(run())