import time
from basePage import BasePage
from selenium.webdriver.common.by import By


class UserPage(BasePage):
    """
    添加用户页面
    """
    add_user_btn = (By.CLASS_NAME, 'anticon-plus')
    user_name_input = (By.ID, 'normal_login_name')
    user_phone_input = (By.ID, 'normal_login_mobile')
    user_email_input = (By.ID, 'normal_login_email')
    user_address_input = (By.ID, 'normal_login_address')
    select_user_auth_btn = (By.CLASS_NAME, 'ant-select-selection-item')
    submit_btn = (By.CLASS_NAME, 'submit_btn')
    
    def add_user(self, name, phone, email, address, auth):
        """
        添加用户的数据
        """
        self.click_Element(self.add_user_btn, mark='添加用户')
        time.sleep(1)
        self.input_Text(self.user_name_input, name, mark='输入用户名')
        self.input_Text(self.user_phone_input, phone, mark='输入电话号码')
        self.input_Text(self.user_email_input, email, mark='输入电子邮箱')
        self.input_Text(self.user_address_input, address, mark='输入地址')
        self.choose_power(auth)
        self.click_Element(self.submit_btn)
        time.sleep(5)

    def choose_power(self, auth):
        """
        选择用户角色
        """
        self.click_Element(self.select_user_auth_btn)
        self.click_Text(auth, mark='选择权限')
