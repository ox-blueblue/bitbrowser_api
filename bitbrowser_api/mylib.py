from playwright.sync_api import Playwright, sync_playwright, Page, ElementHandle
import sys
import random

# 等待元素出现（attached）或者可见(visible)，超时就刷新再等待，超过刷新次数则返回 None，否则返回locator 对象
def wait_for_selector_reflash(page:Page, selector, state='visible', timeout=5000, retry=6)->ElementHandle:
    for i in range(retry):
        try: 
            element = page.wait_for_selector(selector, state=state, timeout=timeout)
        except Exception as r:
            s = sys.exc_info()
            element = None
        if element is None:
            page.reload()
            continue
        else:
            break
    return element

# 等待元素，超时不抛异常，成功返回locator，否则返回None
def wait_for_selector_attached(page:Page, selector, timeout=30000):    
    try: 
        loc = page.wait_for_selector(selector, state='attached', timeout=timeout)
    except Exception as r:
        s = sys.exc_info()
        return None
    return loc

# 等待元素可用，成功返回True，否则返回False
def wait_for_selector_enabled(page:Page, selector, timeout=30000):    
    if timeout < 100:
        return False
    timeout_p = 100
    for i in range(int(timeout/timeout_p)):
        if page.is_enabled(selector):
            return True
        page.wait_for_timeout(timeout_p)
    return False

# 判断selector是否存在
def selector_is_exist(page:Page, selector):
    loc = page.locator(selector)
    if loc.count():
        return True
    else:
        return False
    
# 判断selector列表里有一个存在，否则返回None
def selectors_is_exist(page:Page, selectors:list, trycount=3):
    for i in range(trycount):        
        for s in selectors:        
            if selector_is_exist(page, s):
                return s    
        page.wait_for_timeout(1000)    
    return None

# 操作延时1s
def oper_sleep(page:Page):
    base = 2000
    page.wait_for_timeout(random.randint(base-100, base+100))



