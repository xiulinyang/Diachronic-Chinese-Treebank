import urllib
from urllib import request
import re
from bs4 import BeautifulSoup as bf
import datetime
import ssl
import random
ssl._create_default_https_context = ssl._create_unverified_context

'''GET THE NEWS FROM PEOPLE'S DAILY(1950-2003) AND REFERENCE NEWS(1950-2002)'''
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

# cf. https://blog.csdn.net/qq_34869990/article/details/103382782
def get_date(start, end):
    datalist = []
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        datalist.append(datestart.strftime('%Y-%m-%d'))
    return datalist


# get the the date that People's Daily is available

ppl_first = get_date('1950-1-1', '1965-12-31')
ppl_second = get_date('1966-1-1', '1977-12-31')
ppl_third = get_date('1978-1-1', '1999-12-31')
ppl_fourth = get_date('2000-1-1', '2003-12-31')
ppl_base_url = 'https://www.laoziliao.net/rmrb/'


# define a function generating all possible urls for newspaper extraction.
def get_url(base_url, date_collection, num1, num2):
    url_collection = []
    for date in date_collection:
        for i in range(num1, num2):
            url = base_url + str(date) + '-' + str(i)
            url_collection.append(url)
    return url_collection


# get all possible url link and calculate the number of them
ppl_collection_first = get_url(ppl_base_url, ppl_first, 1, 7)
print(len(ppl_collection_first))
ppl_collection_second = get_url(ppl_base_url, ppl_second, 1, 7)
print(len(ppl_collection_second))
ppl_collection_third = get_url(ppl_base_url, ppl_third, 1, 5)
print(len(ppl_collection_third))
ppl_collection_fourth = get_url(ppl_base_url, ppl_fourth, 1, 6)
print(len(ppl_collection_fourth))


# Define a function to get the data from People's Daily
def getText(collection):
    txt = []
    for i, url in enumerate(collection):
        if i % 5 == 0:
            print(str(i) + ' urls have been read. And the current url is ' + str(url))
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req).read().decode('utf-8')
        text = bf(res, 'html.parser').find_all('div', class_='article')
        text2 = re.sub(r'(<br/>)|(</*div\s*(class="article")*>)', '', str(text))
        text3 = re.sub(r'】', ' ', text2)
        text_final = text3.split()
        for para in text_final:
            if len(para) > 15:
                txt.append(para)
    return txt


# calculate the number of characters and text is a list type
def textlen(text):
    num = 0
    for i in range(len(text)):
        num += len(text[i])
    return num


def characterlen(text):
    pat = r"\w"
    num = 0
    for i in range(len(text)):
        num += len(re.findall(pat, text[i]))
    return num


'''As there are so many links and 10 urls have approximately 65000 characters on average,
this program only extracts random 100 ones from People's Daily. '''
'''Randomly choose 100 urls according to their percentage in the corpus design.'''
random_url_50 = random.sample(ppl_collection_first, 25)
random_url_66 = random.sample(ppl_collection_second, 5)
random_url_77 = random.sample(ppl_collection_third, 35)
random_url_00 = random.sample(ppl_collection_fourth, 35)


# store text into txt.file
def storeText(data, filename):
    file_work = open(filename, "w")
    for para in data:
        file_work.write(para)


# get all possible links from Reference News
refnews_first = get_date('1957-3-1', '1965-12-31')
refnews_second = get_date('1966-1-1', '1976-12-31')
refnews_third = get_date('1977-1-1', '1999-12-31')
refnews_fourth = get_date('2000-1-1', '2002-12-31')

ref_base_url = 'https://www.laoziliao.net/ckxx/'
ref_collection_first = get_url(ref_base_url, refnews_first, 1, 5)
ref_collection_second = get_url(ref_base_url, refnews_second, 1, 5)
ref_collection_third = get_url(ref_base_url, refnews_third, 1, 5)
ref_collection_fourth = get_url(ref_base_url, refnews_fourth, 1, 16)

refdom_url_50 = random.sample(ref_collection_first, 25)
refdom_url_66 = random.sample(ref_collection_second, 5)
refdom_url_77 = random.sample(ref_collection_third, 35)
refdom_url_00 = random.sample(ref_collection_fourth, 35)

news50 = getText(refdom_url_50) + getText(random_url_50)
news66 = getText(refdom_url_66) + getText(random_url_66)
news78 = getText(refdom_url_77) + getText(random_url_77)
news00 = getText(refdom_url_00) + getText(random_url_00)


