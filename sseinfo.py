#_*_coding=utf-8_*_
'''
AUTHOR    Asher
dDATE     2018-9-11
TECH     requests  xpath re  mysql
'''

import re
import datetime
import requests
import pymysql
from lxml import etree

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'sns.sseinfo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/68.0.3440.106 Safari/537.36',
}

#连接数据库
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='123456',
                             db='test1',
                             charset='utf8mb4',
                             )
cursor = connection.cursor()

#创建表
# sql = '''
#     CREATE TABLE question (
#     id int(11) NOT NULL AUTO_INCREMENT,
#     custom varchar(255) ,
#     holder varchar(255) ,
#     question varchar(255) ,
#     time varchar(255) ,
#     answer LongText ,
#     PRIMARY KEY (id)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8
#     AUTO_INCREMENT=1 ;
#     '''
# cursor.execute(sql)

def get_html(url):
    html =requests.get(url,headers=headers).text
    handle_html(html)

def handle_html(html):
    try:
        i = 0
        content = etree.HTML(html)
        custom_name = content.xpath('//div[@class="m_feed_txt"]/a')
        question_initial = content.xpath('//div[@class="m_feed_cnt "]/div[@class="m_feed_txt"]')
        holder_initial = content.xpath('//div[@class="m_feed_detail m_qa_detail"]/div[@class="m_feed_face"]/p')
        answer_initial = content.xpath('//div[@class="m_feed_cnt"]/div[@class="m_feed_txt"]')
        time = content.xpath('//div[@class="m_feed_func"]/div[@class="m_feed_from"]/span')
        day = datetime.date.today()

        while i < len(custom_name):
            custom_initial = custom_name[i].xpath('string(.)').strip()
            custom = custom_initial.replace(':','').replace('@','')
            holder = holder_initial[i].xpath('string(.)').strip()
            date_initial = time[i].xpath('string(.)').strip()
            date_last = re.sub(r'.*前$|今天',str(day),date_initial)
            question = question_initial[i].xpath('string(.)').replace(custom,'').replace(':','').strip()
            answer = answer_initial[i].xpath('string(.)').strip()
            i += 1
            sql = "insert into question(custom,holder,question,time,answer) values('%s','%s','%s','%s','%s' ); " \
                  %(custom,holder,question,date_last,answer)
            connection.ping(reconnect=True)
            cursor.execute(sql)
            connection.commit()
        connection.close()
    except SyntaxError as e:
        print(e)

def main():
    a = 1
    b = int(input('请输入您想爬取的页数（一页十条数据)：'))
    while a <= b:
        url = 'http://sns.sseinfo.com/ajax/feeds.do?type=11&pageSize=10&lastid=-1&show=1&page=' + str(a)
        a += 1
        get_html(url)


if __name__ == '__main__':
    main()










