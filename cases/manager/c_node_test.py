import pytest
from lib.mgrui.locator.nodePage import NodePage


@pytest.fixture(scope='class')
def node_page(login):
    return NodePage(login)


class TestNode:

    @pytest.mark.skip('节点信息已配置')
    @pytest.mark.parametrize('name, desc, rpc, license_file, ip,pwd, host, p2pport, genesis_file, script, user', [(
            'node10',
            'node_desc',
            '1347',
            r'C:\Users\juzix\Documents\platone-license',
            '192.168.120.134',
            '123456',
            '192.168.120.134',
            '11347',
            r'C:\Users\juzix\Documents\genesis.json', '/linux/scripts',
            'juzix')])
    def test_01_add_node_success(self, node_page, name, desc, rpc, license_file, ip,
                              pwd, host, p2pport, genesis_file, script,
                              user):
        """
        添加节点
        tips: 请注意部署ip，端口和部署的路径，且节点名字不能重复！
        TODO: 数据清理
        """
        try:
            node_page.add_node(name, desc, rpc, license_file, ip,
                               pwd, host, p2pport, genesis_file, script,
                               user)
            assert node_page.check_text('操作成功!') is True
        finally:
            pass
            """
            from common.connectServer import connect_linux
            print('开始清理数据......')
            s = connect_linux('192.168.120.13','juzix','123456')  # TODO： 敏感信息不暴露
            stdin, stdout, stderr = s.exec_command(f'cd ~/linux && rm -rf data/ conf/genesis.json platone-license')
            stdin2, stdout2, stderr2 = s.exec_command(f'killall -9 platone')
            # result = str(stdout.read(), encoding='utf-8')
            # print(result)
            """

    def test_02_edit_publicnd_rpc_port(self, node_page):
        """
        修改共识节点的rpc端口
        """
        node_page.edit_rpc_port('1361')
        assert node_page.check_text('操作成功!') is True

    def test_03_edit_normalnd_ip(self, node_page):
        """
        修改观察者节点的ip地址
        """
        node_page.edit_normalnd_ip('192.168.120.135')
        assert node_page.check_text('操作成功!') is True

    def test_04_normalnd_ports(self, node_page):
        """
        修改观察者节点的端口，rpc/p2pport
        """
        node_page.edit_normalnd_port('1350', '11350')
        assert node_page.check_text('操作成功!') is True

    @pytest.mark.skip('跳过,2/3受限')
    def test_05_normalnd_publicnd(self, node_page):
        """
        修改观察者节点为共识节点
        TODO： 断言
        """
        node_page.to_publicnd()
        # assert node_page.check_text('操作成功!') is True

    @pytest.mark.skip('跳过,2/3数据受限')
    def test_06_publicnd_normal(self, node_page):
        """
        1.仅有2个共识节点
        2.共识节点修改为观察者节点
        TODO： 断言
        """
        node_page.to_normalnd()
        # assert node_page.check_text('操作成功!') is True

    def test_07_stop_node(self, node_page):
        """
        禁用节点
        """

        node_page.stop_node()
        assert node_page.check_text('节点禁用成功!') is True

    def test_08_start_node(self, node_page):
        """
        禁用后，重新启动节点
        """
        node_page.start_node()
        assert node_page.check_text('节点启用成功!') is True

    def test_09_delete_node(self, node_page):
        """
        删除节点
        """

        node_page.delete_node()
        assert node_page.check_text('节点信息删除成功!') is True
