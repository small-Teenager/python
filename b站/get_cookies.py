from selenium import webdriver
import json

'''
扫码登陆bilibili 把生成的cookies保存到本地的json文件中
'''


def save_cookies(json_path='bilibili_cookies.json', login_url='https://www.bilibili.com/'):
    '''
    :param json_path: 本地保存json路径
    :param login_url: 登陆url
    :return:
    '''
    driver = webdriver.Chrome()
    driver.get(login_url)
    driver.maximize_window()  # 最大化
    input("等待扫码登录，回车")
    cookies = driver.get_cookies()  # 登录成功后，获取所有cookies,返回列表
    print(f"cookies info: {cookies}")
    json_cookies = json.dumps(cookies)  # python对象转换成json格式的字符串，返回字符串
    with open(json_path, 'w') as f:
        f.write(json_cookies)
    driver.quit()


save_cookies()
