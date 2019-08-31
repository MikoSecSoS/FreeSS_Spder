# -*- coding: utf-8 -*-
import re

import pandas as pd

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = "https://free-ss.site/"

# 爬取数据
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
# option.add_argument("--proxy-server=socks://localhost:1080") # 使用代理请求网页
driver = Chrome(options=option)
driver.get(url)

# 获取源码
WebDriverWait(driver,20).until(lambda x: x.find_element_by_xpath("//*[@id=\"tbss\"]/tbody"))
page_source = driver.page_source
driver.quit() # 关闭浏览器

# 解析数据
ss = re.findall('<div id="tbss_wrapper".*?>(.*?)</div>', page_source, re.S)

# 处理数据
table = pd.read_html(ss[0])
datatmsp = pd.concat(table, axis=0, ignore_index=True)
datatmsp.drop(["Unnamed: 7"], axis=1, inplace=True)
datatmsp.rename(index=str, columns={"Unnamed: 5": "Time", "Unnamed: 6": "Country"}, inplace=True)

# 打印数据
print(datatmsp)

# 保存数据
datatmsp.to_excel("ss.xls", index=False)