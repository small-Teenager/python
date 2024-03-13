from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
from pyquery import PyQuery
import json
'''
淘宝首页商品爬虫
'''
# 选用开发者模式，创建一个浏览器对象，可避免被检测到是selenium模拟浏览器
options = webdriver.ChromeOptions()
# 解决登录出现滑动验证的参数
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 把chrome设为selenium驱动的浏览器代理
driver = webdriver.Chrome(options=options)
# 如果一直到等待时间都没满足则会捕获TimeoutException异常
wait = WebDriverWait(driver, 15)


def search_goods(start_page, total_pages, search_word, json_path="taobao_cookies.json"):
    ''''
    start_page  开始爬取的页面数
    total_pages  爬取的总页面数
    '''
    # 登陆
    driver.get('https://www.taobao.com')
    driver.delete_all_cookies()  # 删除本次打开网站生成的cookies
    with open(json_path, 'r', encoding='utf-8') as f:  # 打开之前生成的cookies
        cookies = json.loads(f.read())  # json的字符串转换成python对象

    for cookie in cookies:  # 列表
        driver.add_cookie({'domain': '.taobao.com',  # 添加cookie
                           'name': cookie['name'],
                           'value': cookie['value'],
                           'path': '/',
                           'expires': None})
    driver.refresh()  # 刷新网站

    print('正在搜索: ')

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
    # 找到搜索输入框
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
    # 找到“搜索”按钮
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
    search_input.send_keys(search_word)
    submit.click()
    # 搜索商品后会再强制停止10秒，如有滑块请手动操作
    time.sleep(10)

    # 如果不是从第一页开始爬取，就滑动到底部输入页面然后跳转
    if start_page != 1:
        # 滑动到页面底端
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 滑动到底部后停留1-3s
        random_sleep(1, 3)

        # 找到输入页面的表单
        pageInput = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div[1]/div[2]/div[4]/div/div/span[3]/input')))
        pageInput.send_keys(start_page)
        # 找到页面跳转的确定按钮，并且点击
        admit = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[3]/div[1]/div[1]/div[2]/div[4]/div/div/button[3]')))
        admit.click()

    get_goods()

    for i in range(start_page + 1, start_page + total_pages):
        page_turning(i)


# 强制等待的方法，在timeS到timeE的时间之间随机等待
def random_sleep(time_start, time_end):
    # 生成一个start到end之间的随机等待时间
    random_sleep_time = random.uniform(time_start, time_end)
    time.sleep(random_sleep_time)


# 进行翻页处理
def page_turning(page_number):
    print(f'正在翻页: {page_number}')
    # 找到下一页的按钮
    submit = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="sortBarWrap"]/div[1]/div[2]/div[2]/div[8]/div/button[2]')))
    submit.click()
    # 判断页数是否相等
    wait.until(EC.text_to_be_present_in_element(
        (By.XPATH, '//*[@id="sortBarWrap"]/div[1]/div[2]/div[2]/div[8]/div/span/em'), str(page_number)))
    get_goods()


# 获取每一页的商品信息；
def save_product(product):
    print('存储商品信息成功: ', product)
    pass


# 查询商品信息
def get_goods():
    # 获取商品前固定等待2-4秒
    random_sleep(2, 4)

    html = driver.page_source
    # print(f"html 信息:{html}")
    doc = PyQuery(html)
    # 提取所有商品的共同父元素的类选择器
    items = doc(
        'div.PageContent--contentWrap--mep7AEm > div.LeftLay--leftWrap--xBQipVc > div.LeftLay--leftContent--AMmPNfB > div.Content--content--sgSCZ12 > div > div').items()

    for item in items:
        print(item.text())
        # 定位商品标题
        title = item.find('.Title--title--jCOPvpf span').text()
        # 定位价格
        price_int = item.find('.Price--priceInt--ZlsSi_M').text()
        price_float = item.find('.Price--priceFloat--h2RR0RK').text()
        if price_int and price_float:
            price = float(f"{price_int}{price_float}")
        else:
            price = 0.0
        # 定位交易量
        deal = item.find('.Price--realSales--FhTZc7U').text()
        # 定位所在地信息
        location = item.find('.Price--procity--_7Vt3mX').text()
        # 定位店名
        shop = item.find('.ShopInfo--TextAndPic--yH0AZfx a').text()
        # 定位包邮的位置
        postText = item.find('.SalesPoint--subIconWrapper--s6vanNY span').text()
        result = 1 if "包邮" in postText else 0
        # 构建商品信息字典
        product = {
            'title': title,
            'price': price,
            'deal': deal,
            'location': location,
            'shop': shop,
            'isPostFree': result
        }
        save_product(product)


# 启动爬虫
if __name__ == '__main__':
    pageStart = 3  # 开始爬取的页面数
    pageAll = 10  # 爬取的总页面数
    search_word = "苹果"  # 爬取商品关键词
    search_goods(pageStart, pageAll, search_word)
