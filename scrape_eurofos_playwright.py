
import json
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        # Connexion
        page.goto("https://www.cccp13.fr/embouestV38/")
        page.fill("input[type='text']", "LOGIN")
        page.fill("input[type='password']", "PASSWORD")

        # Attendre et cliquer sur "Embauche"
        page.get_by_role("link", name="Embauche").click()

        # Attendre le chargement des données visibles
        page.wait_for_timeout(3000)

        # Exemple de récupération de données (à adapter)
        content = page.content()

        data = {"status": "connecté", "html": content}
        with open("eurofos.json", "w") as f:
            json.dump(data, f, indent=2)

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
