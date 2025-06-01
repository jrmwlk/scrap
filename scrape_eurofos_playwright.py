import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        try:
            await page.goto("https://cccp13.fr", timeout=30000)
            await page.wait_for_selector('input[name="login"]', timeout=10000)
            await page.screenshot(path="screenshot.png")
            print("✅ Login page loaded and screenshot saved.")
        except Exception as e:
            await page.screenshot(path="screenshot.png")
            print(f"❌ Error during scraping: {e}")
        finally:
            await browser.close()

asyncio.run(run())
