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
        self.page = await self.browser.new_page()
        
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
    
    async def access_lead_section(self):
        """Truy cập vào phần Lead"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            side_menu_visible = await self.page.locator("aside").is_visible()
            print(f"Side menu hiển thị: {side_menu_visible}")
            await self.page.get_by_role(role="menuitem", name="Lead").click()
        except Exception as e:
            print(f"Lỗi truy cập Lead: {e}")
            raise
    
    async def change_list_view(self):
        """Thay đổi view sang dạng list"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            change_view_selector = "svg[data-icon='bars']"
            await self.page.locator(change_view_selector).wait_for()
            is_button_visible = await self.page.locator(change_view_selector).is_visible()
            print(f"Change view button hiển thị: {is_button_visible}")
            await self.page.locator(change_view_selector).click()
        except Exception as e:
            print(f"Lỗi thay đổi view: {e}")
            raise
    
    async def add_new_lead(self):
        """Mở form thêm lead mới"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            await self.page.get_by_role(role="button", name="Add lead").click()
            drawer_selector = "div[class='ant-drawer-content-wrapper']"
            is_drawer_visible = await self.wait_and_verify_element(drawer_selector)
            print(f"Drawer add lead hiển thị: {is_drawer_visible}")
        except Exception as e:
            print(f"Lỗi mở form thêm lead: {e}")
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
    
    async def fill_lead_information(self):
        """Điền thông tin lead"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            # Basic information
            await self.page.get_by_role(role="textbox", name="Account name").fill("Account")
            await self.page.locator("input[name='name']").fill("Contact")
            await self.page.locator("input[autocomplete='tel']").fill("+8412345678")
            await self.page.get_by_role(role="textbox", name="Email").fill("account@gmail.com")
            await self.page.get_by_role(role="textbox", name="Job title").fill("Title 1")
            
            # Dropdown selections
            await self.select_dropdown_option("Gender", "Male")
            await self.select_dropdown_option("Industry", "Event")
            await self.select_dropdown_option("Source", "Source 1")
            await self.select_dropdown_option("Status", "Hot lead")
            await self.select_dropdown_option("Lead Segmentation", "Cheap")
            await self.select_dropdown_option("Lead label", "acc01")
            await self.select_dropdown_option("Pick list", "Option 1")
            
            # Country and City with search
            await self.select_dropdown_with_search("Country", "Vietnam")
            await self.select_dropdown_with_search("City", "Bến Tre")
            
            # Other fields
            await self.page.locator("input[name='tax_identification_number']").fill("TAX1.1")
            await self.page.locator("input[name='address']").fill("Sala sarina, A0011")
            await self.page.get_by_role(role="textbox", name="Text").fill("ABC")
            await self.page.get_by_role(role="textbox", name="Link").fill("https://oplacrm.com")
            await self.page.locator("input[placeholder='Number']").fill("123")
            
            # Date picker
            await self.page.locator("div.ant-picker").click()
            await self.page.wait_for_selector("div.ant-picker-dropdown", state="visible")
            await self.page.locator("td.ant-picker-cell:has-text('15')").click()
            
            # Save
            await self.page.get_by_role(role="button", name="Save").click()
            sleep(2)
            
        except Exception as e:
            print(f"Lỗi điền thông tin lead: {e}")
            raise
    
    async def update_personal_settings(self):
        """Cập nhật cài đặt cá nhân"""
        if self.page is None:
            raise RuntimeError("Page not initialized")
        try:
            sleep(5)
            
            # Open dropdown menu
            await self.page.locator("div[class^='ant-dropdown-trigger']").click()
            await self.page.wait_for_selector("div[class$='ant-dropdown-placement-bottomRight']")
            await self.page.get_by_role(role='button', name='Personal Setting').click()
            
            sleep(1)
            
            # Fill personal information
            await self.page.locator("input[name='firstName']").fill('Yên')
            await self.page.locator("input[name='lastName']").fill('Lý')
            await self.page.locator("input[autocomplete='tel']").click()
            await self.page.locator("input[autocomplete='tel']").fill('707986543')
            
            # Save
            await self.page.get_by_role(role="button", name='Save').click()
            
        except Exception as e:
            print(f"Lỗi cập nhật cài đặt cá nhân: {e}")
            raise
    
    async def run_full_workflow(self):
        """Chạy toàn bộ workflow"""
        try:
            await self.navigate_to_url(MOGA_STG_URL)
            await self.login_success()
            await self.access_lead_section()
            await self.change_list_view()
            await self.add_new_lead()
            await self.fill_lead_information()
            await self.update_personal_settings()
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