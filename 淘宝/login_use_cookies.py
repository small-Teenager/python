from selenium import webdriver
import json

'''
使用cookies登陆淘宝 
'''


def login_use_cookies(json_path="taobao_cookies.json", url="https://taobao.com"):
    '''
    使用之前生成的cookies文件，完成登录，绕过登录验证
    :param json_path:
    :param url:
    :return:
    '''
    # 选用开发者模式，创建一个浏览器对象，可避免被检测到是selenium模拟浏览器
    option = webdriver.ChromeOptions()
    # 解决登录出现滑动验证的参数
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    driver.delete_all_cookies()  # 删除本次打开网站生成的cookies
    with open(json_path, 'r', encoding='utf-8') as f:  # 打开之前生成的cookies
        cookies = json.loads(f.read())  # json的字符串转换成python对象

    for cookie in cookies:  # 列表
        driver.add_cookie({'domain': '.taobao.com',  # 添加cookie
                           'name': cookie['name'],
                           'value': cookie['value'],
                           'path': '/',
                           'expires': None})
    driver.get(url)  # 重新打开网站

    input("...")
    driver.quit()


login_use_cookies()
