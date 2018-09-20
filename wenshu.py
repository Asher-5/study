# -*- coding:utf-8 -*-
import requests
import re
import random
from lxml import etree
import json
from pyquery import PyQuery
import time

headers = {
        'Host': 'www.qichacha.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'PHPSESSID=c4672ppgqpff8eq7tlds1199e3; UM_distinctid=16578f1755c4fd-037b167af1c11d-9393265-1fa400-16578f1755dde; zg_did=%7B%22did%22%3A%20%2216578f1758620c-0ddc13f7516fd9-9393265-1fa400-16578f1758768e%22%7D; hasShow=1; _uab_collina=153533241524249656940823; acw_tc=AQAAAFQUiGHDNg4A625wewsceIBIyd3C; api=new; _umdata=A502B1276E6D5FEFF2CFEA617ED0DE25A9B62757D7DF25F625F259EB8A3AAB1EB61957E48FC31405CD43AD3E795C914C7D146245BAC22B9B7E73DD8FA6D60613; sstype=2; CNZZDATA1254842228=1295903385-1535328086-https%253A%252F%252Fwww.baidu.com%252F%7C1535338903; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1535332415,1535338236,1535338999; searchkey=%25E8%25B4%25BE%25E8%25B7%2583%25E4%25BA%25AD; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201535337667022%2C%22updated%22%3A%201535339019540%2C%22info%22%3A%201535332414863%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22ecb09f901f44f2d82e135f0db5cd5aa3%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1535339020',
        'Connection': 'keep-alive',
        'Upgrade - Insecure - Requests': '1',
        'Cache-Control': 'max-age=0',
    }

def download_page(url):
    return requests.get(url, headers=headers).text

def parse_html(html):
    content = etree.HTML(html)
    length = content.xpath('//div[@class="row"]//div[@id="wsview"]/div')
    div_len = len(length)
    # print(div_len)
    if div_len > 1:
        basic1 = content.xpath('//div[@class="row"]//div[@id="wsview"]')
        text_content =basic1 [0].xpath('string(.)')
        basic2 = content.xpath('//div[@class="row"]//div[@id="wsview"]/div[3]')
        text_title =basic2 [0].xpath('string(.)').strip()
        if text_title=='':
            basic2 = content.xpath('//div[@class="row"]//div[@id="wsview"]/div[6]')
            text_title = basic2[0].xpath('string(.)').strip()
        # print(text_title)
        with open('{}.txt'.format(text_title), 'w+',encoding='utf-8') as fp:
            fp.write(text_content)
        print('成功下载文件：'+text_title)
    # else:
    #     basic1 = content.xpath('//div[@class="row"]//div[@id="wsview"]')
    #     text_content = basic1[0].xpath('string(.)')
    #     basic2 = content.xpath('//div[@class="row"]//div[@id="wsview"]//div[@class="article_hd"]/h3')
    #     text_title = basic2[0].xpath('string(.)').strip()
    #     print(text_title)
    #     with open('{}.txt'.format(text_title), 'w+', encoding='utf-8') as fp:
    #         fp.write(text_content)
    #     print('成功下载文件：' + text_title)

def main():
    i = 0
    j = 0
    area = '北京市'
    Download_Url = 'https://www.qichacha.com/more_shixin?key='
    while i < 500:
        i += 1
        url = Download_Url + area +'&index=&province=&casetype=&sortField=&isSortAsc=&sstype=2&ajaxflag=true&p=' + str(i)
        if url!='':
            html = download_page(url)
            data = etree.HTML(html)
            url_li = data.xpath('//section[@id="searchlist"]/a/@href')
            for url_ in url_li:
                DOWNLOAD_URL = 'https://www.qichacha.com' + url_
                html = download_page(DOWNLOAD_URL)
                parse_html(html)
                j +=1
                print(j)
        else:
            break
if __name__ == '__main__':
    main()