# cut sentences function
# cf. https://blog.csdn.net/zhuzuwei/article/details/80487032
def cut_sents(textlist):
    new_sents = []
    for text in textlist:
        sents = re.split(r'(。"*）*」*|！"*）*」*|？"*|\.{6}"*」*）*|……"*）*」*|\.」*)', text)
        for i in range(int(len(sents) / 2)):
            sent = sents[2 * i] + sents[2 * i + 1]
            new_sents.append(sent)
    for sent in new_sents:
        re.sub('……+', '', sent)
    return new_sents


news50 = cut_sents(news50)
news66 = cut_sents(news66)
news78 = cut_sents(news78)
news00 = cut_sents(news00)

'''Design a function to randomly extract a specific number of sentences
 and the sum of characters should locate between num1 and num2.'''


def build_corpus(text, num1, num2):
    optimal_solution = -1
    min_dis = 100000
    for i in range(1, len(text)+1):
        corpus = random.sample(text, i)
        text_len = textlen(corpus)
        dis = int(abs(text_len-(num1+num2)/2))
        if dis < min_dis:
            min_dis = dis
            optimal_solution = i
        if num1 < text_len & text_len < num2:
            return corpus
    for j in range(1, 100):
        corpus = random.sample(text, optimal_solution)
        text_len = textlen(corpus)
        if num1 < text_len & text_len < num2:
            return corpus



'''
Similalry, this function is to guarantee the golden corpus 
has at least 5000 Chinese characters.
'''


def build_sample_corpus(text, num1, num2):
    optimal_solution = -1
    min_dis = 100000
    for i in range(1, len(text) + 1):
        corpus = random.sample(text, i)
        char_len = characterlen(corpus)
        dis = int(abs(char_len - (num1 + num2)/2))
        if dis < min_dis:
            min_dis = dis
            optimal_solution = i
        if num1 < char_len & char_len < num2:
            return corpus
    for j in range(1, 100):
        corpus = random.sample(text, optimal_solution)
        char_len = characterlen(corpus)
        if num1 < char_len & char_len < num2:
            return corpus


# extract news from various time periods:
corpnews_50 = build_corpus(news50, 75000, 75200)
'''政府报告字数不够了，在这里加2000'''
corpnews_66 = build_corpus(news66, 18000, 18200)
corpnews_78 = build_corpus(news78, 105000, 105200)
corpnews_00 = build_corpus(news00, 105000, 105200)
print(type(corpnews_00))
print(type(corpnews_66))
print(type(corpnews_78))
print(type(corpnews_50))
print(textlen(corpnews_66))
print(textlen(corpnews_00))
print(textlen(corpnews_78))
print(textlen(corpnews_50))


'''LITERATURE & OTHERS'''
''' Literature works are extracted from various websites based on 
Donglin Zhu, Xiaojin Zhu, and Yiqin Wu's (2014) History of Chinese Modern Literature.'''

'''As most of the works are composed of various sections embedded in other urls,
the following codes define a function to get all urls.'''


def get_url(oneurl):
    url_coll = []
    res = urllib.request.Request(url=oneurl, headers=headers)
    rep = urllib.request.urlopen(res).read().decode('utf-8', 'ignore')
    urls = bf(rep, 'html.parser').find_all('a')
    for data in urls:
        url_coll.append(data.get('href'))
    return url_coll


'''get all the urls for Chinese Government report from 1954 to 2013 
(no report from 1966 to 1976 due to the culture revolution'''

finalurl = []
govurl = get_url('http://www.gov.cn/2013zfbgjjd/lnzf.htm')
for i, url in enumerate(govurl):
    if len(url) >= len('../test/2006-02/23/content_208705.htm'):
        finalurl.append(re.sub(r'\.\.', 'http://www.gov.cn', url))

finalurl.remove('http://www.gov.cn/test/2012-03/15/content_2067314.htm')
finalurl.insert(0, 'http://www.gov.cn/2011lh/content_1825233.htm')
print(len(finalurl))  # check the number


def get_work_gbk(collection):
    col = []
    try:
        for i, url in enumerate(collection):
            if i % 5 == 0:
                print(str(i) + ' urls have been processed. And the current url is ' + str(url))
            res = urllib.request.Request(url=url, headers=headers)
            rep = urllib.request.urlopen(res).read().decode('gbk', 'ignore')
            text = bf(rep, 'html.parser').find_all('p')
            text = re.sub(r'(</*p>)|(</*br/*>)|(\r)|(\n)|(\[)|(<!*-*script-*>)|(<u>一</u><u>哦</u>)','', str(text))
            text = text.replace(r'</p>, <p>', '')
            text = text.replace(u'\xa0', u'')
            text = text.replace(u'\u3000', u'')
            text = text.replace(r'[<td class="content" colspan="3">)', '')
            col.append(text)
    except urllib.error.HTTPError:
        pass
    return col


