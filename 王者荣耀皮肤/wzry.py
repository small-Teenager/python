import os
import requests
import datetime

'''
王者荣耀皮肤下载
不包含新出得皮肤 https://pvp.qq.com/web201605/js/herolist.json 不包含新出皮肤
'''
url = 'https://pvp.qq.com/web201605/js/herolist.json'
hero_list = requests.get(url)  # 获取英雄列表json文件

hero_list_json = hero_list.json()  # 转化为json格式
hero_cnames = list(map(lambda x: x['cname'], hero_list_json))  # 提取英雄的名字
print(f"提取英雄的名字:{hero_cnames}")
hero_enames = list(map(lambda x: x['ename'], hero_list_json))  #
print(f"提取英雄的编号:{hero_enames}")
skin_name = list(map(lambda x: x.get('skin_name'), hero_list_json))  # 提取的英雄的皮肤名称

print(f"英雄的皮肤名称:{skin_name}")


# 下载图片
def download_image(file_path="wzry"):
    # 创建wzry主文件夹
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    os.chdir(file_path)
    for (hero_num, hero_ename) in zip(range(len(hero_enames)),
                                      hero_enames):
        # 创建英雄子文件夹
        if not os.path.isdir(hero_cnames[hero_num]):
            os.mkdir(hero_cnames[hero_num])
        # 进入创建好的英雄子文件夹
        os.chdir(hero_cnames[hero_num])
        print(f"进入英雄子文件夹 {hero_cnames[hero_num]}")
        # print(type(skin_name[hero_num]))
        print(skin_name[hero_num])
        if type(skin_name[hero_num]) is str:
            skins = skin_name[hero_num].split('|')
            print(f"skins 长度：{len(skins)}")

            for skin_num in range(len(skins) + 1):  # 由于if im.status_code == 200:这步莫名导致skin_num+1，因此这里总数为len(skins)+1
                # 拼接url
                one_hero_link = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/' + str(
                    hero_ename) + '/' + str(
                    hero_ename) + '-bigskin-' + str(skin_num) + '.jpg'
                print(f"开始下载:{hero_ename},{skin_num}")
                # print(f"开始下载:{skins[skin_num]}")

                img = requests.get(one_hero_link)  # 请求url
                if img.status_code == 200:  # 这句莫名导致skin_num+1，所以下面编号会-1
                    skin_num -= 1
                    open(hero_cnames[hero_num] + '-' + skins[skin_num] + '.jpg', 'wb').write(img.content)  # 写入文件
            # 此时还在英雄子文件夹内，所以需要返回上一层路径，即主文件夹下
        os.chdir("..")


if __name__ == '__main__':
    curr_time = datetime.datetime.now()

    download_image()

    curr_time2 = datetime.datetime.now()
    print(curr_time2 - curr_time)
