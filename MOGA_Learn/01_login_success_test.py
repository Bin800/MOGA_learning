import asyncio
from time import sleep

from playwright.async_api import async_playwright
from credentials import USERNAME, PASSWORD, MOGA_STG_URL

async def login_succes(page):
    await page.get_by_role(role='textbox', name='email').fill(USERNAME)
    await page.get_by_role(role='textbox', name='password').fill(PASSWORD)
    await page.get_by_role(role='button', name='sign in').click()
    await page.wait_for_selector("div.Toastify__toast-container--bottom-left div.Toastify__toast")
    toast_text = await page.locator("div.Toastify__toast-container--bottom-left div.Toastify__toast").text_content()
    print(toast_text)

if __name__ == "__main__":
    async def main():
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=False,
                channel="msedge"  # Dùng channel để mở Microsoft Edge
            )
            page = await browser.new_page()
            await page.goto(MOGA_STG_URL)
            await login_succes(page)
    asyncio.run(main())