def comp_url(num1, num2, prefix, suffix):
    urlcol = []
    for i in range(num1, num2 + 1):
        url = prefix + str(i) + suffix
        urlcol.append(url)
    return urlcol


# get the report
def get_work(urlcollection):
    work = []
    try:
        for i, url in enumerate(urlcollection):
            if i % 5 == 0:
                print(str(i) + ' url(s) are processed. And the current url is ' + str(url))
            res = urllib.request.Request(url=url, headers=headers)
            rep = urllib.request.urlopen(res).read().decode('utf-8', 'ignore')
            text = bf(rep, 'html.parser').find_all('p')
            text = re.sub(r'(</*p>,*)|(</*strong>)|([a-zA-Z]*)', '', str(text))
            text = text.replace(u'\u3000', u'')
            text = text.replace(r'<br>', '')
            text = text.replace(u'\xa0', u'')
            text = text.replace(r'·鲲·弩·小·说  w w w_k u n n u_c o m', '')
            work.append(text)
    except urllib.error.URLError:
        pass
    return work

govrep_00 = get_work(finalurl[:11])
govrep_78 = get_work(finalurl[11:33])


url = finalurl[33]
res1 = urllib.request.Request(url=url, headers=headers)
rep1 = urllib.request.urlopen(res1).read().decode('utf-8')
text1 = bf(rep1, 'html.parser').find_all('p')
text1 = re.sub(r'(</*p>,*)|(</*strong>)|(\u3000)|(\xa0)', '', str(text1))
govrep_6 = re.split(r'(。"*）*|！"*）*|？"*|\.{6}"*）*|……"*）*|\.)', text1)
govrep_66 = []
for i in range(int(len(govrep_6) / 2)):
    sent1 = govrep_6[2 * i] + govrep_6[2 * i + 1]
    govrep_66.append(sent1)
govrep_50 = get_work(finalurl[34:])
govrep_50 = cut_sents(govrep_50)
govrep_78 = cut_sents(govrep_78)
govrep_00 = cut_sents(govrep_00)

print('There are ' + str(textlen(govrep_00) + textlen(govrep_50) + textlen(govrep_66) + textlen(
    govrep_78)) + ' characters in government reports.')

corpgovrep_50 = build_corpus(govrep_50[5:-5], 50000, 50200)
corpgovrep_66 = build_corpus(govrep_66[5:-5], 4000, 4200)
corpgovrep_78 = build_corpus(govrep_78[5:-5], 50000, 50200)
corpgovrep_00 = build_corpus(govrep_00[5:-5], 50000, 50200)
print(textlen(corpgovrep_50))
print(textlen(corpgovrep_66))
print(textlen(corpgovrep_78))
print(textlen(corpgovrep_00))

'''Literature'''

'''1950-1965
Fiction
https://www.kunnu.com/chuangyeshi/cys-1/ 创业史
http://www.dushu369.com/zhongguomingzhu/qczg/ 青春之歌
Prose
https://www.xyyuedu.com/writer/laoshexs/laoshesanwenji/ 老舍
http://www.dushu369.com/zhongguomingzhu/ysyh/ 燕山夜话 1962
http://www.bdwenxue.com/sanwen/sanwensuibi/2018-11-25/504.html 臧克家
Others
https://www.kanunu8.com/book3/6073/ 从文自传 1949
https://www.xstt5.com/mingzhu/1454/ 茶馆 1955

https://www.kanunu8.com/book3/8023/ 老舍自传
Sci-fi
https://www.99csw.com/article/4680.htm From the Earth to the March 1950
https://m.shutxt.com/kh/9338/526940.html 割掉鼻子的大象'''

lit_501 = comp_url(157696, 157748, 'https://www.qiyao5200.com/book/3/3192/', '.html')
lit_502 = comp_url(185687, 185716, 'https://www.kanunu8.com/book3/8368/', '.html')
lit_503 = comp_url(174774, 174789, 'https://www.kanunu8.com/book3/7993/', '.html')
lit_504 = comp_url(79356, 79358, 'https://www.xstt5.com/mingzhu/1454/', '.html')
lit_505 = comp_url(17085, 17160, 'http://www.dushu369.com/zhongguomingzhu/HTML/', '.html')
lit_506 = comp_url(175626, 175654, 'https://www.kanunu8.com/book3/8023/', '.html')
lit_507 = comp_url(107404, 107420, 'https://www.kanunu8.com/book3/6073/', '.html')
lit_508 = comp_url(174705, 174751, 'https://www.kanunu8.com/book3/7991/', '.html')
lit_509 = comp_url(115522, 115536, 'https://www.kanunu8.com/book3/6484/', '.html')
lit_510 = comp_url(176216, 176230, 'https://www.kanunu8.com/book3/8062/', '.html')
litext_501 = []
for i, url in enumerate(lit_501):
    if i % 5 == 0:
        print(str(i) + ' url(s) are processed. And the current url is ' + str(url))
    res7 = urllib.request.Request(url=url, headers=headers)
    rep7 = urllib.request.urlopen(res7).read().decode('gbk', 'ignore')
    text7 = bf(rep7, 'html.parser').find_all('div', id="ChapterContents")
    text7 = re.sub(r'<br/>|(</*div/*>)|(\r)|(\n)', '', str(text7))
    text7 = text7.replace(r'<div class="page-content" id="ChapterContents">', '')
    text7 = text7.replace(u'\xa0', u'')
    litext_501.append(text7)
