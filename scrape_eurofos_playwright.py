from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    # Bonne URL corrigée
    page.goto("https://www.cccp13.fr/embouestV38/", timeout=60000)

    page.fill('input[name="login"]', "LOGIN")
    page.fill('input[name="password"]', "PASS")
    page.click('input[type="submit"]')

    context.close()
    browser.close()