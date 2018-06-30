#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#https://www.cnblogs.com/mingjiatang/p/4890420.html

import os, re, datetime, unicodedata, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

# global var
q_type = []       # question type: 单选题，多选题
q_context = []
#q_answer = []
all_q_answer = []

#real_answer = []
all_real_answer = []

def login(usrname, passwd):
    driver = webdriver.Firefox(executable_path="./geckodriver")

    driver.get('https://xxx.com/sso/login')
    time.sleep(3)

    user = 'xxx'
    passwd = 'xxx'
    validate = input("Validate Code:")

    driver.find_element_by_id("username").send_keys(user)
    driver.find_element_by_id("password").send_keys(passwd)
    driver.find_element_by_id("validateCode").send_keys(validate)

    driver.find_element_by_class_name("tianze-loginbtn").click()
    time.sleep(3)
    driver.get("http://xxjs.dtdjzx.gov.cn/index.html")

    #driver.implicitly_wait(30)
    #bt = driver.find_element_by_id("mkjh")
    #print(bt)
    #print(bt.get_text())
    #bt.click()
    #time.sleep(10)
    driver.implicitly_wait(30)
    xiaoxi=driver.find_element_by_id("myxiaoxi")

    print(xiaoxi.text)

    #print(driver.page_source)

    driver.get("http://xxx.com/index.html")


    time.sleep(10)
    driver.find_element_by_id("lbuts").click()

    shenfen = Select(driver.find_element_by_id('shenfen'))
    shenfen.select_by_value('0')
    driver.find_element_by_id('bts').click()
    time.sleep(3)

    #driver.get("http://xxx.cn/monidati.html")
    #driver.get("http://xxx.cn/kaishijingsai.html")
    time.sleep(5)


    return driver

def getQestions(driver):
    bs = BeautifulSoup(driver.page_source, 'html.parser', from_encoding='utf-8')
    # print(bs)
    # finaAll VS find_all
    questions = bs.find("div", class_='W_ti W_mt22').find_all("li")

    for i in questions:
        q_answer = []
        a = i.find_all("span")
        if a[1].get_text() == "单选题":
            q_type.append(0)
        else:
            q_type.append(1)

        q_type.append(a[1].get_text())
        q_context.append(a[2].get_text().strip())

        b = i.find_all("div")
        q_answer.append(b[0].get_text())
        q_answer.append(b[1].get_text())
        q_answer.append(b[2].get_text())
        q_answer.append(b[3].get_text())

        all_q_answer.append(q_answer)


def getAnswers():
    file_path = "dt.txt"
    f = open(file_path, "r", encoding="utf-8")
    file_content = f.readlines()
    f.close()
    ti_num = 0
    real_answer = []
    for ti in q_context:
        real_answer = []
        for index, line in enumerate(file_content):
            if index % 6 == 0:
                searchObj = re.search(r'(.*)' + ti + '.*', line, re.M | re.I)
                if searchObj:
                    print("great!, completely match.")
                    cankao_daan = file_content[index + 5].split(':')[1].strip()
                    if 'A' in cankao_daan:
                        real_answer.append(file_content[index + 1][2:-1])
                    if 'B' in cankao_daan:
                        real_answer.append(file_content[index + 2][2:-1])
                    if 'C' in cankao_daan:
                        real_answer.append(file_content[index + 3][2:-1])
                    if 'D' in cankao_daan:
                        real_answer.append(file_content[index + 4][2:-1])
                    break
                elif fuzz.partial_ratio(ti, line) >= 80:
                    # need to double check the effecting of this score
                    print("good!, partially match.")
                    print(ti)
                    print(line)
                    new_ti = ti.replace("（）", '')
                    position1 = ti.find("（）")
                    position2 = line.find("（）")

                    if position1 < position2 or position1 == position2:
                        for i in range(len(line)):
                            if line[i] != new_ti[position1]:
                                continue
                            else:
                                #print(i)
                                break
                        real_answer = line[position1:position1 + i]
                    else:
                        for j in range(len(line)):

                            if line[-(len(new_ti) - position1) + 3 - j] != new_ti[position1 - 1]:
                                continue
                            else:
                                #print(j)
                                break
                        real_answer = line[-(len(ti) - position1) + 3 - j + 1:-(ti - position1) + 3]

                    if q_type[ti_num] == 1:
                        real_answer = re.split(re.compile('、|，|；'), real_answer)

                    break
                else:
                    if index == 119:
                        print("Unfortunately! do not find it %s."%(ti))

        all_real_answer.append(real_answer)
        ti_num = ti_num + 1
def getRealAnswers():
    pass


def submitTestPaper():
    pass


if __name__ == "__main__":
    usename = "xxx"
    passwd = "xxx"
    #validate = input("Validate Code:")
    drv = login(usename, passwd)
    getQestions(drv)
    print(q_type)
    print(q_context)
    print(all_q_answer)
    getAnswers()

    for i in all_real_answer:
        print(i)

