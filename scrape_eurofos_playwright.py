
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    try:
        page.goto("https://www.cccp13.fr/embouestV38/", timeout=60000)
        page.wait_for_selector('input[type="text"]', timeout=30000)
        print("Champ de connexion détecté.")
    except Exception as e:
        print("Erreur pendant le chargement :", e)
        page.screenshot(path="error.png")
    finally:
        browser.close()
