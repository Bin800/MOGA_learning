import asyncio
from time import sleep

from playwright.async_api import async_playwright
from credentials import USERNAME, PASSWORD, MOGA_STG_URL

async def login_succes(page):
    await page.get_by_role(role="textbox", name="email").fill(USERNAME)
    await page.get_by_role(role="textbox", name="password").fill(PASSWORD)
    await page.get_by_role(role="button", name="sign in").click()
    await page.wait_for_selector("div.Toastify__toast-container--bottom-left div.Toastify__toast")
    toast_visible = await page.locator("div.Toastify__toast-container--bottom-left div.Toastify__toast").is_visible()
    print(f"Toast co hien khong: {toast_visible}")
    # await page.wait_for_selector("div.Toastify__toast-container--bottom-left div.Toastify__toast")
    # toast_text = await page.locator("div.Toastify__toast-container--bottom-left div.Toastify__toast").text_content()
    # print(toast_text)

async def access_lead(page):
    side_menu_visible = page.locator("aside")
    print(f"Side menu visible: {side_menu_visible}")
    await page.get_by_role(role="menuitem", name="Lead").click()

async def change_view(page):
    change_list_view = page.locator("svg[data-icon='bars']")
    await change_list_view.wait_for()
    is_button_visible = await change_list_view.is_visible()
    print(f"Change view button: {is_button_visible}")
    await change_list_view.click()

async def add_lead(page):
    await page.get_by_role(role="button", name="Add lead").click()
    drawer_add_lead = page.locator("div[class='ant-drawer-content-wrapper']")
    await drawer_add_lead.wait_for()
    is_drawer_visible = await drawer_add_lead.is_visible()
    print(f"Drawer add lead visible: {is_drawer_visible}")

async def fill_lead_info (page):
    await page.get_by_role(role="textbox", name="Account name").fill("Account")
    await page.locator("input[name='name']").fill("Contact")
    await page.locator("input[autocomplete='tel']").fill("+8412345678")
    await page.get_by_role(role="textbox", name="Email").fill("account@gmail.com")
    await page.locator("div.ant-select", has=page.locator("span.ant-select-selection-placeholder", has_text="Gender")).click()
    await page.wait_for_selector("div.ant-select-item-option", state="visible")
    await page.locator('div.ant-select-item-option[title="Male"]').click()
    await page.get_by_role(role="textbox", name="Job title").fill("Title 1")
    await page.locator("div.ant-select", has=page.locator("span.ant-select-selection-placeholder", has_text="Industry")).click()
    await page.wait_for_selector("div.ant-select-item-option", state="visible")
    await page.locator('div.ant-select-item-option[title="Event"]').click()
    await page.locator("input[name='tax_identification_number']").fill("TAX1.1")
    await page.locator("div.ant-select", has=page.locator("span.ant-select-selection-placeholder", has_text="Country")).click()
    await page.wait_for_timeout(500)
    await page.keyboard.type("Vietnam")
    await page.wait_for_timeout(500)
    await page.locator("div.ant-select-item-option", has_text="Vietnam").click()
    await page.locator("div.ant-select", has=page.locator("span.ant-select-selection-placeholder", has_text="City")).click()
    await page.wait_for_timeout(500)
    await page.keyboard.type("Bến Tre")
    await page.wait_for_timeout(500)
    await page.locator("div.ant-select-item-option", has_text="Bến Tre").click()
    await page.locator("input[name='address']").fill("Sala sarina, A0011")
    await page.locator("div.ant-select", has=page.locator("span.ant-select-selection-placeholder", has_text="Source")).click()
    await page.wait_for_timeout(500)
    await page.locator('div.ant-select-item-option[title="Source 1"]').click()
    await page.locator("div.ant-select", has=page.locator("span.ant-select-selection-placeholder", has_text="Status")).click()
    await page.wait_for_timeout(500)
    await page.locator('div.ant-select-item-option[title="Hot lead"]').click()
    await page.locator("div.ant-select", has=page.locator("span.ant-select-selection-placeholder", has_text="Lead Segmentation")).click()
    await page.wait_for_timeout(500)
    await page.locator('div.ant-select-item-option[title="Cheap"]').click()
    await page.locator("div.ant-select", has=page.locator("span.ant-select-selection-placeholder", has_text="Lead label")).click()
    await page.wait_for_timeout(500)
    await page.locator('div.ant-select-item-option[title="acc01"]').click()
    await page.get_by_role(role="textbox", name="Text").fill("ABC")
    await page.get_by_role(role="textbox", name="Link").fill("https://oplacrm.com")
    await page.locator("div.ant-select", has=page.locator("span.ant-select-selection-placeholder", has_text="Pick list")).click()
    await page.wait_for_timeout(500)
    await page.locator('div.ant-select-item-option[title="Option 1"]').click()
    await page.locator("div.ant-picker").click()
    await page.wait_for_selector("div.ant-picker-dropdown", state="visible")
    await page.locator("td.ant-picker-cell", has_text="15").click()
    await page.locator("input[placeholder='Number']").fill("123")
    await page.get_by_role(role="button", name="Save").click()
    # await page.get_by_role(role="button", name="Cancel").click()
    sleep(2)

async def personal_setting (page):
    sleep(5)
    await page.locator("div[class^='ant-dropdown-trigger']").click()
    await page.wait_for_selector("div[class$='ant-dropdown-placement-bottomRight']")
    await page.get_by_role(role='button', name='Personal Setting').click()
    sleep(1)
    await page.locator("input[name='firstName']").fill('Yên')
    await page.locator("input[name='lastName']").fill('Lý')
    await page.locator("input[autocomplete='tel']").click()
    await page.locator("input[autocomplete='tel']").fill('707986543')
    await page.get_by_role(role="button", name='Save').click()
    # await page.get_by_role(role="button", name='Cancel').click()


if __name__ == "__main__":
    async def main():
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=False,
                channel="chrome"  # Dùng channel để mở Chrome
            )
            page = await browser.new_page()
            await page.goto(MOGA_STG_URL)
            await login_succes(page)
            await access_lead(page)
            await change_view(page)
            await add_lead(page)
            await fill_lead_info(page)
            await personal_setting(page)
            sleep(2)

    asyncio.run(main())
