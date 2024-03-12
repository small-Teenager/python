import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
使用用户名密码登陆淘宝
'''


def login_taobao_selenium(username, password):
    '''
    :param username: 用户名
    :param password: 密码
    :return:
    '''
    # 选用开发者模式，创建一个浏览器对象，可避免被检测到是selenium模拟浏览器
    option = webdriver.ChromeOptions()
    # 解决登录出现滑动验证的参数
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=option)

    # 启动Chrome浏览器
    # driver = webdriver.Chrome()
    # 打开淘宝登录页面
    driver.get('https://login.taobao.com/member/login.jhtml')
    time.sleep(1)
    # 输入用户名和密码
    user_input = driver.find_element("id", 'fm-login-id')
    user_input.send_keys(username)
    time.sleep(1)
    pass_input = driver.find_element("id", 'fm-login-password')
    pass_input.send_keys(password)

    # 点击登录按钮
    login_button = driver.find_element('xpath', '//*[@id="login-form"]/div[4]/button')
    login_button.click()
    # 等待页面加载完成
    WebDriverWait(driver, 10).until(EC.title_contains('淘宝网'))

    print(driver.title)

    input("wait any time")

    # 关闭浏览器
    driver.quit()


if __name__ == '__main__':
    # 使用用户名和密码登录
    login_taobao_selenium('username', 'password')