litext_501 = cut_sents(litext_501)
litext_502 = cut_sents(get_work_gbk(lit_502))
litext_503 = cut_sents(get_work_gbk(lit_503))
litext_504 = cut_sents(get_work(lit_504))
litext_505 = []
for i, url in enumerate(lit_505):
    if i % 5 == 0:
        print(str(i) + ' url(s) are processed.')
    res6 = urllib.request.Request(url=url, headers=headers)
    rep6 = urllib.request.urlopen(res6).read().decode('gbk', 'ignore')
    text6 = bf(rep6, 'html.parser').find_all(class_='content')
    text6 = re.sub(r'(</*br/*>)|(\r)|(\n)|(<!--script-*>)', '', str(text6))
    text6 = text6.replace(u'\u3000', u'')
    text6 = text6.replace(r'[<td class="content" colspan="3">', '')
    litext_505.append(text6)
litext_505 = cut_sents(litext_505)
litext_506 = cut_sents(get_work_gbk(lit_506))
litext_507 = cut_sents(get_work_gbk(lit_507))
litext_508 = cut_sents(get_work_gbk(lit_508))
litext_509 = cut_sents(get_work_gbk(lit_509))
litext_510 = cut_sents(get_work_gbk(lit_510))
a = open('sci_fi_50', 'r').read()
sci = re.sub(r'(\n)|(\u3000)', '', str(a))
sci_50 = cut_sents([sci])

print(litext_501)
# build a corpus
text_501 = build_corpus(litext_501[5:-5], 32150, 32350)
text_502 = build_corpus(litext_502[5: -5], 32150, 32350)
text_503 = build_corpus(litext_503[5: -5], 10300, 10500)
text_504 = build_corpus(litext_504[5: -5], 4450, 4650)
text_505 = build_corpus(litext_505[5: -5], 10300, 10500)
text_506 = build_corpus(litext_506[5: -5], 4650, 4850)
text_507 = build_corpus(litext_507[5: -5], 3000, 3200)
text_508 = build_corpus(sci_50[1:-2], 3000, 3200)
text_509 = build_corpus(litext_508[5:-5], 7000, 7200)
text_510 = build_corpus(litext_509[5:-5], 6400, 6600)
text_511 = build_corpus(litext_510[5:-5], 9300, 9500)

print(type(text_501))
print(type(text_502))
print(type(text_503))
print(type(text_504))
print(type(text_505))
print(type(text_506))
print(type(text_507))
print(type(text_508))
print(type(text_509))
print(type(text_510))
print(type(text_511))
print(textlen(text_507))
print(textlen(text_508))
corpus_50 = corpnews_50 + corpgovrep_50 + text_501 + text_502 + text_503 + text_504 + text_505 + \
            text_506 + text_507 + text_508 + text_509 + text_510 + text_511
storeText(corpus_50, 'corpus_50_65.txt')


sample_corpus_50 = build_sample_corpus(corpus_50, 1200, 1300)
print(sample_corpus_50)
print(textlen(sample_corpus_50))

'''
https://www.yooread.net/6/2072/ 浩然 艳阳天 1964+
'''
lit_66 = comp_url(63850, 63940, 'https://www.yooread.net/6/2072/', '.html')
litext_66 = []
for i, url in enumerate(lit_66):
    if i % 5 == 0:
        print(str(i) + ' url(s) are processed. And the current url is ' + str(url))
    res5 = urllib.request.Request(url=url, headers=headers)
    rep5 = urllib.request.urlopen(res5).read().decode('utf-8', 'ignore')
    text5 = bf(rep5, 'html.parser').find_all('p')
    text5 = re.sub(r'<|=|"|_|>|/|,|\d*|\(\);|\.|\w*书签|\+|\?|&|;|([a-zA-Z]*)|(</*p>,*)|(</*strong>)', '', str(text5))
    litext_66.append(text5[:-16])
