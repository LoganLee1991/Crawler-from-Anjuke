# -*- coding: utf-8 -*-
'''
爬取安居客网站的租房信息
'''

import urllib.request
import gzip
from bs4 import BeautifulSoup

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
    "Upgrade-Insecure-Requests": 1,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.33 Safari/537.36"
}

num = 0
delimiter = '|'
url = 'https://cd.zu.anjuke.com/fangyuan/jinjiang/'

urllist = [url + 'p' + str(i) for i in range(2, 12)]
urllist.insert(0, url)

file = open('./rentInfoResult2.txt', 'w+')

for oneurl in urllist:
    print(oneurl)
    req = urllib.request.Request(oneurl, headers=header)
    response = urllib.request.urlopen(req)

    html = gzip.decompress(response.read()).decode('utf-8', 'ignore')
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    zuinfo = soup.find_all('div', class_='zu-itemmod')

    for info in zuinfo:
        num += 1
        link = info.find('a')['href']
        img = info.find('img')['src']
        title = info.find('h3').string
        detail = info.find('p', class_='details-item tag').contents[::2]
        details = delimiter.join(detail)
        address = info.find('address').get_text().replace(' ', '').replace('\n', '')  # info.address.a
        price = info.find('div', class_='zu-side').p.strong.string + info.find('div', class_='zu-side').p.contents[1]
        name = info.find('p', class_='details-item bot-tag').span.string
        other = info.find('p', class_='details-item bot-tag').em.string
        allinfo = [num, link, img, title, details, address, price, name, other]
        allinfostr = [str(item) for item in allinfo]  # 将所有元素转换为字符串格式，因为有空值，为NoneType类型，造成连接出错
        # print(delimiter.join(allinfostr))
        file.write(delimiter.join(allinfostr) + '\n')

    file.flush()

file.close()
