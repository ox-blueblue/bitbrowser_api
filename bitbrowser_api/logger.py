#format_rule = "[%(name)s]%(asctime)s-%(levelname)s[%(lineno)d]: %(message)s"   
format_rule = "%(asctime)s-%(levelname)s[%(lineno)d]: %(message)s"   

log_file_config = {
    "version":1,
    "disable_existing_loggers":False,
    "formatters":{
        "simple":{
            "format": format_rule         
        }
    },
    "handlers":{
        "console":{
            "class":"logging.StreamHandler",
            "level":"DEBUG",
            "formatter":"simple",
            "stream":"ext://sys.stdout"
        },
		"debug_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"DEBUG",
            "formatter":"simple",
            "filename":"logfile/debug.log",
            "maxBytes":10485760,
            "backupCount":20,
            "encoding":"utf8"
        },
        "info_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"INFO",
            "formatter":"simple",
            "filename":"logfile/info.log",
            "maxBytes":10485760,
            "backupCount":20,
            "encoding":"utf8"
        },
        "error_file_handler":{
            "class":"logging.handlers.RotatingFileHandler",
            "level":"ERROR",
            "formatter":"simple",
            "filename":"logfile/errors.log",
            "maxBytes":10485760,
            "backupCount":20,
            "encoding":"utf8"
        }
    },
    "loggers":{
        "my_module":{
            "level":"ERROR",
            "handlers":["info_file_handler"],
            "propagate":"no"
        }
    },
    "root":{
        "level":"DEBUG",
        "handlers":["console","debug_file_handler","info_file_handler","error_file_handler"]
    }
}

import logging
import json
import logging.config
import os

LOG_DIR = 'logfile'
curpath = os.getcwd()
log_dir_path = os.path.join(curpath, LOG_DIR)
log_file_name = os.path.join(log_dir_path, 'web3.log')
if not os.path.isdir(log_dir_path):  # 无文件夹时创建
    os.makedirs(log_dir_path)


# 输出format参数中可能用到的格式化串：
# %(name)s Logger的名字
# %(levelno)s 数字形式的日志级别
# %(levelname)s 文本形式的日志级别
# %(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
# %(filename)s 调用日志输出函数的模块的文件名
# %(module)s 调用日志输出函数的模块名
# %(funcName)s 调用日志输出函数的函数名
# %(lineno)d 调用日志输出函数的语句所在的代码行
# %(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
# %(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
# %(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
# %(thread)d 线程ID。可能没有
# %(threadName)s 线程名。可能没有
# %(process)d 进程ID。可能没有
# %(message)s用户输出的消息

# **注：1和3/4只设置一个就可以，如果同时设置了1和3，log日志中会出现一条记录存了两遍的问题。
def setup_logging(log, use_log_file_config=False, file_level=logging.INFO, console_level=logging.INFO):
    use_log_file_config = True
    default_path = "logging.json.nouse"
    env_key = "LOG_CFG"
    path = default_path
    value = os.getenv(env_key,None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path,"r") as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    elif use_log_file_config:
        logging.config.dictConfig(log_file_config)          
    else:   

        #1.设置log日志记录格式及记录级别
        #level记录级别包括DEBUG/INFO/WARNING/ERROR/CRITICAL，级别依次上升，log只会输出保存设置的级别及以上的日志。如果设置level=logging.DEBUG,则所有级别日志都会输出保存、如果level=logging.CRITICAL，则只输出保存CRITICAL级别日志
        #format输出格式levelname级别名、asctime 时间、filename所在文件名、message记录内容
        #datefmt 时间格式
        #filename 要保存的文件名
        #a写入模式，a则每次启动脚本时在原有文件中继续添加；w则每次启动脚本会重置文件然后记录
        # logging.basicConfig(level=logging.INFO,
        #                 format=format_rule,
        #                 datefmt='%Y-%m-%d %A %H:%M:%S',
        #                 filename=os.path.join(curpath, 'jd.log'),
        #                 filemode='a')
        
        #2.设置log日志的标准输出打印，如果不需要在终端输出结果可忽略        
        console = logging.StreamHandler()
        console.setLevel(console_level)
        #formatter = logging.Formatter("%(asctime)s--%(message)s" )
        formatter = logging.Formatter(format_rule)
        console.setFormatter(formatter)
        log.addHandler(console)
        
        #3.设置log日志文件按时间拆分记录，并保存几个历史文件，如果不需要拆分文件记录可忽略
        #class logging.handlers.WatchedFileHandler(filename, mode='a', encoding=None, delay=False)
        #例：设置每天保存一个log文件，以日期为后缀，保留7个旧文件。
        # log.setLevel(logging.DEBUG)  
        # formatter = logging.Formatter(format_rule)
        # filehandler = logging.handlers.TimedRotatingFileHandler(log_file_name, when='d', interval=1, backupCount=7)#每 1(interval) 天(when) 重写1个文件,保留7(backupCount) 个旧文件；when还可以是Y/m/H/M/S
        # filehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"#设置历史文件 后缀
        # filehandler.setFormatter(formatter)
        # log.addHandler(filehandler)
        
        #4.设置log日志文件按文件大小拆分记录，并保存几个历史文件，如果不需要拆分文件记录可忽略
        #class logging.handlers.RotatingFileHandler(filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0)
        
        log.setLevel(file_level)  
        formatter = logging.Formatter(format_rule)        
        filehandler = logging.handlers. RotatingFileHandler(log_file_name, mode='a', maxBytes=1024000, backupCount=10)#每 1024Bytes重写一个文件,保留2(backupCount) 个旧文件
        filehandler.setFormatter(formatter)
        log.addHandler(filehandler)


# 禁用安全请求警告
# import requests
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logging.getLogger("urllib3").setLevel(logging.WARNING)
#from selenium.webdriver.remote.remote_connection import LOGGER
#LOGGER.setLevel(logging.WARNING)

logging.getLogger("requests").setLevel(logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3") 
requests_log.setLevel(logging.ERROR)
# 默认是console的error，可通过setup_logging(log, file_level=logging.DEBUG, console_level=logging.INFO) 设置文件
log = logging.getLogger('web3')

import sys
class StdRedirection:    
    def __init__(self, log):
        self.buff=''
        self.__console__=sys.stdout
        self.__stderr__=sys.stderr
        self.logger = log
        
    def write(self, output_stream):
        self.logger.info(output_stream)
        
    def reset(self):
        sys.stdout=self.__console__
        sys.stderr=self.__stderr__

#setup_logging(log, file_level=logging.DEBUG, console_level=logging.DEBUG)  
setup_logging(log, use_log_file_config=True)        

if __name__ == "__main__":         
    setup_logging(log, file_level=logging.DEBUG, console_level=logging.INFO)    
    # 输出内容到日志 log.info()
    log.debug('这是debug级别log')
    # 输出内容到日志 log.info()
    log.info('这是info级别log')
    # 输出内容到日志 log.info()
    log.error('这是error级别log') 

         