litext_66 = cut_sents(litext_66)
text_66 = build_corpus(litext_66[5:-5], 28000, 28200)
print(type(text_66))
print(type(corpgovrep_66))
print(type(corpnews_66))
corpus_66 = corpgovrep_66 + corpnews_66 + text_66
storeText(corpus_66, 'corpus_66_76.txt')

sample_corpus_66 = build_sample_corpus(corpus_66, 200, 280)
print(sample_corpus_66)

'''1978-1999
Fiction
https://www.99csw.com/book/2683/index.htm 人到中年 1990
https://www.99csw.com/book/2603/index.htm 爸爸爸 1985
https://www.99csw.com/book/1083/index.htm 绿化树 1984
https://www.99csw.com/book/2426/index.htm 许三观卖血记 1995
https://www.kanunu8.com/book4/8929/ 洗澡 1988
https://www.kanunu8.com/book/3980/index.html 永远有多远 1999

Prose
http://www.dushu369.com/zhongguomingzhu/suixianglu/ 随想录 巴金 1980-1986
https://www.xstt5.com/mingzhu/1233/ 文化苦旅 1992
https://www.99csw.com/book/2289/68659.htm 汪曾祺 1987+
https://www.kanunu8.com/files/chinese/201104/2611/62666.html 贾平凹散文集
Others
https://www.xstt5.com/renwen/3459/ 李泽厚 美的历程 1981
https://www.kanunu8.com/book3/7056/ 他们的世界——中国男同性恋群落透视 1992
https://www.kanunu8.com/book4/8746/ 邓小平政治评传 1995
Essay and report
https://nuoha.com/book/chapter/82860/22.html 论阿Q的性格系统 1984
http://www.people.com.cn/item/20years/newfiles/b1020.html 实践是检验认识真理性的唯一标准 1978
Science and Detective Fiction
http://www.txshuku.la/mulu/45973.html 霍桑探案
https://www.kanunu8.com/book3/6483/index.html 飞向人马座 1978
https://www.shutxt.com/kh/22496/1282461.html  小岛上的珊瑚死光 1978
http://www.dushu369.com/tonghua/xltmywl/ 小灵通漫游未来 1978
http://www.kehuan.net.cn/book/yadanghuigui.html 亚当回归 1993
http://www.kehuan.net.cn/book/yiyefengkuang.html 一夜疯狂 1991'''

lit7801 = comp_url(22231, 22251, 'https://www.xstt5.com/dangdai/796/', '.html')


# get the report

def get_work_xstt(collection):
    litext = []
    for i, url in enumerate(collection):
        if i % 5 == 0:
            print(str(i) + ' url(s) are processed.')
        res = urllib.request.Request(url=url, headers=headers)
        rep = urllib.request.urlopen(res).read().decode('utf-8', 'ignore')
        text = bf(rep, 'html.parser').find_all(class_='zw')
        text = re.sub(r'(<br/*>)|(</*div>)|(\r)|(\n)|(</*p>)|([a-zA-Z])|\[', '', str(text))
        text = text.replace(r'<div class="zw">', '')
        text = text.replace(u'\xa0', u'')
        litext.append(text)
    return litext


litext_7801 = cut_sents(get_work_xstt(lit7801))

lit7802 = comp_url(301935, 301942, 'https://m.ksw8888.com/zuojia/hanshaogong/bababa/', '.html')

litext_7802 = cut_sents(get_work_gbk(lit7802))
print(litext_7802)
lit7803 = comp_url(66003, 66039, 'http://www.dushu369.com/zhongguomingzhu/HTML/', '.html')
litext_7803 = []
for i, url in enumerate(lit7803):
    if i % 5 == 0:
        print(str(i) + ' urls have been processed. And the current url is ' + str(url))
    res4 = urllib.request.Request(url=url, headers=headers)
    rep4 = urllib.request.urlopen(res4).read().decode('gbk', 'ignore')
    text4 = bf(rep4, 'html.parser').find_all(class_="content")
    text4 = re.sub(r'(</*p>)|(\r\n)|(</*br/*>)', '', str(text4)[34:-7])
    text4 = text4.replace(r'</p>, <p>', '')
    text4 = text4.replace(r'<u>[哦一]</u>', '')
    litext_7803.append(text4)
litext_7803 = cut_sents(litext_7803)
lit7804 = comp_url(159246, 159274, 'https://www.kanunu8.com/book3/7196/', '.html')
litext_7804 = cut_sents(get_work_gbk(lit7804))

