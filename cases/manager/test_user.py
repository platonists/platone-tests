import pytest
from lib.mgrui.locator.userPage import UserPage


@pytest.fixture(scope='class')
def user_page(login):
    return UserPage(login)


class TestUser:

    # @pytest.mark.skip('有bug？？之前存在的用户名、地址不能再次添加')
    @pytest.mark.parametrize('name,phone,email,address,power', [
        ('user113', '15820347773', '447174@qq.com', 'lax1vf83f6yyzxqt6uerpfwcarvj9vtun8g4fdmkhq', '节点管理员')])
    def test_add_user_success(self, user_page, name, phone, email, address, power):
        """
        添加用户
        TODO： 测试数据未准备好
        """
        user_page.add_user(name, phone, email, address, power)
        assert user_page.check_text('新增用户成功!') is True

    def test_delete_user_success(self, user_page):
        """
        删除用户
        """
        user_page.delete_user(index=0)  # 删除第X个用户
        assert user_page.check_text('用户信息删除成功!') is True

    @pytest.mark.parametrize('name,phone,email,address,power', [
        ('user112', '15820347773', '447174@qq.com', 'lax1uhgck9xcllhwf30ped48gpz9yyjy4ves0cga8j', '游客')])
    def test_add_user_fail(self, user_page, name, phone, email, address, power):
        """
        添加重复的用户地址
        """
        user_page.add_user(name, phone, email, address, power)
        assert user_page.check_text('用户地址已经注册') is True
