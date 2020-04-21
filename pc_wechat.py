from selenium import webdriver
import time,re,os
import requests

class crawl_jiandan(object):
    def __init__(self,offset=0):
        self._url='https://mp.weixin.qq.com/mp/profile_ext?'
        self.query_data={'action':'getmsg',
'__biz':'MzAxODYxNDA1OA==',
'f':'json',
'offset':str(offset),
'count':'10',
'is_ok':'1',
'scene':'124',
'uin':'MTc5NTA0NzExNg==',
'key':'8f662e0cdb8668e564696a09aa9b5a5f43bb59237697d7560caf905139b3b0b82c59d8f963b926363c57976ef3e36e633ff6d2f2bcf34fa00aec00b40c739d28a31d18fe50c4fca2b85749aa6c178c2f',
'pass_ticket':'XCfnaGIcL5xjNyUeIa0cW3Ep000/FTXzdtxc9JhjDOx6To5QPzJzuz1bnc7wgN0l',
'x5':'0',}
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        self.cookies={'Cookie':'pgv_pvi=1300235264; eas_sid=X1o4j9H6D1s068H8a494E9k173; RK=tNEH/rgLYw; tvfe_boss_uuid=a405038974a386e3; pac_uid=1_739535841; LW_sid=Z1f5c03038Z1v5w3S3u4S3i8l3; LW_uid=l1e5H0Z0T8W1R503B3V4e3g8D5; pgv_pvid=2738188268; o_cookie=739535841; ptui_loginuin=739535841; ptcz=94ac2a266a9f4f073f9d2df9f3c47b7fe1736c8e6cd7a0d7b8c3340e67128c1d; pt2gguin=o0739535841; ua_id=VpBkVua4RqwJsPsqAAAAAHAXs__VtHlT-qtdtN5agAA=; pgv_si=s2265438208; wxtokenkey=ec31bd588082ba09f4e0931d9816d523044a6692b5d00aff334ba0f4355fa986; wxuin=1795047116; pass_ticket=XCfnaGIcL5xjNyUeIa0cW3Ep000/FTXzdtxc9JhjDOx6To5QPzJzuz1bnc7wgN0l; wap_sid2=CMz9+NcGElxPS2JidTEwLWlOUGRGX0VTRmY3M2ZHVUxqTlRnUmlGWURMTHRJcFdkVk5zOTdaR1JfTmJZQVY1MktaS3dlZjlldVNDQXplckRzTVRzd2h0RnNzQ09pcE1EQUFBfjCdq+TLBTgMQJRO'}


    def get_page_data(self):
        try:
            html=requests.get(self._url,headers=self.headers,params=self.query_data,cookies=self.cookies,timeout=3,verify=False).text
            if 'title' in html:
                self.log('抓取网页成功，返回码为：',requests.get(self._url,headers=self.headers,params=self.query_data,cookies=self.cookies,timeout=3,verify=False).status_code)
            else:
                self.log('抓取完毕,退出程序')
                exit()
            return html
        except:
            self.log('获取网页失败，错误码为:',requests.get(self._url,headers=self.headers,params=self.query_data,cookies=self.cookies,timeout=3,verify=False).status_code)

    def get_title_data(self,html):
        title_list=[]
        title_pattern = re.compile(r'\\"title\\":\\".*?\\"')
        titles = title_pattern.findall(html)
        for title in titles:
            after_re = re.sub('\\\\', '', title).replace('title','').replace('"','').replace(':','')
            title_list.append(after_re)
        return title_list

    def get_url_data(self,html):
        url_list=[]
        url_pattern = re.compile(r'http:\\\\\\/\\\\\\/mp.weixin.qq.com\\\\\\/s?.*?\\"')
        urls = url_pattern.findall(html)
        for url in urls:
            after_re = re.sub(r'\\\\\\', '', url).replace('&amp', '&').replace(';', '')
            url_list.append(after_re)
        return url_list

    def get_date_data(self,html):
        date_list=[]
        date_pattern = re.compile(r'201\d{1}\\\\\\/\d{2}\\\\\\/\d{2}')
        dates = date_pattern.findall(html)
        for date in dates:
            after_re = re.sub(r'\\\\\\', '', date).replace('/','_')
            date_list.append(after_re)
        return date_list

    def store_page(self,urls,date,title):
        path='E:\jiandan\gongzhonghao\%s'%date
        if not os.path.exists(path):
            os.makedirs(path)
        title=title.replace('?','').replace(':','').replace('/','').replace('\\','').replace(('*'),'')#windows不允许文件名有这些符号出现
        file_name='%s\%s.html'%(path,title)
        print(file_name)
        page = self.parse_url(urls)
        with open(file_name, 'w', encoding='utf-8')as f:
            f.write(page)
        self.log('网页保存成功')

    def parse_url(self, url):
        browser = webdriver.PhantomJS()
        browser.get(url)
        time.sleep(3)
        html = browser.execute_script("return document.documentElement.outerHTML")  # 执行js语句，得到整个网页的DOM
        return html

    def log(self, msg,var=''):
        print('%s,%s%s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg,var))

    def run(self):
        self.log('开始爬取煎蛋公众号信息')
        html=self.get_page_data()
        titles=self.get_title_data(html)
        urls=self.get_url_data(html)
        dates=self.get_date_data(html)
        for title ,url,date in zip(titles,urls,dates):
            self.store_page(url,date,title)

if __name__ == '__main__':
    offset=0  
    while True:
        print(offset)
        crawl_jiandan(offset).run()
        offset+=10

# 加一行
