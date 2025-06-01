
import asyncio
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import json

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        try:
            page.goto("https://www.cccp13.fr/embouestV38/", timeout=60000)
            page.wait_for_selector("input[name='login']", timeout=60000)
            page.screenshot(path="screenshot.png")

            page.fill("input[name='login']", "votre_identifiant")
            page.fill("input[name='password']", "votre_mot_de_passe")
            page.click("button[type='submit']")

            page.wait_for_timeout(5000)
            page.screenshot(path="dashboard.png")

            data = {
                "date": datetime.today().strftime("%Y-%m-%d"),
                "parc": {
                    "gemfos": 4,
                    "total": 8
                },
                "portiques": [
                    {
                        "portique": "P1",
                        "bateau": "NAVIRE AF",
                        "nb": 3
                    }
                ]
            }

            with open("eurofos.json", "w") as f:
                json.dump(data, f, indent=2)

        except PlaywrightTimeoutError as e:
            print("Erreur durant le scraping :", e)
            page.screenshot(path="error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
