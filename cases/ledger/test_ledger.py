import time, json

import pytest
from hexbytes import HexBytes
from platone import Web3, HTTPProvider, platone, txpool, Account, miner, net, personal, ledger, ledger_node, admin
from lib.utils import *
from cases.ledger.conftest import *


class TestNode:


    def test_listAll(self, create_ledger_jion_observe_node):
        """
        @describe: 查询指定子帐本所有节点信息
        @parameters:
        - null
        @return:
        - 1. 子帐本所有节点信息，list
        """
        ledger_name, sub_ledger_node, _ = create_ledger_jion_observe_node
        subledger_node_list = sub_ledger_node.list()
        assert isinstance(subledger_node_list, list)
        assert json.loads(subledger_node_list[0])['code'] == 0


    def test_add(self):
        """
        @describe: 获取指定块中特定账户地址的余额
        @parameters:
        - 1. pubkey： node_id
        - 2. bls_pubkey： 节点的blsPubKey
        - 3. private_key： 私钥
        - 4. tx_cfg: 可不填
        @return:
        - 1.
        """
        #joinLedger接口已经测，不重复测
        pass


    def test_grantPerm(self, create_ledger):
        """
        @describe:
        @parameters:
        - 1. address： node_id
        - 2.  private_key： 私钥
        - 3. tx_cfg: 可不填
        @return:
        - 1.
        """
        ledger_name, sub_ledger_node, _ = create_ledger
        time.sleep(3)
        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)


    def test_revokePerm(self, create_ledger):
        """
        @describe:
        @parameters:
        - 1. address： node_id
        - 2.  private_key： 私钥
        - 3. tx_cfg: 可不填
        @return:
        - 1.
        """
        ledger_name, sub_ledger_node, _ = create_ledger
        time.sleep(5)
        result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        # 底层没有做限制没有授权的不能回收授权。前端说会做验证但是待验
        assert_code(result, 0)

        grantperm_result = sub_ledger_node.grantPerm(chain_admin_address, main_private_key)
        assert_code(grantperm_result, 0)
        time.sleep(2)
        result = sub_ledger_node.revokePerm(chain_admin_address, main_private_key)
        assert_code(result, 0)


    def test_remove(self, create_ledger_jion_observe_node, clients):
        """
        @describe: 节点退出子帐本
        @parameters:
        - 1. pubkey： node_id
        - 2.  private_key： 交易签名私钥
        - 3. tx_cfg: 可不填
        @return:
        - 1. dict
        """
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        observe_client_another = clients[4]
        result = sub_ledger_node.remove(observe_client_another.node_id, main_private_key)
        assert_code(result, 0)


    def test_updateNodeType_obs_to_con(self, create_ledger_jion_observe_node, clients):
        """
        @describe:
        @parameters: 更改子帐本节点类型, 观察者节点修改未共识节点
        - 1. pubkey： node_id
        - 2. node_type: 节点类型 0观察节点 1共识节点
        - 2.  private_key： 交易签名私钥
        - 3. tx_cfg: 可不填
        @return: dict
        - 1.
        """
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        observe_client_another = clients[4]
        node_id = json.loads(sub_ledger_node.list()[0])['data']['observer'][0]['nodeID']
        assert node_id == observe_client_another.node_id
        result = sub_ledger_node.updateNodeType(observe_client_another.node_id, 1, main_private_key)
        assert_code(result, 0)
        consensus_node_list = [json.loads(sub_ledger_node.list()[0])['data']['consensus'][i]['nodeID'] for i in range(len(json.loads(sub_ledger_node.list()[0])['data']['consensus']))]
        assert observe_client_another.node_id in consensus_node_list


    def test_updateNodeType_con_to_obs(self, create_ledger_four_node, clients):
        """
        @describe:
        @parameters: 更改子帐本节点类型, 修改共识节点为观察者节点,修改后共识节点数量大于节点列表数量的2/3
        - 1. pubkey： node_id
        - 2. node_type: 节点类型 0观察节点 1共识节点
        - 2.  private_key： 交易签名私钥
        - 3. tx_cfg: 可不填
        @return: dict
        - 1.
        """
        ledger_name, sub_ledger_node, client = create_ledger_four_node
        client_another = clients[4]
        time.sleep(10)
        obs_nodeid = json.loads(sub_ledger_node.list()[0])['data']['observer']
        assert obs_nodeid == []
        result = sub_ledger_node.updateNodeType(client_another.node_id, 2, main_private_key)
        assert_code(result, 0)
        time.sleep(10)
        sub_ledger_list = sub_ledger_node.list()
        update_obs_nodeid = json.loads(sub_ledger_list[0])['data']['observer'][0]['nodeID']
        assert update_obs_nodeid == client_another.node_id



