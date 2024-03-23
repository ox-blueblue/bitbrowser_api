from playwright.sync_api import Playwright, sync_playwright, expect, Page, ElementHandle, BrowserContext
import requests
import json
import random
import wallet_tool
from logger import log
# 官方文档地址
# httpsdoc2.bitbrowser.cnjiekouben-di-fu-wu-zhi-nan.html

# 新建一个窗口
class BitBrowser
    def __init__(self, url, headers, id, proxy_type='', proxy_host='', proxy_port='', proxy_user='', proxy_pwd='')
        self.url = url
        self.headers = headers
        self.id = id        
        self.ws = None
        # 代理
        self.proxy_type = proxy_type
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pwd = proxy_pwd
        self.proxy_ip = '' #需要chack agent 后获取
        # 新窗口参数
        self.finger_print =   
        self.update_proxy()    

    def open(self)
        json_data = {id f'{self.id}'}
        res = requests.post(f{self.url}browseropen,
                            data=json.dumps(json_data), headers=self.headers).json()
        if res[success]            
            ws = res['data']['ws']
            log.info(fopen browser ws address == {ws})
            self.ws = ws
        else
            log.error(res[msg])
        return self.ws
    
    def close(self)
        json_data = {'id' f'{self.id}'}
        res = requests.post(f{self.url}browserclose,
                    data=json.dumps(json_data), headers=self.headers).json()
        if res[success]            
            log.info(fclose browser success{self.id})
            return True
        else
            log.error(res[msg])
        return False
        
    def update(self, valuedict)
        json_data = {'id' f'{id}'}
        json_data.update(value)
        res = requests.post(f{self.url}browserupdatepartial,
                            data=json.dumps(json_data), headers=self.headers).json()
        return res
    
    #  'remark' '我是一个备注', 'browserFingerPrint' {}}
    def update_remark(self, remark)
        json_data = {'id' f'{id}'}
        json_data.update({'remark'remark})
        res = requests.post(f{self.url}browserupdatepartial,
                            data=json.dumps(json_data), headers=self.headers).json()
        return res
            
    def update_finger_print(self, finger_print='')
        if finger_print == ''
            finger_print = self.radom_finger_pring()
        json_data = {ids [self.id,]}
        json_data.update({'browserFingerPrint'finger_print})
        res = requests.post(f{self.url}browserupdatepartial,
                            data=json.dumps(json_data), headers=self.headers).json()
        if res[success]            
            log.info(fupdate finger success{self.id})
            return True
        else
            log.error(res[msg])
        return False
    
    def radom_finger_pring(self)
        # browserfingerprintrandom
        json_data = {'browserId' f'{self.id}'}
        res = requests.post(f{self.url}browserfingerprintrandom,
                            data=json.dumps(json_data), headers=self.headers).json()
        self.finger_print = res[data]
        return self.finger_print
    
    def update_proxy(self)
        json_data = {ids [self.id,],         #string
            proxyMethod 2,        # 代理方式 2自定义 3 提取IP            
            'proxyType' self.proxy_type, # 代理类型  ['noproxy', 'http', 'https', 'socks5', 'ssh']
            'host' self.proxy_host,  # 代理主机
            'port' self.proxy_port,  # 代理端口
            'proxyUserName' self.proxy_user,  # 代理账号
            'proxyPassword' self.proxy_pwd
            }
        res = requests.post(f{self.url}browserproxyupdate,
                        data=json.dumps(json_data), headers=self.headers).json()
        if res[success]            
            log.info(fupdate proxy success{self.proxy_user})
            return True
        else
            log.error(res[msg])
        return False
    
    # 删除全部缓存，包括云端数据
    def cache_clear(self)
        json_data = {ids [self.id,]}
        res = requests.post(f{self.url}cacheclear,
                        data=json.dumps(json_data), headers=self.headers).json()
        if res[success]            
            log.info(fcache clear success{self.id})
            return True
        else
            log.error(res[msg])
        return False
        
    def cache_clear_except_ex(self)
        json_data = {ids [self.id,]}
        res = requests.post(f{self.url}cacheclearexceptExtensions,
                        data=json.dumps(json_data), headers=self.headers).json()
        if res[success]            
            log.info(fcache clear exceptExtensions success{self.id})
            return True
        else
            log.error(res[msg])
        return False
    
    def check_agent(self)        
        json_data = {host self.proxy_host,         #string
                 port self.proxy_port,        #int 
                 proxyType self.proxy_type,   #string
                 proxyUserName self.proxy_user, #string
                 proxyPassword self.proxy_pwd, #string
                 checkExists 1, 
                 }
        res = requests.post(f{self.url}checkagent,
                        data=json.dumps(json_data), headers=self.headers).json()   
        if res[data][success]
            self.proxy_ip = res[data][data][ip] 
            log.info(fcheck agent success{self.proxy_ip})
            return True
        else
            log.error(res[data][message])
        return False    
       

if __name__ == '__main__':       
    browser_id = 3547827ebf3a4253aa01f6a0e13ba95e    
    b = BitBrowser(
        url=http127.0.0.154345,
        headers={'Content-Type' 'applicationjson'},
        id=browser_id
    )        
    b.update_finger_print()
    b.cache_clear()        
    b.open()
            