litext_7805 = []
lit7805 = comp_url(100033, 100050, 'http://www.dushu369.com/zhongguomingzhu/HTML/', '.html')
for i, url in enumerate(lit7805):
    if i % 5 == 0:
        print(str(i) + ' urls have been processed.')
    res3 = urllib.request.Request(url=url, headers=headers)
    rep3 = urllib.request.urlopen(res3).read().decode('gbk', 'ignore')
    text3 = bf(rep3, 'html.parser').find_all('p')
    litext_7805.append(re.sub(r'(<br/*>)|(</*p>)|(\r)|(\n)|(\u3000)', '', str(text3)))
litext_7805 = cut_sents(litext_7805)

lit7806 = comp_url(36650, 36686, 'https://www.xstt5.com/mingzhu/1233/', '.html')
litext_7806 = cut_sents(get_work_xstt(lit7806))
lit7807 = comp_url(221302, 221311, 'https://www.xstt5.com/renwen/3459/', '.html')
# need to get rid of the first sentence
litext_7807 = cut_sents(get_work_xstt(lit7807))

lit7808 = comp_url(2542396, 2542411, 'http://www.txshuku.la/html/45973_', '.html')
litext_7808 = []
for url in lit7808:
    res2 = urllib.request.Request(url=url, headers=headers)
    rep2 = urllib.request.urlopen(res2).read().decode('gbk', 'ignore')
    text2 = bf(rep2, 'html.parser').find_all(id='htmlContent')
    text2 = re.sub(r'(</*br/*>)|(</*div>)|(</*p>)|(\r)|(\n)','', str(text2))
    text2 = text2.replace(r'<div class="contentbox" id="htmlContent">', '')
    text2 = text2.replace(u'\xa0', u'')
    text2 = text2.replace(u'\u3000', u'')
    litext_7808.append(text2)
litext_7808 = cut_sents(litext_7808)
lit_7809 = comp_url(115497, 115520, 'https://www.kanunu8.com/book3/6483/', '.html')
litext_7809 = cut_sents(get_work_gbk(lit_7809))
lit_7810 = comp_url(197722, 197733, 'https://www.kanunu8.com/book4/8929/', '.html')
litext_7810 = cut_sents(get_work_gbk(lit_7810))

lit_7811 = comp_url(147727, 147749, 'https://www.kanunu8.com/book3/7056/', '.html')
litext_7811 = cut_sents(get_work_gbk(lit_7811))

lit_7812 = comp_url(194321, 194329, 'https://www.kanunu8.com/book4/8746/', '.html')
litext_7812 = cut_sents(get_work_gbk(lit_7812))
lit_7813 = comp_url(42768, 42774, 'https://www.kanunu8.com/book/3980/', '.html')
litext_7813 = cut_sents(get_work_gbk(lit_7813))
lit_7814 = comp_url(182597, 182632, 'https://www.kanunu8.com/book3/8255/', '.html')
litext_7814 = cut_sents(get_work_gbk(lit_7814))
lit_7815 = comp_url(62666, 62706, 'https://www.kanunu8.com/files/chinese/201104/2611/', '.html')
litext_7815 = cut_sents(get_work_gbk(lit_7815))

text_7801 = build_corpus(litext_7801, 14500, 14700)
text_7802 = build_corpus(litext_7802, 14500, 14700)
text_7803 = build_corpus(litext_7803, 14400, 14600)
text_7804 = build_corpus(litext_7804, 14400, 14600)
text_7805 = build_corpus(litext_7805, 17500, 17700)
text_7806 = build_corpus(litext_7806, 17500, 17700)
text_7807 = build_corpus(litext_7807, 5800, 6000)
text_7808 = build_corpus(litext_7808, 8700, 8900)
text_7809 = build_corpus(litext_7809, 8700, 8900)
text_7810 = build_corpus(litext_7810, 14500, 14700)
text_7811 = build_corpus(litext_7811, 6600, 6800)
text_7812 = build_corpus(litext_7812, 6600, 6800)
text_7813 = build_corpus(litext_7813, 14500, 14700)
text_7814 = build_corpus(litext_7814, 14500, 14700)
text_7815 = build_corpus(litext_7815, 17500, 17700)

print(type(text_7801))
print(type(text_7802))
print(type(text_7803))
print(type(text_7804))
print(type(text_7805))
print(type(text_7806))
print(type(text_7807))
print(type(text_7808))
print(type(text_7809))
print(type(text_7810))
print(type(text_7811))
print(type(text_7812))
print(type(text_7813))
print(type(text_7814))
print(type(text_7815))

corpus_78 = corpnews_78 + corpgovrep_78 + text_7801 + text_7802 + text_7803 + \
            text_7804 + text_7805 + text_7806 + text_7807 + \
            text_7808 + text_7809 + text_7810 + text_7811 + text_7812 + text_7813 + text_7814 + text_7815
