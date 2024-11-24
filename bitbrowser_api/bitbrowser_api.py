import requests
import json
import sys
from loguru import logger as log
import time
import threading
lock = threading.Lock()  # 创建锁，暂时只对open、close、update_finger_print、check_agent 加锁，其他外部调用函数不支持多线程
# 官方文档地址
# https://doc2.bitbrowser.cn/jiekou/ben-di-fu-wu-zhi-nan.html


# 新建一个窗口
class BitBrowser:
    def __init__(self, url, headers, id, proxy_type='', proxy_host='', proxy_port='', proxy_user='', proxy_pwd=''):
        self.url = url
        self.headers = headers
        self.id = id        
        self.ws = None
        self.context = None
        self.clear_cache_after_closing = False
        # 代理
        self.proxy_type = proxy_type
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pwd = proxy_pwd
        self.proxy_ip = '' #需要chack agent 后获取
        # 新窗口参数
        self.detail = None        
        # 状态
        self.is_open = False

    def open(self, headless=False):
        with lock:
            if self.proxy_type != '':
                if not self.update_proxy():
                    return False

            json_data = {"id": f'{self.id}'}
            res = requests.post(f"{self.url}/browser/open",
                                data=json.dumps(json_data), headers=self.headers).json()
            if res["success"]:            
                ws = res['data']['ws']
                log.info(f"open browser ws address ==>>> {ws}")
                self.ws = ws
                ret = self.get_detail()
                if ret == False:
                    return False
                self.is_open = True
                time.sleep(2)
                return True
            else:
                log.error(res["msg"])       
            return False  
    
    def close(self, clear_cache=False):
        with lock:
            json_data = {'id': f'{self.id}'}
            res = requests.post(f"{self.url}/browser/close",
                        data=json.dumps(json_data), headers=self.headers).json()
            if res["success"]:            
                log.info(f"close browser success:{self.id}")
            else:
                log.error(res["msg"])
            self.is_open = False
            time.sleep(3)         
            if self.clear_cache_after_closing or clear_cache:
                self.cache_clear() 
            log.info(f"close browser:{self.id}")
    
    def get_browser_context(self):
        port = self.ws.split(':')[2].split('/')[0]
        self.context = f"http://127.0.0.1:{port}"
        return self.context   
    def update(self, value:dict):
        json_data = {'id': f'{id}'}
        json_data.update(value)
        res = requests.post(f"{self.url}/browser/update/partial",
                            data=json.dumps(json_data), headers=self.headers).json()
        return res
    
    #  'remark': '我是一个备注', 'browserFingerPrint': {}}
    def update_remark(self, remark):
        json_data = {'id': f'{id}'}
        json_data.update({'remark':remark})
        res = requests.post(f"{self.url}/browser/update/partial",
                            data=json.dumps(json_data), headers=self.headers).json()
        return res
            
    def update_finger_print(self, finger_print=''):
        with lock:
            if finger_print == '':
                finger_print = self.radom_finger_pring()
            json_data = {"ids": [self.id,]}
            json_data.update({'browserFingerPrint':finger_print})
            res = requests.post(f"{self.url}/browser/update/partial",
                                data=json.dumps(json_data), headers=self.headers).json()
            if res["success"]:            
                log.info(f"update finger success:{self.id}")
                return True
            else:
                log.error(res["msg"])
            return False    
    
    def radom_finger_pring(self):
        # /browser/fingerprint/random
        json_data = {'browserId': f'{self.id}'}
        res = requests.post(f"{self.url}/browser/fingerprint/random",
                            data=json.dumps(json_data), headers=self.headers).json()
        if res["success"]:            
            log.info(f"random finger success:{self.id}")
            return res["data"]        
        return ""
    
    def update_proxy(self):
        json_data = {"ids": [self.id,],         #string
            "proxyMethod": 2,        # 代理方式 2自定义 3 提取IP            
            'proxyType': self.proxy_type, # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
            'host': self.proxy_host,  # 代理主机
            'port': self.proxy_port,  # 代理端口
            'proxyUserName': self.proxy_user,  # 代理账号
            'proxyPassword': self.proxy_pwd
            }
        res = requests.post(f"{self.url}/browser/proxy/update",
                        data=json.dumps(json_data), headers=self.headers).json()
        if res["success"]:            
            log.info(f"update proxy success:{self.proxy_type}")
            return True
        else:
            log.error(res["msg"])
        return False
    
    def set_clear_cache_after_closing(self):
        self.clear_cache_after_closing = True

    # 删除全部缓存，包括云端数据
    def cache_clear(self):
        try:
            json_data = {"ids": [self.id,]}
            res = requests.post(f"{self.url}/cache/clear",
                            data=json.dumps(json_data), headers=self.headers).json()
            if res["success"]:            
                log.info(f"cache clear success:{self.id}")
                return True
            else:
                log.error(res["msg"])
            return False
        except Exception as r:            
            s = sys.exc_info()
            log.error("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)) 
            return False 
        
    def cache_clear_except_ex(self):
        json_data = {"ids": [self.id,]}
        res = requests.post(f"{self.url}/cache/clear/exceptExtensions",
                        data=json.dumps(json_data), headers=self.headers).json()
        if res["success"]:            
            log.info(f"cache clear exceptExtensions success:{self.id}")
            return True
        else:
            log.error(res["msg"])
        return False
    
    def check_agent(self):    
        with lock:   
            json_data = {"host": self.proxy_host,         #string
                    "port": self.proxy_port,        #int 
                    "proxyType": self.proxy_type,   #string
                    "proxyUserName": self.proxy_user, #string
                    "proxyPassword": self.proxy_pwd, #string
                    "checkExists": 1, 
                    }
            res = requests.post(f"{self.url}/checkagent",
                            data=json.dumps(json_data), headers=self.headers).json()   
            if res["data"]["success"]:
                self.proxy_ip = res["data"]["data"]["ip"] 
                log.info(f"[{self.id}]check agent success:{self.proxy_ip}")
                return True
            else:
                log.error(res["data"]["message"])
            return False   

    def get_detail(self):
        json_data = {"id": self.id}
        res = requests.post(f"{self.url}/browser/detail",
                        data=json.dumps(json_data), headers=self.headers).json()   
        if res["success"]:
            self.detail = res["data"] 
            #log.debug(self.detail)
            finger_print = self.detail["browserFingerPrint"]["userAgent"]
            log.info(f"get detail success:FingerPrint:{finger_print}")
            return True
        else:
            log.error(res["error"])
        return False


url = "http://127.0.0.1:54345"
headers = {'Content-Type': 'application/json'}

def createBrowser():  # 创建或者更新窗口，指纹参数 browserFingerPrint 如没有特定需求，只需要指定下内核即可，如果需要更详细的参数，请参考文档
    json_data = {
        'name': 'google',  # 窗口名称
        'remark': '',  # 备注
        'proxyMethod': 2,  # 代理方式 2自定义 3 提取IP
        # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
        'proxyType': 'noproxy',
        'host': '',  # 代理主机
        'port': '',  # 代理端口
        'proxyUserName': '',  # 代理账号
        "browserFingerPrint": {  # 指纹对象
            'coreVersion': '112'  # 内核版本 112 | 104，建议使用112，注意，win7/win8/winserver 2012 已经不支持112内核了，无法打开
        }
    }

    res = requests.post(f"{url}/browser/update",
                        data=json.dumps(json_data), headers=headers).json()
    browserId = res['data']['id']
    print(browserId)
    return browserId


def updateBrowser():  # 更新窗口，支持批量更新和按需更新，ids 传入数组，单独更新只传一个id即可，只传入需要修改的字段即可，比如修改备注，具体字段请参考文档，browserFingerPrint指纹对象不修改，则无需传入
    json_data = {'ids': ['93672cf112a044f08b653cab691216f0'],
                 'remark': '我是一个备注', 'browserFingerPrint': {}}
    res = requests.post(f"{url}/browser/update/partial",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)


def openBrowser(id):  # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
    json_data = {"id": f'{id}'}
    res = requests.post(f"{url}/browser/open",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)
    print(res['data']['http'])
    return res


def closeBrowser(id):  # 关闭窗口
    json_data = {'id': f'{id}'}
    requests.post(f"{url}/browser/close",
                  data=json.dumps(json_data), headers=headers).json()


def deleteBrowser(id):  # 删除窗口
    json_data = {'id': f'{id}'}
    print(requests.post(f"{url}/browser/delete",
          data=json.dumps(json_data), headers=headers).json())

def pidsOfBrowser():  # 查询窗口
    print(requests.post(f"{url}/browser/pids/all", headers=headers).json())

def listBrowser():
    json_data = {"page": 1, "pageSize": 500, }
    res = requests.post(f"{url}/browser/list",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)
    print(len(res['data']['list']))
    id_list = []
    for browser in res['data']['list']:
        id_list.append(browser['id'])
    id_list.reverse()
    for id in id_list:
        print(id)

if __name__ == '__main__':
    b = BitBrowser(
                url="http://127.0.0.1:54345",
                headers={'Content-Type': 'application/json'},
                id="a8924c465c08411790656e66accc48f5")    
    b.open()
    context = b.get_browser_context()
    print(context)
        
        


    