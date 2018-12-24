# encoding=utf-8
import requests
import time
from selenium import webdriver
import selenium.webdriver.support.ui as ui

class qqMessage(object):
    def __init__(self):
        self.qq = ''  # 要爬的QQ
        self.account = ''  # 用来登录的QQ账号
        self.password = ''  # 用来登录的QQ密码
        self.gtk = None
        self.newQQ = []  # 爬虫爬下来的QQ，准备加入待爬队列
        self.timeout = None  # 超时时间

class QzoneMessage(object):
    def getGTK(self, cookie):
        """ 根据cookie得到GTK """
        hashes = 5381
        for letter in cookie['p_skey']:
            hashes += (hashes << 5) + ord(letter)
        return hashes & 0x7fffffff

    def getCookie(self, account, password):
        """ 根据QQ号和密码获取cookie """
        failure = 0
        while failure < 2:
            try:
                browser = webdriver.PhantomJS()
                wait = ui.WebDriverWait(browser, 10)
                browser.get('http://qzone.qq.com/?s_url=http://user.qzone.qq.com/1141802674/')
                browser.switch_to_frame('login_frame')
                wait.until(lambda browser: browser.find_element_by_id('switcher_plogin'))
                plogin = browser.find_element_by_id('switcher_plogin')
                plogin.click()
                wait.until(lambda browser: browser.find_element_by_id('u'))
                u = browser.find_element_by_id('u')
                u.send_keys('%s' % (account))
                p = browser.find_element_by_id('p')
                p.send_keys('%s' % (password))
                wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="login_button"]'))
                login = browser.find_element_by_xpath('//*[@id="login_button"]')
                time.sleep(2)
                login.click()
                time.sleep(1)
                try:
                    browser.switch_to_frame('vcode')
                    print u'Failed!----------------reason:该QQ首次登录Web空间，需要输入验证码！'
                    break
                except Exception:
                    pass
                try:
                    err = browser.find_element_by_id('err_m')
                    time.sleep(2)
                    d = err.text
                    print account, d
                    if u'您输入的帐号或密码不正确' in d:
                        print u'Failed!----------------reason:账号或者密码错误！'
                        break
                    if u'网络繁忙' in d:
                        time.sleep(2)
                except Exception, e:
                    # wait.until(lambda browser: browser.find_element_by_xpath(
                    #     '//*[@id="pageContent"]/div[1]/div[3]/div/div[2]/div[1]/div/b/b/textarea'))
                    # msg_b = browser.find_element_by_xpath(
                    #     '//*[@id="pageContent"]/div[1]/div[3]/div/div[2]/div[1]/div/b/b/textarea')
                    # msg_b.send_keys(u'Glory Be to Jehovah')
                    # wait.until(lambda browser: browser.find_element_by_xpath(
                    #     '//*[@id="pageContent"]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]/a'))
                    # btn = browser.find_element_by_xpath(
                    #     '//*[@id="pageContent"]/div[1]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]/a')
                    # btn.click()
                    cookie = {}
                    cookieStr = browser.get_cookies()
                    print cookieStr
                    for ck in cookieStr:
                        cookie[ck['name']] = ck['value']
                    browser.quit()
                    print u'Get the cookie of QQ:%s successfully!(共%d个键值对)' % (account, len(cookie))
                    return [cookie, cookieStr]
            except Exception:
                failure = failure + 1
            except KeyboardInterrupt, e:
                raise e