storeText(corpus_78, 'corpus_78_99.txt')

sample_corpus_78 = build_sample_corpus(corpus_78, 1730, 1830)
print(sample_corpus_78)
'''
1999-2010
fiction:
https://www.kanunu8.com/book3/7437/ 夏至未至 2005
https://www.kanunu8.com/book4/8852/ 最美的时光 2009
http://www.dushu369.com/zhongguomingzhu/yjdywj/ 一句顶一万句 2009
https://www.kanunu8.com/book3/8459/ 河岸
https://www.kanunu8.com/files/chinese/201101/1009.html 1988我想和这个世界谈谈 2010
prose:
https://www.99csw.com/book/2155/index.htm 2001 安妮宝贝 八月未央
https://www.51shucheng.net/qingchun/zadewen 2008 杂的文 韩寒
https://www.kanunu8.com/book/3937/index.html 往事并不如烟 2004
http://www.dushu369.com/shici/sanwen/bsmswj/ 毕淑敏
https://www.kanunu8.com/book/4389/index.html 被窝是青春的坟墓 七堇年 2007
others:
https://www.kanunu8.com/book3/7576/ 周国平 偶尔远行
https://www.danseshu.com/books/8814 中国农民调查 2003
https://www.kanunu8.com/book3/8112/ 刘心武揭秘红楼梦 2005
https://www.kanunu8.com/files/world/201102/1596.html 世界是平的，21世纪简史 2010
science and detective fiction:
https://www.kanunu8.com/tuili/10502/ 红色高跟鞋
https://www.kanunu8.com/book3/6640/ 乡村教师 2001
https://www.kanunu8.com/book3/6639/index.html 流浪地球 2000
https://www.kanunu8.com/book3/6623/index.html 泡泡 2007'''

lit_0001 = comp_url(163020, 163044, 'https://www.kanunu8.com/book3/7437/', '.html')
litext_0001 = cut_sents(get_work_gbk(lit_0001))

lit_0002 = comp_url(86612, 86635, 'http://www.dushu369.com/zhongguomingzhu/HTML/', '.html')
litext_0002 = cut_sents(get_work_gbk(lit_0002))

lit_0003 = comp_url(188052, 188065, 'https://www.kanunu8.com/book3/8459/', '.html')
litext_0003 = cut_sents(get_work_gbk(lit_0003))

lit_0004 = comp_url(41650, 41659, 'https://www.kanunu8.com/book/3937/', '.html')
litext_0004 = cut_sents(get_work_gbk(lit_0004))

lit_0005 = comp_url(99802, 99856, 'http://www.dushu369.com/shici/HTML/', '.html')
litext_0005 = []
for i, url in enumerate(lit_0005):
    if i % 5 == 0:
        print(str(i) + ' urls have been processed.')
    res7 = urllib.request.Request(url=url, headers=headers)
    rep7 = urllib.request.urlopen(res7).read().decode('gbk', 'ignore')
    text7 = bf(rep7, 'html.parser').find_all('p')
    text7 = re.sub(r'(</*p>)|(<br/*>)', '', str(text7))
    litext_0005.append(text7)
litext_0005 = cut_sents(litext_0005)
lit_0006 = comp_url(22824, 22903, 'https://www.cbxs.net/jishi/287/', '.html')
litext_0006 = []
for i, url in enumerate(lit_0006):
    if i % 5 == 0:
        print(str(i) + ' urls have been processed.')
    try:
        res8 = urllib.request.Request(url=url, headers=headers)
        rep8 = urllib.request.urlopen(res8).read().decode('utf-8', 'ignore')
        text8 = bf(rep8, 'html.parser').find_all(id='nr1')
        text8 = re.sub(r'(<div id="nr1">)|(</*p>)', '', str(text8))
        litext_0006.append(text8)
    except urllib.error.HTTPError:
        pass
litext_0006 = cut_sents(litext_0006)
lit_0007 = comp_url(183122, 183129, 'https://www.kanunu8.com/tuili/10502/', '.html')
litext_0007 = cut_sents(get_work_gbk(lit_0007))

lit_0008 = comp_url(116118, 116125, 'https://www.kanunu8.com/book3/6640/', '.html')
litext_0008 = cut_sents(get_work_gbk(lit_0008))

lit_0009 = comp_url(115827, 115831, 'https://www.kanunu8.com/book3/6623/', '.html')
litext_0009 = cut_sents(get_work_gbk(lit_0009))

