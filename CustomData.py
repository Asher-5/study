# -*- coding:utf-8 -*-
'''
AUTHOR    Asher
dDATE     2018-9-11
TECH     requests  xpath re  mysql
'''

import requests
import random
import json
import time
from lxml import etree
from pyquery import PyQuery

headers = {
        'Host': 'www.qichacha.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.baidu.com/link?url=FU28_dPfJHQm7jXxQqCWB0afMb4T4gXD6FUPNb3z213sOMCT_xYMz_-SPaa1_f0t&wd=&eqid=fcaae1ce00006123000000025b4d4a2d',
        'cookie': 'PHPSESSID=qee8uppd5n530ajmu4pnq5a1r6; UM_distinctid=165b19487d4288-03fc45995da41b-9393265-1fa400-165b19487d59c; zg_did=%7B%22did%22%3A%20%22165b19488b91af-0fb9be3681a066-9393265-1fa400-165b19488ba2ba%22%7D; hasShow=1; _uab_collina=153628262639910554015981; acw_tc=7b7d07cf15362826301432205e30e281bd6a73b25c044da9c7a81a2244; _umdata=65F7F3A2F63DF0203254105527DA165EBBFD91DE1A3CDEA2269392857C04613958078EEC5FE86221CD43AD3E795C914C66114A2D2FEF9EE5A5205A702F1BED3E; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1536282626,1536288913; acw_sc__=5b92265df9698bd58156d27083162f8370ccf8fc; CNZZDATA1254842228=1367101856-1536277679-%252F%252Fwww.baidu.com%252F%7C1536304696; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201536303075504%2C%22updated%22%3A%201536304763564%2C%22info%22%3A%201536282626239%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%228854c239023a72ce86511b6e2d8587c8%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1536304764',
        'Connection': 'keep-alive',
        'Upgrade - Insecure - Requests': '1',
        'Cache-Control': 'max-age=0',
    }
def download_page(url):
    #proxies={'http':'http://115.28.100.127:80'}
    return requests.get(url, headers=headers).text

