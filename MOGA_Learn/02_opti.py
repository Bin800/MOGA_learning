import asyncio
from time import sleep
from typing import Optional
from playwright.async_api import async_playwright, Page, Browser
from credentials import USERNAME, PASSWORD, MOGA_STG_URL


class MOGAWebAutomation:
    """Class để tự động hóa các thao tác trên website MOGA CRM"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
    async def __aenter__(self):
        """Context manager entry"""
        await self.start_browser()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close_browser()
    
    async def start_browser(self):
        """Khởi tạo browser và page"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            channel="chrome"
        )
        # Đảm bảo viewport đủ lớn khi khởi tạo page
        self.page = await self.browser.new_page(viewport={"width": 1600, "height": 1200})
        
    async def close_browser(self):
        """Đóng browser"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    async def navigate_to_url(self, url: str):
        """Điều hướng đến URL"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        await self.page.goto(url)
        
    async def wait_and_verify_element(self, selector: str, timeout: int = 5000) -> bool:
        """Chờ và kiểm tra element có hiển thị không"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return await self.page.locator(selector).is_visible()
        except Exception as e:
            print(f"Error waiting for element {selector}: {e}")
            return False
    
    async def login_success(self):
        """Đăng nhập vào hệ thống"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            # Fill login form
            await self.page.get_by_role(role="textbox", name="email").fill(USERNAME)
            await self.page.get_by_role(role="textbox", name="password").fill(PASSWORD)
            await self.page.get_by_role(role="button", name="sign in").click()
            
            # Wait for toast notification
            toast_selector = "div.Toastify__toast-container--bottom-left div.Toastify__toast"
            toast_visible = await self.wait_and_verify_element(toast_selector)
            print(f"Toast hiển thị: {toast_visible}")
            
        except Exception as e:
            print(f"Lỗi đăng nhập: {e}")
            raise

    async def access_opti_section(self):
        """Truy cập vào phần OPTI"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            side_menu_visible = await self.page.locator("aside").is_visible()
            print(f"Side menu hiển thị: {side_menu_visible}")
            await self.page.get_by_role(role="menuitem", name="Opportunity").click()
        except Exception as e:
            print(f"Lỗi truy cập OPTI: {e}")
            raise

    async def add_new_opti(self):
        """Thêm mới opportunity"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            await self.page.get_by_role(role="button", name="Add opportunity").click()
            drawer_selector = "div[class='ant-drawer-content-wrapper']"
            is_drawer_visible = await self.wait_and_verify_element(drawer_selector)
            print(f"Drawer add opportunity hiển thị: {is_drawer_visible}")
        except Exception as e:
            print(f"Lỗi thêm opportunity: {e}")
            raise
        
    async def select_dropdown_option(self, placeholder_text: str, option_title: str, wait_time: int = 500):
        """Helper method để chọn option trong dropdown"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            # Click dropdown
            dropdown_selector = f"div.ant-select:has(span.ant-select-selection-placeholder:text-is('{placeholder_text}'))"
            await self.page.locator(dropdown_selector).click()
            
            # Wait for options to appear - sử dụng timeout như file gốc
            await self.page.wait_for_timeout(wait_time)
            
            # Select option
            option_selector = f'div.ant-select-item-option[title="{option_title}"]'
            await self.page.locator(option_selector).click()
            
        except Exception as e:
            print(f"Lỗi chọn dropdown {placeholder_text}: {e}")
            raise

    async def select_dropdown_with_search(self, placeholder_text: str, search_text: str, wait_time: int = 500):
        """Helper method để chọn dropdown với tìm kiếm"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            # Click dropdown
            dropdown_selector = f"div.ant-select:has(span.ant-select-selection-placeholder:text-is('{placeholder_text}'))"
            await self.page.locator(dropdown_selector).click()
            
            # Type search text
            await self.page.wait_for_timeout(wait_time)
            await self.page.keyboard.type(search_text)
            await self.page.wait_for_timeout(wait_time)
            
            # Select option
            option_selector = f"div.ant-select-item-option:has-text('{search_text}')"
            await self.page.locator(option_selector).click()
            
        except Exception as e:
            print(f"Lỗi chọn dropdown với search {placeholder_text}: {e}")
            raise

    async def fill_opti_information(self):
        """Điền thông tin opportunity"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:            
            # Basic information
            await self.page.get_by_role(role="textbox", name="External ID").fill("Opla-001")
            await self.page.get_by_role(role="textbox", name='name').fill("Opportunity 1")
            await self.page.get_by_placeholder("Company").click()
            await self.page.wait_for_selector("div[class='ant-drawer-content-wrapper']")
            await self.page.locator("ul.ant-list-items > div.flex.cursor-pointer").first.click()
            await self.page.locator("div.ant-select:has(span.ant-select-selection-placeholder:text('Contact name'))").click()
            await self.page.wait_for_selector("div[class='ant-drawer-content-wrapper']")
            await self.page.locator("ul.ant-list-items input[type='checkbox']").first.click()
            await self.page.get_by_role(role="button", name="Save").click()
            await self.page.locator("div.ant-picker:has(input[name='date_opened'])").click()
            await self.page.locator("div.ant-picker-dropdown td.ant-picker-cell.ant-picker-cell-in-view:has-text('1')").nth(0).click()
            await self.page.locator("div.ant-picker:has(input[name='date_closed'])").click()
            await self.page.locator("div.ant-picker-dropdown td.ant-picker-cell.ant-picker-cell-in-view:has-text('15')").nth(0).click()

        except Exception as e:
            print(f"Lỗi điền thông tin opportunity: {e}")
            raise

    async def run_full_workflow(self):
        """Chạy toàn bộ workflow"""
        try:
            await self.navigate_to_url(MOGA_STG_URL)
            await self.login_success()
            await self.access_opti_section()
            await self.add_new_opti()
            await self.fill_opti_information()
            sleep(2)
            print("Workflow hoàn thành thành công!")
            
        except Exception as e:
            print(f"Lỗi trong workflow: {e}")
            raise


async def main():
    """Hàm main để chạy automation"""
    async with MOGAWebAutomation(headless=False) as automation:
        await automation.run_full_workflow()


if __name__ == "__main__":
    asyncio.run(main())