lit_0010 = comp_url(199422, 199437, 'https://www.kanunu8.com/book4/8914/', '.html')
litext_0010 = cut_sents(get_work_gbk(lit_0010))
lit_0011 = comp_url(116113, 116116, 'https://www.kanunu8.com/book3/6639/', '.html')
litext_0011 = cut_sents(get_work_gbk(lit_0011))
lit_0012 = comp_url(37358, 37374, 'https://www.kanunu8.com/files/world/201102/1596/', '.html')
litext_0012 = cut_sents(get_work_gbk(lit_0012))

lit_0013 = comp_url(54420, 54455, 'https://www.kanunu8.com/book/4389/', '.html')
litext_0013 = cut_sents(get_work_gbk(lit_0013))

lit_0014 = comp_url(45910, 45926, 'https://www.kanunu8.com/files/chinese/201103/1976/', '.html')
litext_0014 = cut_sents(get_work_gbk(lit_0014))
lit_0015 = comp_url(195534, 195541, 'https://www.kanunu8.com/book4/8852/', '.html')
litext_0015 = cut_sents(get_work_gbk(lit_0015))

text_0001 = build_corpus(litext_0001, 17500, 17700)
text_0002 = build_corpus(litext_0002, 17500, 17700)
text_0003 = build_corpus(litext_0003, 17400, 17600)
text_0004 = build_corpus(litext_0004, 17500, 17700)
text_0005 = build_corpus(litext_0005, 17500, 17700)
text_0006 = build_corpus(litext_0006, 8750, 8950)
text_0007 = build_corpus(litext_0007, 4370, 4570)
text_0008 = build_corpus(litext_0008, 4370, 4570)
text_0009 = build_corpus(litext_0009, 4370, 4570)
text_0010 = build_corpus(litext_0010, 10000, 10200)
text_0011 = build_corpus(litext_0011, 4370, 4570)
text_0012 = build_corpus(litext_0012, 10000, 10200)
text_0013 = build_corpus(litext_0013, 17300, 17500)
text_0014 = build_corpus(litext_0014, 17300, 17500)
text_0015 = build_corpus(litext_0015, 17400, 17600)

print(type(text_0001))
print(type(text_0002))
print(type(text_0003))
print(type(text_0004))
print(type(text_0005))
print(type(text_0006))
print(type(text_0007))
print(type(text_0008))
print(type(text_0009))
print(type(text_0010))
print(type(text_0011))
print(type(text_0012))
print(type(text_0013))
print(type(text_0014))
print(type(text_0015))

corpus_00 = corpnews_00 + corpgovrep_00 + text_0001 + text_0002 + text_0003 + text_0004 + text_0005 + text_0006 + text_0007 + text_0008 + text_0009 + text_0010 + text_0011 + text_0012 + text_0013 + text_0014 + text_0015

storeText(corpus_00, 'corpus_00_10.txt')

sample_corpus_00 = build_sample_corpus(corpus_00, 1750, 1850)


'''Building a golden corpus'''
sample_corpus = sample_corpus_00 + sample_corpus_78 + sample_corpus_66 + sample_corpus_50
storeText(sample_corpus, 'sample_corpus.txt')




'''Have an overview of the corpus size'''
print('There are ' + str(textlen(sample_corpus)) +
      ' characters in the sample corpus (including punctuation characters).')
print('There are ' + str(characterlen(sample_corpus)) +
      ' characters in the sample (without punctuation characters).')

print('There are ' + str(textlen(corpus_50)) + ' characters in corpus 1950-1965 (including punctuation characters).')
print('There are ' + str(characterlen(corpus_50)) + ' characters in corpus 1950-1965 (without punctuation characters).')


print('There are ' + str(textlen(corpus_66)) + ' characters in corpus 1966-1976 (including punctuation characters).')
print('There are ' + str(characterlen(corpus_66)) + ' characters in corpus 1966-1976 (without punctuation characters).')

print('There are ' + str(textlen(corpus_78)) + ' characters in corpus 1978-1999 (including punctuation characters).')
print('There are ' + str(characterlen(corpus_78)) + ' characters in corpus 1978-1999 (without punctuation characters).')

print('There are ' + str(textlen(corpus_00)) + ' characters in corpus 2000-2010 (including punctuation characters).')
print('There are ' + str(characterlen(corpus_00)) + ' characters in corpus 2000-2010 (without punctuation characters).')

print('There are ' + str(textlen(corpus_50) + textlen(corpus_66) + textlen(corpus_78) + textlen(corpus_00)) +
      ' characters in corpus (including punctuation characters)')

print('There are ' + str(characterlen(corpus_50) + characterlen(corpus_66) + characterlen(corpus_78) + characterlen(corpus_00)) +
      ' characters in corpus (without punctuation characters)')