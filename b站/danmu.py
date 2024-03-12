import requests
import pandas
from lxml import etree

import jieba.analyse
from wordcloud import WordCloud, random_color_func
import matplotlib.pyplot as plt


def download_dm(url):
    '''
    :param url: bilibili视频弹幕文件
    '''
    # 发送请求
    response = requests.get(url)
    xml = etree.fromstring(response.content)

    # 解析数据
    dm = xml.xpath("/i/d/text()")
    print(dm)  # list
    # print(type(dm))  # list

    # 把列表转换成 dataframe
    dm_df = pandas.DataFrame(dm)
    print(dm_df)
    print(type(dm_df))

    # 存到本地
    # 解决中文乱码
    dm_df.to_csv('dm.csv', encoding='utf_8_sig')
    return dm


def word_cloud_img(dm, img_file):
    '''
    :param dm:弹幕数据
    :param img_file:背景文件
    '''
    # jieba分词
    dm_str = " ".join(dm)
    words_list = jieba.lcut(dm_str)  # 切分的是字符串,返回的是列表
    words_str = " ".join(words_list)

    # 读取本地文件
    backgroud_image = plt.imread(img_file)

    # 创建词云
    wc = WordCloud(
        background_color='white',
        mask=backgroud_image,
        font_path='/Library/Fonts/Arial Unicode.ttf',  # 设置本地字体
        max_words=2000,
        max_font_size=100,
        min_font_size=10,
        color_func=random_color_func,
        random_state=50,
    )

    word_cloud = wc.generate(words_str)  # 产生词云
    word_cloud.to_file("dm.jpg")  # 保存图片


if __name__ == '__main__':
    # bilibili视频弹幕文件 cid 从网页源码中获取
    cid = '1458555064'
    url = f'https://comment.bilibili.com/{cid}.xml'
    dm = download_dm(url)
    word_cloud_img(dm, 'backgroud.jpeg')