class TestLedger:

    def test_getAllLedgers(self, client):
        """
        @describe: 查询所有账本信息
        @parameters:
        - null
        @return:
        - 1. 所有账本信息，list
        """
        ledgers = client.ledger.getAllLedgers()
        assert json.loads(ledgers[0])['code'] == 0



    def test_createLedger(self, client):
        """
        @describe: 创建一个新账本
        @parameters:
        - 1. ledger_json： 要查询的账户地址，bech32 address格式，lax开头的为测试网，lat开头的为主网
            - LedgerName: 新账本名称
            - NodeLedgerInfos ：
                - PublicKey： 节点id，可以用admin.nodeInfo查到节点id
                - nodeType： 节点类型
        - 2. private_key： 创建账本的用户地址私钥
        - 3. tx_cfg： dict,可不填，chainID,nonce,gas, value, gasPrice
        @return:
        - 1. 指定块中特定账户地址的余额,int
        """
        platone = client.platone
        nonce = platone.getTransactionCount(main_address, ledger=sys_ledger)
        id = client.node_id
        ledger_name = "test" + str(nonce)
        ledger_json = {
            "LedgerName": ledger_name,
            "NodeLedgerInfos": [
                {
                    "PublicKey": id,
                    "nodeType": 1
                }
            ]
        }
        result = client.ledger.createLedger(ledger_json, main_private_key)
        assert_code(result, 0)
        len_list = len(json.loads(client.ledger.getAllLedgers()[0])['data'])
        for i in range(len_list):
            if ledger_name == json.loads(client.ledger.getAllLedgers()[0])['data'][i]['ledgerName']:
                assert json.loads(client.ledger.getAllLedgers()[0])['data'][i]['consensusNodes'][0]['blsPubKey'] == client.node_pubkey
                break
        else:
            assert 1 == 2, 'Failed to create ledger'


    def test_joinLedger(self, create_ledger, clients):
        """
        @describe:
        @parameters:
        - 1. ledger_name：
        - 2. node_id：
        - 3. bls_pubKey：
        - 4. private_key：
        - 5. tx_cfg：
        @return:
        - 1.
        """
        ledger_name, sub_ledger_node, client = create_ledger
        client_another = clients[4]
        join_result = client.ledger.joinLedger(ledger_name, client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(join_result, 0)
        time.sleep(5)
        add_result = sub_ledger_node.add(client_another.node_id, client_another.node_pubkey, main_private_key)
        assert_code(add_result, 0)


    def test_joinLedgers(self, create_ledger):
        """
        @describe: 查询节点加入的账本名称列表
        @parameters:
        - 1. node_id： 节点ID
        - 2. tx_cfg：可不填
        @return:账本名字列表
        - 1.节点加入的账本名称列表
        """
        ledger_name, sub_ledger_node, client = create_ledger
        result = client.ledger.joinLedgers(client.node_id)
        assert isinstance(result, list) and json.loads(result[0])['code'] == 0



    def test_quitLedger(self, create_ledger_jion_observe_node, clients):
        """
        @describe: 退出子帐本
        @parameters:
        - 1. ledger_name：子帐本名称
        - 2. node_id：节点ID
        - 3. private_key：签名私钥
        - 4. tx_cfg：可不填
        @return:
        - 1. 返回结果
        """
        ledger_name, sub_ledger_node, client = create_ledger_jion_observe_node
        client_another = clients[4]
        result = client.ledger.quitLedger(ledger_name, client_another.node_id, main_private_key)
        assert_code(result, 0)
        result = sub_ledger_node.remove(client_another.node_id, main_private_key)
        assert_code(result, 0)




    def test_terminateLedger(self, create_ledger_jion_observe_node):
        """
        @describe: 关闭账本所有记账节点都将退出账本
        @parameters:
        - 1. ledger_name： 要关闭的账本名称
        - 2. private_key： 发起交易的账户私钥
        - 3. tx_cfg： 可不填
        @return: 交易信息，dict
        - 1.
        """
        ledger_name, _, client = create_ledger_jion_observe_node
        result = client.ledger.terminateLedger(ledger_name, main_private_key)
        assert_code(result, 0)