def parse_html(html):
    i = 0
    j = 0
    k = 0
    data = dict()
    content = etree.HTML(html)
    try:
        # 基本信息
        basic = content.xpath('//div[@class="row"]//div[@class="content"]/div/span')
        if len(basic) == 7:
            phone = basic[1].xpath('string(.)')
            guanwang = basic[3].xpath('string(.)')
            youxiang = basic[4].xpath('string(.)')
            dizhi = basic[6].xpath('string(.)')
        elif len(basic) == 9:
            phone = basic[2].xpath('string(.)')
            youxiang = basic[4].xpath('string(.)')
            guanwang = basic[6].xpath('string(.)')
            dizhi = basic[8].xpath('string(.)')
        else:
            phone = '暂无'
            youxiang = '暂无'
            guanwang = '暂无'
            dizhi = '暂无'
        data['phone'] = phone.replace(' 电话：', '').replace(' 更多号码', '').strip()
        data['webSite'] = guanwang.replace('流量分析', '').strip()
        data['email'] = youxiang.replace(' 邮箱：', '').strip()
        data['officialAddress'] = dizhi.replace('附近公司', '').strip()

        # 工商信息
        faren_initial = content.xpath('//section[@id="Cominfo"]//div[@class="pull-left"]/a[1]')
        faren = faren_initial[0].xpath('string(.)')
        name_basic = content.xpath('//div[@class="row title"]')
        cnName = name_basic[0].xpath('string(.)')
        d = PyQuery(html)
        td = d('#Cominfo > table').eq(1)('td')
        data['cnName'] = cnName.replace('曾用名', '').replace('存续', '').replace('在业', '').replace('正常', '').replace(
            '注销', '').replace('仍注册', '').replace('吊销', '').strip()
        if td.eq(1).text() != '':
            data['registeredCapital'] = td.eq(1).text()
        else:
            data['registeredCapital'] = '无'
        if td.eq(3).text() != '':
            data['paidInCapital'] = td.eq(3).text()
        else:
            data['paidInCapital'] = '无'
        if td.eq(5).text() != '':
            data['status'] = td.eq(5).text()
        else:
            data['status'] = '无'
        if td.eq(7).text() != '' or td.eq(7).text() != '-':
            data['foundDate'] = td.eq(7).text()
        else:
            data['foundDate'] = '2015-07-22'
        if td.eq(9).text() != '' or td.eq(9).text() != '-':
            data['unifiedSocialCreditCode'] = td.eq(9).text()
        else:
            data['unifiedSocialCreditCode'] = '00000000000000000A'
        if td.eq(11).text() != '' or td.eq(11).text() != '-':
            data['taxpayerID'] = td.eq(11).text()
        else:
            data['taxpayerID'] = '00000000000000000A'
        if td.eq(13).text() != '' or td.eq(13).text() != '-':
            data['registerCode'] = td.eq(13).text()
        else:
            data['registerCode'] = '000000000000000'
        if td.eq(15).text() != '' or td.eq(15).text() != '-':
            data['orgCode'] = td.eq(15).text()
        else:
            data['orgCode'] = '00000000-0'
        if td.eq(17).text() != '':
            data['category'] = td.eq(17).text()
        else:
            data['category'] = '无'
        if td.eq(19).text() != '':
            data['industry'] = td.eq(19).text()
        else:
            data['industry'] = '-'
        if td.eq(21).text() != '' or td.eq(21).text() != '-':
            data['approvalDate'] = td.eq(21).text()
        else:
            data['approvalDate'] = '2018-04-12'
        if td.eq(23).text() != '':
            data['registrationOrgan'] = td.eq(23).text()
        else:
            data['registrationOrgan'] = '-'
        if td.eq(25).text() != '':
            data['area'] = td.eq(25).text()
        else:
            data['area'] = '-'
        if td.eq(27).text() != '':
            data['enName'] = td.eq(27).text()
        else:
            data['enName'] = '-'
        data['oldName'] = td.eq(29).text()
        if td.eq(37).text() != '':
            data['registerAddress'] = td.eq(37).text().replace('查看地图', '').replace('附近公司', '')
        else:
            data['registerAddress'] = '-'
        if td.eq(39).text() != '':
            data['bizScope'] = td.eq(39).text()
        else:
            data['bizScope'] = '-'
        data['legalPerson'] = faren.strip()

        # 股东信息
        holder = []
        basic_gudong = content.xpath('//section[@id="Sockinfo"]//td[2]/a[1]')
        basic_gubi = content.xpath('//section[@id="Sockinfo"]//td[3]')
        basic_renjiao = content.xpath('//section[@id="Sockinfo"]//td[4]')
        basic_paiddate = content.xpath('//section[@id="Sockinfo"]//td[5]')
        basic_holdersort = content.xpath('//section[@id="Sockinfo"]//td[1]')
        while i < len(basic_gudong):
            data_holder = dict()
            name_length = len(basic_gudong[i].xpath('string(.)').strip())
            if name_length > 3:
                data_holder['type'] = "CORP"
                data_holder['sort'] = basic_holdersort[i].xpath('string(.)').strip()
                data_holder['corpName'] = basic_gudong[i].xpath('string(.)').strip()
                data_holder['proportion'] = basic_gubi[i].xpath('string(.)').strip()
                if  basic_renjiao[i].xpath('string(.)').strip() =='-':
                    data_holder['subscribedShare'] = 0
                else:
                    data_holder['subscribedShare'] = basic_renjiao[i].xpath('string(.)').replace('万元','').strip()
                if basic_paiddate[i].xpath('string(.)').strip() !='-':
                    data_holder['subscribedDate'] = basic_paiddate[i].xpath('string(.)').strip()
                else:
                    data_holder['subscribedDate'] ='2000-08-31'
            else:
                data_holder['type'] = "PERSON"
                data_holder['sort'] = basic_holdersort[i].xpath('string(.)').strip()
                data_holder['personName'] = basic_gudong[i].xpath('string(.)').strip()
                data_holder['proportion'] = basic_gubi[i].xpath('string(.)').strip()
                if basic_renjiao[i].xpath('string(.)').strip() == '-':
                    data_holder['subscribedShare'] = 0
                else:
                    data_holder['subscribedShare'] = basic_renjiao[i].xpath('string(.)').replace('万元', '').strip()
                if basic_paiddate[i].xpath('string(.)').strip() !='-':
                    data_holder['subscribedDate'] = basic_paiddate[i].xpath('string(.)').strip()
                else:
                    data_holder['subscribedDate'] ='2000-08-31'
                if  basic_gudong[i].xpath('string(.)').strip() == faren:
                    data_holder['legalPerson'] = "true"
                else:
                    data_holder['legalPerson'] = "false"
            i = i + 1
            holder.append(data_holder)

        # 主要成员
        member = []
        basic_member = content.xpath('//section[@id="Mainmember"]//td[2]/a[1]')
        basic_position = content.xpath('//section[@id="Mainmember"]//td[3]')
        basic_membersort = content.xpath('//section[@id="Mainmember"]//td[1]')
        while j < len(basic_member):
            data_member = dict()
            data_member['name'] = basic_member[j].xpath('string(.)').strip()
            data_member['position'] = basic_position[j].xpath('string(.)').strip()
            data_member['sort'] = basic_membersort[j].xpath('string(.)').strip()
            member.append(data_member)
            j += 1

        # 变更记录
        change = []
        basic_changesort = content.xpath('//section[@id="Changelist"]//td[1]')
        basic_changedate = content.xpath('//section[@id="Changelist"]//td[2]')
        basic_changeitem = content.xpath('//section[@id="Changelist"]//td[3]')
        basic_changebefore = content.xpath('//section[@id="Changelist"]//td[4]')
        basic_changeafter = content.xpath('//section[@id="Changelist"]//td[5]')
        while k < (len(content.xpath('//section[@id="Changelist"]//tr')) - 1):
            data_change = dict()
            data_change['changeDate'] = basic_changedate[k].xpath('string(.)').strip().replace('\n', '').replace(
                '                带有*标记的为法定代表人', '')
            data_change['sort'] = basic_changesort[k].xpath('string(.)').strip().replace('\n',
                                                                                               '').replace(
                '                带有*标记的为法定代表人', '')
            data_change['changeItem'] = basic_changeitem[k].xpath('string(.)').strip().replace('\n', '').replace(
                '                     ', '').replace('                带有*标记的为法定代表人', '')
            data_change['changeBefore'] = basic_changebefore[k].xpath('string(.)').strip().replace('\n',
                                                                                             '').replace(
                '                     ', '').replace('                带有*标记的为法定代表人', '')
            data_change['changeAfter'] = basic_changeafter[k].xpath('string(.)').strip().replace('\n',
                                                                                           '').replace(
                '                     ', '').replace('                带有*标记的为法定代表人', '')

            data_member['sort'] = basic_changesort[k].xpath('string(.)').strip()
            change.append(data_change)
            k += 1
        data['shareholders'] = holder
        data['changeHistories'] = change
        data['members'] = member
        print(data)
        file = json.dumps(data)
        header = {'content-type': 'application/json'}
        post_url = 'post-url'
        r = requests.post(post_url,data=file,headers=header)
        print(r)
    except Exception as e:
        print(e)

def main():
    Download_Url = 'https://www.qichacha.com/g_SH_'
    url_list = []
    a = 400
    b = a*10
    while a < 500:
        a += 1
        url = Download_Url + str(a) + '.html'
        if url!='':
            html = download_page(url)
            # time.sleep(30)
            data = etree.HTML(html)
            url_li = data.xpath('//div[@class="row"]//section/a/@href')
            for url_ in url_li:
                DOWNLOAD_URL = 'https://www.qichacha.com' + url_
                html = download_page(DOWNLOAD_URL)
                # time.sleep(20)
                parse_html(html)
                b += 1
                print(b)
        else:
            break

if __name__ == '__main__':
    main()


