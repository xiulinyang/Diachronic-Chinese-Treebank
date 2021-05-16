import urllib
from urllib import request
import re
from bs4 import BeautifulSoup as bf
import datetime
import ssl
import random
from main import get_corp
ssl._create_default_https_context = ssl._create_unverified_context
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

'''NECESSARY FUNCTIONS TO GET AND STORE THE DATA'''


'''FUNCTIONS USED TO EXTRACT DATA FROM PEOPLE'S DAILY AND REFERENCE NEWS'''
# get the data to form the complete web links.
def get_date(start, end):
    datalist = []
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        datalist.append(datestart.strftime('%Y-%m-%d'))
    return datalist



# define a function generating all possible urls for newspaper extraction.
def get_url(base_url, time1, time2,num):
    url_collection = []
    for date in get_date(time1, time2):
        for i in range(1, 7):
            url = base_url + str(date) + '-' + str(i)
            url_collection.append(url)
    url_collection= random.sample(url_collection, num)
    return url_collection

# Two base urls I will use for this project which are People's Daily and Reference News respectively.
ppl_base_url = 'https://www.laoziliao.net/rmrb/'
ref_base_url = 'https://www.laoziliao.net/ckxx/'

# Define a function to extract and clean the data from People's Daily/Reference News
def get_text(base_url, time1, time2, num):
    collection = get_url(base_url, time1, time2, num)
    txt = []
    for i, url in enumerate(collection):
        if i%2 == 0:
            print(str(i) + ' urls have been read. And the current url is ' + str(url))
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req).read().decode('utf-8')
        text = bf(res, 'html.parser').find_all('div', class_='article')
        text2 = re.sub(r'(<br/>)|(</*div\s*(class="article")*>)', '', str(text))
        text3 = re.sub(r'】', ' ', text2)
        text_final = text3.split()
        for para in text_final:
            if len(para) > 15:
                # Usually if the length of a sentence is smaller than 15, it is a title.
                txt.append(para)
    return txt

# the function of cutting sentences
def cut_sents(textlist):
    new_sents = []
    for text in textlist:
        sents = re.split(r'(。”*"*）*」*|！”*"*）*」*|？”*"*|\.{6}”*」"*）*|……”*）*"*」*|;"*|：)', text.strip(' '))
        for i in range(int(len(sents) / 2)):
            sent = sents[2 * i] + sents[2 * i + 1]
            new_sents.append(sent)
    return new_sents


'''FUNCTIONS RELATED TO LITERATURE WORK EXTRACTION'''
# get the url of literature works with the given base url
def comp_url(num1, num2, prefix, suffix):
    urlcol = []
    for i in range(num1, num2 + 1):
        url = prefix + str(i) + suffix
        urlcol.append(url)
    return urlcol


# get the literature work in which the character encoding is gbk
def get_work_gbk(collection):
    col = []
    try:
        for i, url in enumerate(collection):
            if i % 5 == 0:
                print(str(i) + ' urls have been processed. And the current url is ' + str(url))
            res = urllib.request.Request(url=url, headers=headers)
            rep = urllib.request.urlopen(res).read().decode('gbk', 'ignore')
            text = bf(rep, 'html.parser').find_all('p')
            text = re.sub(r'(</*p>)|(</*br/*>)|(\r)|(\n)|(\[)|(\t)|(<!*-*script-*>)|(<u>一</u><u>哦</u>)','', str(text))
            text = text.replace(r'</p>, <p>', '')
            text = text.replace(u'\xa0', u'')
            text = text.replace(u'\u3000', u'')
            text = text.replace(r'[<td class="content" colspan="3">)', '')
            col.append(text)
    except urllib.error.HTTPError:
        pass
    return col


# get the literature work in which the character encoding is gbk
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


# get the text of Chinese government report
def get_report(url):
    while True:
        try:
            res = urllib.request.Request(url=url, headers=headers)
            rep = urllib.request.urlopen(res).read().decode('utf-8')
            text = bf(rep, 'html.parser').find_all('p')
            text = re.sub(r'(</*p>,*)|(</*strong>)|(\u3000)|(\xa0)', '', str(text))
            text = re.split(r'</*font>*| ', text)
            if urllib.request.urlopen(res).getcode() == 200:
                break
        except Exception as er:
            print(er)
    return cut_sents(text)[4:]


'''FUNCTIONS USED TO BUILD A CORPUS'''

# randomly pick out a specific number of sentences to form the corpus of various time spans.
def build_corpus(text, num1, num2):
    text = cut_sents(text)
    min_dis = 100000
    for i in range(1, len(text)):
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


# save the text and its information
def save_text(docname, dict):
    with open(docname, 'w', encoding='utf-8') as filework:
        for key, value in dict.items():
            filework.write(key + '\t' + str(value) +'\n')


# define a function to add metadata to the extracted sentences
def add_metadata(sentences,information):
    metadata ={}
    for sent in sentences:
        metadata[sent] = information
    return metadata

# calculate the number of characters; the text is a list
def textlen(text):
    num = 0
    for i in range(len(text)):
        num += len(text[i])
    return num

# define a function to calculate the length of corpus without considering the punctuations
def characterlen(text):
    pat = r"\w"
    num = 0
    for i in range(len(text)):
        num += len(re.findall(pat, text[i]))
    return num


'''Collecting the data published between 1950 and 1965'''

# The text from People's Daily
text_ppl_50 = get_text(ppl_base_url, '1950-1-1', '1950-12-31', 5)
text_ppl_51 = get_text(ppl_base_url, '1951-1-1', '1951-12-13', 5)
text_ppl_52 = get_text(ppl_base_url, '1952-1-1', '1952-12-13', 5)
text_ppl_53 = get_text(ppl_base_url, '1953-1-1', '1953-12-13', 5)
text_ppl_54 = get_text(ppl_base_url, '1954-1-1', '1954-12-13', 5)
text_ppl_55 = get_text(ppl_base_url, '1955-1-1', '1955-12-13', 5)
text_ppl_56 = get_text(ppl_base_url, '1956-1-1', '1956-12-13', 5)
text_ppl_57 = get_text(ppl_base_url, '1957-1-1', '1957-12-13', 5)
text_ppl_58 = get_text(ppl_base_url, '1958-1-1', '1958-12-13', 5)
text_ppl_59 = get_text(ppl_base_url, '1959-1-1', '1959-12-13', 5)
text_ppl_60 = get_text(ppl_base_url, '1960-1-1', '1960-12-13', 5)
text_ppl_61 = get_text(ppl_base_url, '1961-1-1', '1961-12-13', 5)
text_ppl_62 = get_text(ppl_base_url, '1962-1-1', '1962-12-13', 5)
text_ppl_63 = get_text(ppl_base_url, '1963-1-1', '1963-12-13', 5)
text_ppl_64 = get_text(ppl_base_url, '1964-1-1', '1964-12-13', 5)
text_ppl_65 = get_text(ppl_base_url, '1965-1-1', '1965-12-13', 5)

# The text from Reference News
text_ref_57 = get_text(ref_base_url, '1957-1-1', '1957-12-31', 10)
text_ref_58 = get_text(ref_base_url, '1958-1-1', '1958-12-31', 10)
text_ref_59 = get_text(ref_base_url, '1959-1-1', '1959-12-31', 10)
text_ref_60 = get_text(ref_base_url, '1960-1-1', '1960-12-31', 10)
text_ref_61 = get_text(ref_base_url, '1961-1-1', '1961-12-31', 10)
text_ref_62 = get_text(ref_base_url, '1962-1-1', '1962-12-31', 10)
text_ref_63 = get_text(ref_base_url, '1963-1-1', '1963-12-31', 10)
text_ref_64 = get_text(ref_base_url, '1964-1-1', '1964-12-31', 10)
text_ref_65 = get_text(ref_base_url, '1965-1-1', '1965-12-31', 10)

# Building the corpus and adding the metadata to each sentence
text_ppl_50 = add_metadata(build_corpus(text_ppl_50, 2340,2540), {'year':'1950', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_51 = add_metadata(build_corpus(text_ppl_51, 2340,2540), {'year':'1951', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_52 = add_metadata(build_corpus(text_ppl_52, 2340,2540), {'year':'1952', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_53 = add_metadata(build_corpus(text_ppl_53, 2340,2540), {'year':'1953', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_54 = add_metadata(build_corpus(text_ppl_54, 2340,2540), {'year':'1954', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_55 = add_metadata(build_corpus(text_ppl_55, 2340,2540), {'year':'1955', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_56 = add_metadata(build_corpus(text_ppl_56, 2340,2540), {'year':'1956', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_57 = add_metadata(build_corpus(text_ppl_57, 2340,2540), {'year':'1957', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_58 = add_metadata(build_corpus(text_ppl_58, 2340,2540), {'year':'1958', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_59 = add_metadata(build_corpus(text_ppl_59, 2340,2540), {'year':'1959', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_60 = add_metadata(build_corpus(text_ppl_60, 2340,2540), {'year':'1960', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_61 = add_metadata(build_corpus(text_ppl_61, 2340,2540), {'year':'1961', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_62 = add_metadata(build_corpus(text_ppl_62, 2340,2540), {'year':'1962', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_63 = add_metadata(build_corpus(text_ppl_63, 2340,2540), {'year':'1963', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_64 = add_metadata(build_corpus(text_ppl_64, 2340,2540), {'year':'1964', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_65 = add_metadata(build_corpus(text_ppl_65, 2340,2540), {'year':'1965', 'genre': 'press reportage', 'name':'People\' Daily'})

# Combine all the sentence extracted from the People's Daily together.
text_ppl_5065 = {**text_ppl_50,**text_ppl_51,**text_ppl_52,**text_ppl_53,**text_ppl_54,**text_ppl_55,**text_ppl_56,**text_ppl_57,**text_ppl_58,**text_ppl_59,
                 **text_ppl_60,**text_ppl_61,**text_ppl_62,**text_ppl_63,**text_ppl_64,**text_ppl_65}


text_ref_57 = add_metadata(build_corpus(text_ref_57, 4200,4400), {'year':'1957', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_58 = add_metadata(build_corpus(text_ref_58, 4200,4400), {'year':'1958', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_59 = add_metadata(build_corpus(text_ref_59, 4200,4400), {'year':'1959', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_60 = add_metadata(build_corpus(text_ref_60, 4200,4400), {'year':'1960', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_61 = add_metadata(build_corpus(text_ref_61, 4200,4400), {'year':'1961', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_62 = add_metadata(build_corpus(text_ref_62, 4200,4400), {'year':'1962', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_63 = add_metadata(build_corpus(text_ref_63, 4200,4400), {'year':'1963', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_64 = add_metadata(build_corpus(text_ref_64, 4200,4400), {'year':'1964', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_65 = add_metadata(build_corpus(text_ref_65, 4200,4400), {'year':'1965', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_5065 = {**text_ref_57,**text_ref_58,**text_ref_59,**text_ref_60,**text_ref_61,**text_ref_62,**text_ref_63,**text_ref_64,**text_ref_65}

# building the corpus with the text extracted from Chinese Government Report
rep_54 = build_corpus(get_report('https://web.archive.org/web/20060911162256/ttp://www.gov.cn/test/2006-02/23/content_208673.htm'),7100, 7300)
rep_55 = build_corpus(get_report('https://web.archive.org/web/20120212032142/http://www.gov.cn/test/2006-02/23/content_208705.htm'), 7100, 7300)
rep_56 = build_corpus(get_report('https://web.archive.org/web/20200922044133/http://www.gov.cn/test/2006-02/23/content_208738.htm'), 7100, 7300)
rep_57 = build_corpus(get_report('https://web.archive.org/web/20200922044217/http://www.gov.cn/test/2006-02/23/content_208756.htm'), 7100, 7300)
rep_59 = build_corpus(get_report('https://web.archive.org/web/20200922044153/http://www.gov.cn/test/2006-02/23/content_208774.htm'), 7100, 7300)
rep_60 = build_corpus(get_report('https://web.archive.org/web/20200922044208/http://www.gov.cn/test/2006-02/27/content_212502.htm'), 7100, 7300)
rep_64 = build_corpus(get_report('https://web.archive.org/web/20210317144514/http://www.gov.cn/test/2006-02/23/content_208787.htm'),7100, 7300)

rep_54 = add_metadata(rep_54, {'time':'1954', 'genre':'others', 'name':'Chinese government\'s report'})
rep_55 = add_metadata(rep_55, {'time':'1955', 'genre':'others', 'name':'Chinese government\'s report'})
rep_56 = add_metadata(rep_56, {'time':'1956', 'genre':'others', 'name':'Chinese government\'s report'})
rep_57 = add_metadata(rep_57, {'time':'1957', 'genre':'others', 'name':'Chinese government\'s report'})
rep_59 = add_metadata(rep_59, {'time':'1959', 'genre':'others', 'name':'Chinese government\'s report'})
rep_60 = add_metadata(rep_60, {'time':'1960', 'genre':'others', 'name':'Chinese government\'s report'})
rep_64 = add_metadata(rep_64, {'time':'1964', 'genre':'others', 'name':'Chinese government\'s report'})

rep_5065 = {**rep_54,**rep_55,**rep_56,**rep_57,**rep_59,**rep_60,**rep_64}


# Extract literature works
'''1950-1965
Fiction
https://www.kunnu.com/chuangyeshi/cys-1/ 创业史 1959
http://www.dushu369.com/zhongguomingzhu/qczg/ 青春之歌 1958

Prose
http://www.dushu369.com/zhongguomingzhu/ysyh/ 燕山夜话 1962
https://www.kanunu8.com/book3/6089/index.html 大山里的人生 沈从文 -1965
https://www.kanunu8.com/book3/7993/ 生活情趣 周作人 -1965

Others
https://www.xstt5.com/mingzhu/1454/ 茶馆 1955
https://www.kanunu8.com/book3/8023/ 老舍自传 -1965
https://www.kanunu8.com/book3/7991/ 文学评论 -1965
Sci-fi
https://www.99csw.com/article/4680.htm From the Earth to the March 1950
https://m.shutxt.com/kh/9338/526940.html 割掉鼻子的大象''' 1957

# 创业史 1959
lit_501 = comp_url(157696, 157748, 'https://www.qiyao5200.com/book/3/3192/', '.html')
# 青春之歌 1958
lit_502 = comp_url(185687, 185716, 'https://www.kanunu8.com/book3/8368/', '.html')
# 周作人 生活情趣 1965
lit_503 = comp_url(174774, 174789, 'https://www.kanunu8.com/book3/7993/', '.html')
# 茶馆 1958
lit_504 = comp_url(79356, 79358, 'https://www.xstt5.com/mingzhu/1454/', '.html')
# 燕山夜话
lit_505 = comp_url(17085, 17160, 'http://www.dushu369.com/zhongguomingzhu/HTML/', '.html')
# 老舍自传
lit_506 = comp_url(175626, 175654, 'https://www.kanunu8.com/book3/8023/', '.html')
# 大山里的人生
lit_507 = comp_url(107559, 107603, 'https://www.kanunu8.com/book3/6089/', '.html')
# 周作人 文学评论
lit_508 = comp_url(174705, 174751, 'https://www.kanunu8.com/book3/7991/', '.html')

# Some literature works are from other websites which have different node tags
# I have to write specific codes to crawl the data

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

# As there are only two available science fiction texts, I copy and paste them to a txt file.
a = open('sci_fi_50', 'r').read()
sci = re.sub(r'(\n)|(\u3000)', '', str(a))
sci_50 = cut_sents([sci])

# add the metadata to the literature sentences
text_501 = add_metadata(build_corpus(litext_501[5:-5], 32500, 32700), {'year':'1959', 'genre': 'literature', 'category':'general fiction', 'name': '创业史' })
text_502 = add_metadata(build_corpus(litext_502[5: -5], 32500, 32700), {'year': '1958', 'genre': 'literature', 'category': 'general fiction', 'name': '青春之歌'})
text_503 = add_metadata(build_corpus(litext_503[5: -5], 12500, 12700), {'year': '1965', 'genre': 'literature', 'category':'prose', 'name':'周作人文集之生活情趣'})
text_504 = add_metadata(build_corpus(litext_504[5: -5], 5200, 5400), {'year': '1958', 'genre':'literature', 'category':'others', 'name':'茶馆'})
text_505 = add_metadata(build_corpus(litext_505[5: -5], 12500, 12700), {'year': '1961', 'genre':'literature', 'category': 'prose', 'name': '燕山夜话'})
text_506 = add_metadata(build_corpus(litext_506[5: -5], 5200, 5400), {'year':'1965', 'genre': 'literature', 'category':'others', 'name':'老舍自传'})
text_507 = add_metadata(build_corpus(litext_507[5: -5], 12500, 12700), {'year':'1965', 'genre': 'literature', 'category': 'prose', 'name':'大山里的人生'})
text_508 = add_metadata(build_corpus(litext_508[5: -5],5200,5400), {'year': '1965', 'genre': 'literature', 'category': 'others', 'name':'周作人文集之文学评论'})
text_509 = add_metadata(build_corpus(sci_50, 2500, 3000), {'year': '1965', 'genre': 'literature', 'category': 'science fiction', 'name':'从地球到火星'})

lit_5065 = {**text_501,**text_502,**text_503,**text_504,**text_505,**text_506,**text_507,**text_508,**text_509,**text_ppl_5065, **text_ref_5065}

# combine each part of the corpus together including
# Poeple's Daily, Reference News, Chinese Government Reports, General fictions, Science/detective fictions, Prose and Others.
corpus_50 = {**text_ppl_5065, **text_ref_5065, **rep_5065, **lit_5065}
save_text('corpus_50_65.txt', corpus_50)
print('The corpus 1950-1965 is built.')

'''Collecting the data published between 1966 and 1976'''
# 1966-1976 People's Daily
text_ppl_66 = get_text(ppl_base_url, '1966-1-1', '1966-12-13', 3)
text_ppl_67 = get_text(ppl_base_url, '1967-1-1', '1967-12-13', 3)
text_ppl_68 = get_text(ppl_base_url, '1968-1-1', '1968-12-13', 3)
text_ppl_69 = get_text(ppl_base_url, '1969-1-1', '1969-12-13', 3)
text_ppl_70 = get_text(ppl_base_url, '1970-1-1', '1970-12-13', 3)
text_ppl_71 = get_text(ppl_base_url, '1971-1-1', '1971-12-13', 3)
text_ppl_72 = get_text(ppl_base_url, '1972-1-1', '1972-12-13', 3)
text_ppl_73 = get_text(ppl_base_url, '1973-1-1', '1973-12-13', 3)
text_ppl_74 = get_text(ppl_base_url, '1974-1-1', '1974-12-13', 3)
text_ppl_75 = get_text(ppl_base_url, '1975-1-1', '1975-12-13', 3)
text_ppl_76 = get_text(ppl_base_url, '1976-1-1', '1976-12-13', 3)

text_ppl_66 = add_metadata(build_corpus(text_ppl_66, 690,890), {'year':'1966', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_67 = add_metadata(build_corpus(text_ppl_67, 690,890), {'year':'1967', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_68 = add_metadata(build_corpus(text_ppl_68, 690,890), {'year':'1968', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_69 = add_metadata(build_corpus(text_ppl_69, 690,890), {'year':'1969', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_70 = add_metadata(build_corpus(text_ppl_70, 690,890), {'year':'1970', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_71 = add_metadata(build_corpus(text_ppl_71, 690,890), {'year':'1971', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_72 = add_metadata(build_corpus(text_ppl_72, 690,890), {'year':'1972', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_73 = add_metadata(build_corpus(text_ppl_73, 690,890), {'year':'1973', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_74 = add_metadata(build_corpus(text_ppl_74, 600,890), {'year':'1974', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_75 = add_metadata(build_corpus(text_ppl_75, 700,1000), {'year':'1975', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_76 = add_metadata(build_corpus(text_ppl_76, 700,1000), {'year':'1976', 'genre': 'press reportage', 'name':'People\' Daily'})

text_ppl_6676 = {**text_ppl_66,**text_ppl_67,**text_ppl_68,**text_ppl_69,**text_ppl_70,**text_ppl_71,**text_ppl_72,**text_ppl_73,
                 **text_ppl_74,**text_ppl_75,**text_ppl_76}

# 1966-1976 Reference News
text_ref_66 = get_text(ref_base_url, '1966-1-1', '1966-12-13', 5)
text_ref_67 = get_text(ref_base_url, '1967-1-1', '1967-12-13', 5)
text_ref_68 = get_text(ref_base_url, '1968-1-1', '1968-12-13', 5)
text_ref_69 = get_text(ref_base_url, '1969-1-1', '1969-12-13', 5)
text_ref_70 = get_text(ref_base_url, '1970-1-1', '1970-12-13', 5)
text_ref_71 = get_text(ref_base_url, '1971-1-1', '1971-12-13', 5)
text_ref_72 = get_text(ref_base_url, '1972-1-1', '1972-12-13', 5)
text_ref_73 = get_text(ref_base_url, '1973-1-1', '1973-12-13', 5)
text_ref_74 = get_text(ref_base_url, '1974-1-1', '1974-12-13', 5)
text_ref_75 = get_text(ref_base_url, '1975-1-1', '1975-12-13', 5)
text_ref_76 = get_text(ref_base_url, '1976-1-1', '1976-12-13', 5)

text_ref_66 = add_metadata(build_corpus(text_ref_66, 690,990), {'year':'1966', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_67 = add_metadata(build_corpus(text_ref_67, 690,990), {'year':'1967', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_68 = add_metadata(build_corpus(text_ref_68, 690,990), {'year':'1968', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_69 = add_metadata(build_corpus(text_ref_69, 690,990), {'year':'1969', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_70 = add_metadata(build_corpus(text_ref_70, 690,990), {'year':'1970', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_71 = add_metadata(build_corpus(text_ref_71, 690,990), {'year':'1971', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_72 = add_metadata(build_corpus(text_ref_72, 690,990), {'year':'1972', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_73 = add_metadata(build_corpus(text_ref_73, 690,990), {'year':'1973', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_74 = add_metadata(build_corpus(text_ref_74, 690,990), {'year':'1974', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_75 = add_metadata(build_corpus(text_ref_75, 690,990), {'year':'1975', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_76 = add_metadata(build_corpus(text_ref_76, 690,990), {'year':'1976', 'genre': 'press reportage', 'name':'Reference News'})

text_ref_6676 ={**text_ref_66,**text_ref_67,**text_ref_68,**text_ref_69,**text_ref_70,**text_ref_71,**text_ref_72,**text_ref_73,**text_ref_74,
                **text_ref_75,**text_ref_76}

# 1966-1976 Chinese Government Report
# (Only one was published during this period of time)
rep_6676 = add_metadata(build_corpus(get_report('https://web.archive.org/web/20210416155911/http://www.gov.cn/test/2006-02/23/content_208796.htm'), 4000, 4100),{'time':'1975', 'genre':'others', 'work':'Chinese government\'s report'})


# Literature works published between 1966 and 1976
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
text_66 = add_metadata(build_corpus(litext_66[5:-5], 30000, 30200), {'time':'1966', 'genre':'literature', 'category':'general fiction'})

corpus_66 = {**text_ppl_6676, **text_ref_6676, **rep_6676, **text_66}
save_text('corpus_66_76.txt',corpus_66)
print('The corpus 1966-1976 is built.')


'''Collecting the data published between 1977 and 1999'''
#  1977-1999 People's Daily
text_ppl_77 = get_text(ppl_base_url, '1977-1-1', '1977-12-13', 7)
text_ppl_78 = get_text(ppl_base_url, '1978-1-1', '1978-12-13', 7)
text_ppl_79 = get_text(ppl_base_url, '1979-1-1', '1979-12-13', 7)
text_ppl_80 = get_text(ppl_base_url, '1980-1-1', '1980-12-13', 7)
text_ppl_81 = get_text(ppl_base_url, '1981-1-1', '1981-12-13', 7)
text_ppl_82 = get_text(ppl_base_url, '1982-1-1', '1982-12-13', 7)
text_ppl_83 = get_text(ppl_base_url, '1983-1-1', '1983-12-13', 7)
text_ppl_84 = get_text(ppl_base_url, '1984-1-1', '1984-12-13', 7)
text_ppl_85 = get_text(ppl_base_url, '1985-1-1', '1985-12-13', 7)
text_ppl_86 = get_text(ppl_base_url, '1986-1-1', '1986-12-13', 7)
text_ppl_87 = get_text(ppl_base_url, '1987-1-1', '1987-12-13', 7)
text_ppl_88 = get_text(ppl_base_url, '1988-1-1', '1988-12-13', 7)
text_ppl_89 = get_text(ppl_base_url, '1989-1-1', '1989-12-13', 7)
text_ppl_90 = get_text(ppl_base_url, '1990-1-1', '1990-12-13', 7)
text_ppl_91 = get_text(ppl_base_url, '1991-1-1', '1991-12-13', 7)
text_ppl_92 = get_text(ppl_base_url, '1992-1-1', '1992-12-13', 7)
text_ppl_93 = get_text(ppl_base_url, '1993-1-1', '1993-12-13', 7)
text_ppl_94 = get_text(ppl_base_url, '1994-1-1', '1994-12-13', 7)
text_ppl_95 = get_text(ppl_base_url, '1995-1-1', '1995-12-13', 7)
text_ppl_96 = get_text(ppl_base_url, '1996-1-1', '1996-12-13', 7)
text_ppl_97 = get_text(ppl_base_url, '1997-1-1', '1997-12-13', 7)
text_ppl_98 = get_text(ppl_base_url, '1998-1-1', '1998-12-13', 7)
text_ppl_99 = get_text(ppl_base_url, '1999-1-1', '1999-12-13', 7)


text_ppl_77 = add_metadata(build_corpus(text_ppl_77, 2280,2480), {'year':'1977', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_78 = add_metadata(build_corpus(text_ppl_78, 2280,2480), {'year':'1978', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_79 = add_metadata(build_corpus(text_ppl_79, 2280,2480), {'year':'1979', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_80 = add_metadata(build_corpus(text_ppl_80, 2280,2480), {'year':'1980', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_81 = add_metadata(build_corpus(text_ppl_81, 2280,2480), {'year':'1981', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_82 = add_metadata(build_corpus(text_ppl_82, 2280,2480), {'year':'1982', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_83 = add_metadata(build_corpus(text_ppl_83, 2280,2480), {'year':'1983', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_84 = add_metadata(build_corpus(text_ppl_84, 2280,2480), {'year':'1984', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_85 = add_metadata(build_corpus(text_ppl_85, 2280,2480), {'year':'1985', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_86 = add_metadata(build_corpus(text_ppl_86, 2280,2480), {'year':'1986', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_87 = add_metadata(build_corpus(text_ppl_87, 2280,2480), {'year':'1987', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_88 = add_metadata(build_corpus(text_ppl_88, 2280,2480), {'year':'1988', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_89 = add_metadata(build_corpus(text_ppl_89, 2280,2480), {'year':'1989', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_90 = add_metadata(build_corpus(text_ppl_90, 2280,2480), {'year':'1990', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_91 = add_metadata(build_corpus(text_ppl_91, 2280,2480), {'year':'1991', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_92 = add_metadata(build_corpus(text_ppl_92, 2280,2580), {'year':'1992', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_93 = add_metadata(build_corpus(text_ppl_93, 2280,2480), {'year':'1993', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_94 = add_metadata(build_corpus(text_ppl_94, 2280,2480), {'year':'1994', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_95 = add_metadata(build_corpus(text_ppl_95, 2280,2480), {'year':'1995', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_96 = add_metadata(build_corpus(text_ppl_96, 2280,2480), {'year':'1996', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_97 = add_metadata(build_corpus(text_ppl_97, 2280,2480), {'year':'1997', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_98 = add_metadata(build_corpus(text_ppl_98, 2280,2480), {'year':'1998', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_99 = add_metadata(build_corpus(text_ppl_99, 2280,2480), {'year':'1999', 'genre': 'press reportage', 'name':'People\' Daily'})

text_ppl_7799 ={**text_ppl_77,**text_ppl_78,**text_ppl_79,**text_ppl_80,**text_ppl_81,**text_ppl_82,**text_ppl_83,**text_ppl_84,**text_ppl_85,**text_ppl_86,
            **text_ppl_87,**text_ppl_88,**text_ppl_89,**text_ppl_90,**text_ppl_91,**text_ppl_92,**text_ppl_93,**text_ppl_94,**text_ppl_95,
            **text_ppl_96,**text_ppl_97,**text_ppl_98,**text_ppl_99}

# 1977-1999 Reference News
text_ref_77 = get_text(ref_base_url, '1977-1-1', '1977-12-13', 7)
text_ref_78 = get_text(ref_base_url, '1978-1-1', '1978-12-13', 7)
text_ref_79 = get_text(ref_base_url, '1979-1-1', '1979-12-13', 7)
text_ref_80 = get_text(ref_base_url, '1980-1-1', '1980-12-13', 7)
text_ref_81 = get_text(ref_base_url, '1981-1-1', '1981-12-13', 7)
text_ref_82 = get_text(ref_base_url, '1982-1-1', '1982-12-13', 7)
text_ref_83 = get_text(ref_base_url, '1983-1-1', '1983-12-13', 7)
text_ref_84 = get_text(ref_base_url, '1984-1-1', '1984-12-13', 7)
text_ref_85 = get_text(ref_base_url, '1985-1-1', '1985-12-13', 7)
text_ref_86 = get_text(ref_base_url, '1986-1-1', '1986-12-13', 7)
text_ref_87 = get_text(ref_base_url, '1987-1-1', '1987-12-13', 7)
text_ref_88 = get_text(ref_base_url, '1988-1-1', '1988-12-13', 7)
text_ref_89 = get_text(ref_base_url, '1989-1-1', '1989-12-13', 7)
text_ref_90 = get_text(ref_base_url, '1990-1-1', '1990-12-13', 7)
text_ref_91 = get_text(ref_base_url, '1991-1-1', '1991-12-13', 7)
text_ref_92 = get_text(ref_base_url, '1992-1-1', '1992-12-13', 7)
text_ref_93 = get_text(ref_base_url, '1993-1-1', '1993-12-13', 7)
text_ref_94 = get_text(ref_base_url, '1994-1-1', '1994-12-13', 7)
text_ref_95 = get_text(ref_base_url, '1995-1-1', '1995-12-13', 7)
text_ref_96 = get_text(ref_base_url, '1996-1-1', '1996-12-13', 7)
text_ref_97 = get_text(ref_base_url, '1997-1-1', '1997-12-13', 7)
text_ref_98 = get_text(ref_base_url, '1998-1-1', '1998-12-13', 7)
text_ref_99 = get_text(ref_base_url, '1999-1-1', '1999-12-13', 7)

# Adding the metadata
text_ref_77 = add_metadata(build_corpus(text_ref_77, 2280,2480), {'year':'1977', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_78 = add_metadata(build_corpus(text_ref_78, 2280,2480), {'year':'1978', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_79 = add_metadata(build_corpus(text_ref_79, 2280,2480), {'year':'1979', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_80 = add_metadata(build_corpus(text_ref_80, 2280,2480), {'year':'1980', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_81 = add_metadata(build_corpus(text_ref_81, 2280,2480), {'year':'1981', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_82 = add_metadata(build_corpus(text_ref_82, 2280,2480), {'year':'1982', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_83 = add_metadata(build_corpus(text_ref_83, 2280,2480), {'year':'1983', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_84 = add_metadata(build_corpus(text_ref_84, 2280,2480), {'year':'1984', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_85 = add_metadata(build_corpus(text_ref_85, 2280,2480), {'year':'1985', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_86 = add_metadata(build_corpus(text_ref_86, 2280,2480), {'year':'1986', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_87 = add_metadata(build_corpus(text_ref_87, 2280,2480), {'year':'1987', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_88 = add_metadata(build_corpus(text_ref_88, 2280,2480), {'year':'1988', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_89 = add_metadata(build_corpus(text_ref_89, 2280,2480), {'year':'1989', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_90 = add_metadata(build_corpus(text_ref_90, 2280,2480), {'year':'1990', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_91 = add_metadata(build_corpus(text_ref_91, 2280,2480), {'year':'1991', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_92 = add_metadata(build_corpus(text_ref_92, 2280,2480), {'year':'1992', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_93 = add_metadata(build_corpus(text_ref_93, 2280,2480), {'year':'1993', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_94 = add_metadata(build_corpus(text_ref_94, 2280,2480), {'year':'1994', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_95 = add_metadata(build_corpus(text_ref_95, 2280,2480), {'year':'1995', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_96 = add_metadata(build_corpus(text_ref_96, 2280,2480), {'year':'1996', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_97 = add_metadata(build_corpus(text_ref_97, 2280,2480), {'year':'1997', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_98 = add_metadata(build_corpus(text_ref_98, 2280,2480), {'year':'1998', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_99 = add_metadata(build_corpus(text_ref_99, 2280,2480), {'year':'1999', 'genre': 'press reportage', 'name':'Reference News'})

text_ref_7799 ={**text_ref_77,**text_ref_78,**text_ref_79,**text_ref_80,**text_ref_81,**text_ref_82,**text_ref_83,**text_ref_84,**text_ref_85,
                **text_ref_86,**text_ref_87,**text_ref_88,**text_ref_89,**text_ref_90,**text_ref_91,**text_ref_92,**text_ref_93,**text_ref_94,
                **text_ref_95,**text_ref_96,**text_ref_97,**text_ref_98,**text_ref_99}


# Scrape the Chinese Government Report published between 1977 and 1999.
rep_78 =build_corpus(get_report('https://web.archive.org/web/20210129024716/http://www.gov.cn/test/2006-02/16/content_200704.htm'), 3200, 3400)
rep_79 =build_corpus(get_report('https://web.archive.org/web/20200922044122/http://www.gov.cn/test/2006-02/16/content_200759.htm'), 3200, 3400)
rep_80 =build_corpus(get_report('https://web.archive.org/web/20210117002310/http://www.gov.cn/test/2006-02/16/content_200778.htm'), 3200, 3400)
rep_81 =build_corpus(get_report('https://web.archive.org/web/20200922044128/http://www.gov.cn/test/2006-02/16/content_200802.htm'), 3200, 3400)
rep_82 =build_corpus(get_report('https://web.archive.org/web/20200922044102/http://www.gov.cn/test/2006-02/23/content_208652.htm'), 3200, 3400)
rep_83 =build_corpus(get_report('https://web.archive.org/web/20210117010057/http://www.gov.cn/test/2006-02/16/content_200823.htm'), 3200, 3400)
rep_84 =build_corpus(get_report('https://web.archive.org/web/20200922044115/http://www.gov.cn/test/2006-02/16/content_200834.htm'), 3200, 3400)
rep_85 =build_corpus(get_report('https://web.archive.org/web/20210116235930/http://www.gov.cn/test/2006-02/16/content_200841.htm'), 3200, 3400)
rep_86 =build_corpus(get_report('https://web.archive.org/web/20200922044107/http://www.gov.cn/test/2006-02/16/content_200850.htm'), 3200, 3400)
rep_87 =build_corpus(get_report('https://web.archive.org/web/20200922044112/http://www.gov.cn/test/2006-02/16/content_200857.htm'), 3200, 3400)
rep_88 =build_corpus(get_report('https://web.archive.org/web/20200922044220/http://www.gov.cn/test/2006-02/16/content_200865.htm'), 3200, 3400)
rep_89 =build_corpus(get_report('https://web.archive.org/web/20210117002844/http://www.gov.cn/test/2006-02/16/content_200875.htm'), 3200, 3400)
rep_90 =build_corpus(get_report('https://web.archive.org/web/20200316080428/http://www.gov.cn/test/2006-02/16/content_200883.htm'), 3200, 3400)
rep_91 =build_corpus(get_report('https://web.archive.org/web/20210118234443/http://www.gov.cn/test/2006-02/16/content_200903.htm'), 3200, 3400)
rep_92 =build_corpus(get_report('https://web.archive.org/web/20200922044111/http://www.gov.cn/test/2006-02/16/content_200922.htm'), 3200, 3400)
rep_93 =build_corpus(get_report('https://web.archive.org/web/20210116235411/http://www.gov.cn/test/2006-02/16/content_200926.htm'), 3200, 3400)
rep_94 =build_corpus(get_report('https://web.archive.org/web/20210116233334/http://www.gov.cn/test/2006-02/16/content_201101.htm'), 3200, 3400)
rep_95 =build_corpus(get_report('https://web.archive.org/web/20120308021105/http://www.gov.cn/test/2006-02/16/content_201109.htm'), 3200, 3400)
rep_96 =build_corpus(get_report('https://web.archive.org/web/20210120163700/http://www.gov.cn/test/2006-02/16/content_201115.htm'), 3200, 3400)
rep_97 =build_corpus(get_report('https://web.archive.org/web/20210117003002/http://www.gov.cn/test/2006-02/16/content_201124.htm'), 3200, 3400)
rep_98 =build_corpus(get_report('https://web.archive.org/web/20210118235611/http://www.gov.cn/test/2006-02/16/content_201129.htm'), 3200, 3400)
rep_99 =build_corpus(get_report('https://web.archive.org/web/20210118230302/http://www.gov.cn/test/2006-02/16/content_201143.htm'), 3200, 3400)

rep_78 =add_metadata(rep_78, {'time':'1978', 'genre':'others', 'name':'Chinese government\'s report'})
rep_79 =add_metadata(rep_79, {'time':'1979', 'genre':'others', 'name':'Chinese government\'s report'})
rep_80 =add_metadata(rep_80, {'time':'1980', 'genre':'others', 'name':'Chinese government\'s report'})
rep_81 =add_metadata(rep_81, {'time':'1981', 'genre':'others', 'name':'Chinese government\'s report'})
rep_82 =add_metadata(rep_82, {'time':'1982', 'genre':'others', 'name':'Chinese government\'s report'})
rep_83 =add_metadata(rep_83, {'time':'1983', 'genre':'others', 'name':'Chinese government\'s report'})
rep_84 =add_metadata(rep_84, {'time':'1984', 'genre':'others', 'name':'Chinese government\'s report'})
rep_85 =add_metadata(rep_85, {'time':'1985', 'genre':'others', 'name':'Chinese government\'s report'})
rep_86 =add_metadata(rep_86, {'time':'1986', 'genre':'others', 'name':'Chinese government\'s report'})
rep_87 =add_metadata(rep_87, {'time':'1987', 'genre':'others', 'name':'Chinese government\'s report'})
rep_88 =add_metadata(rep_88, {'time':'1988', 'genre':'others', 'name':'Chinese government\'s report'})
rep_89 =add_metadata(rep_89, {'time':'1989', 'genre':'others', 'name':'Chinese government\'s report'})
rep_90 =add_metadata(rep_90, {'time':'1990', 'genre':'others', 'name':'Chinese government\'s report'})
rep_91 =add_metadata(rep_91, {'time':'1991', 'genre':'others', 'name':'Chinese government\'s report'})
rep_92 =add_metadata(rep_92, {'time':'1992', 'genre':'others', 'name':'Chinese government\'s report'})
rep_93 =add_metadata(rep_93, {'time':'1993', 'genre':'others', 'name':'Chinese government\'s report'})
rep_94 =add_metadata(rep_94, {'time':'1994', 'genre':'others', 'name':'Chinese government\'s report'})
rep_95 =add_metadata(rep_95, {'time':'1995', 'genre':'others', 'name':'Chinese government\'s report'})
rep_96 =add_metadata(rep_96, {'time':'1996', 'genre':'others', 'name':'Chinese government\'s report'})
rep_97 =add_metadata(rep_97, {'time':'1997', 'genre':'others', 'name':'Chinese government\'s report'})
rep_98 =add_metadata(rep_98, {'time':'1998', 'genre':'others', 'name':'Chinese government\'s report'})
rep_99 =add_metadata(rep_99, {'time':'1999', 'genre':'others', 'name':'Chinese government\'s report'})

# Combine the Chinese Government reports together
rep_7799 = {**rep_78,**rep_79,**rep_80,**rep_81,**rep_82,**rep_83,**rep_84,**rep_85,**rep_86,**rep_87,**rep_88,
            **rep_89,**rep_90,**rep_91,**rep_92,**rep_93,**rep_94,**rep_95,**rep_96,**rep_97,**rep_98,**rep_99}



'''1978-1999
Fiction
https://www.99csw.com/book/2683/index.htm 人到中年 1990
https://www.99csw.com/book/2603/index.htm 爸爸爸 1985
https://www.99csw.com/book/1083/index.htm 绿化树 1984
https://www.99csw.com/book/2426/index.htm 许三观卖血记 1995
https://www.kanunu8.com/book4/8929/ 洗澡 1988
https://www.kanunu8.com/book/3980/index.html 永远有多远 1999
https://www.kanunu8.com/book3/8255/ 丰乳肥臀 1996

Prose
http://www.dushu369.com/zhongguomingzhu/suixianglu/ 随想录 巴金 1980-1986
https://www.xstt5.com/mingzhu/1233/ 文化苦旅 1992
https://www.kanunu8.com/files/chinese/201104/2611/62666.html 贾平凹散文集 1980s
Others
https://www.xstt5.com/renwen/3459/ 李泽厚 美的历程 1981
https://www.kanunu8.com/book3/7056/ 他们的世界——中国男同性恋群落透视 1992
https://www.kanunu8.com/book4/8746/ 邓小平政治评传 1995

Science and Detective Fiction
http://www.txshuku.la/mulu/45973.html 霍桑探案 1997
https://www.kanunu8.com/book3/6483/index.html 飞向人马座 1978
http://www.dushu369.com/tonghua/xltmywl/ 小灵通漫游未来 1978
https://www.kanunu8.com/book3/6476/index.html 潘海天 克隆之城 1996'''


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
# 人到中年 1990
lit7801 = comp_url(22231, 22251, 'https://www.xstt5.com/dangdai/796/', '.html')
litext_7801 = cut_sents(get_work_xstt(lit7801))

# 爸爸爸 1985
lit7802 = comp_url(301935, 301942, 'https://m.ksw8888.com/zuojia/hanshaogong/bababa/', '.html')
litext_7802 = cut_sents(get_work_gbk(lit7802))

# 绿化树 1984
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

# 许三观卖血记 1995
lit7804 = comp_url(159246, 159274, 'https://www.kanunu8.com/book3/7196/', '.html')
litext_7804 = cut_sents(get_work_gbk(lit7804))

# 随想录 1980-1986
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

#文化苦旅 1992
lit7806 = comp_url(36650, 36686, 'https://www.xstt5.com/mingzhu/1233/', '.html')
litext_7806 = cut_sents(get_work_xstt(lit7806))

# 美的历程 1981
lit7807 = comp_url(221302, 221311, 'https://www.xstt5.com/renwen/3459/', '.html')
litext_7807 = cut_sents(get_work_xstt(lit7807))[5:]

# 小灵通漫游未来 1978
lit_7808 = comp_url(115522,115533 , 'https://www.kanunu8.com/book3/6484/', '.html')
litext_7808 = cut_sents(get_work_gbk(lit_7808))

#飞向人马座 1978
lit_7809 = comp_url(115497, 115520, 'https://www.kanunu8.com/book3/6483/', '.html')
litext_7809 = cut_sents(get_work_gbk(lit_7809))

# 洗澡 1988
lit_7810 = comp_url(197722, 197733, 'https://www.kanunu8.com/book4/8929/', '.html')
litext_7810 = cut_sents(get_work_gbk(lit_7810))

# 他们的世界——中国男同性恋群落透视 1992
lit_7811 = comp_url(147727, 147749, 'https://www.kanunu8.com/book3/7056/', '.html')
litext_7811 = cut_sents(get_work_gbk(lit_7811))

# 邓小平政治评传 1995
lit_7812 = comp_url(194321, 194329, 'https://www.kanunu8.com/book4/8746/', '.html')
litext_7812 = cut_sents(get_work_gbk(lit_7812))

# 永远有多远 1999
lit_7813 = comp_url(42768, 42774, 'https://www.kanunu8.com/book/3980/', '.html')
litext_7813 = cut_sents(get_work_gbk(lit_7813))

# 丰乳肥臀 1996
lit_7814 = comp_url(182597, 182632, 'https://www.kanunu8.com/book3/8255/', '.html')
litext_7814 = cut_sents(get_work_gbk(lit_7814))

# 贾平凹散文 1980s
lit_7815 = comp_url(62666, 62706, 'https://www.kanunu8.com/files/chinese/201104/2611/', '.html')
litext_7815 = cut_sents(get_work_gbk(lit_7815))

# 克隆之城 1996
lit_7816 = comp_url(115486, 115491, 'https://www.kanunu8.com/book3/6476/', '.html')
litext_7816 = cut_sents(get_work_gbk(lit_7816))

# 霍桑探案 1997
litext_7817=[]
url_all=comp_url(2542396,2542411, 'http://www.txshuku.la/html/45973_','.html')
for url1 in url_all:
    res1 = urllib.request.Request(url=url1, headers=headers)
    rep1 = urllib.request.urlopen(res1).read().decode('gbk', 'ignore')
    text1 = bf(rep1, 'html.parser').find_all(class_='contentbox')
    text1 = re.sub(r'(</*p>)|(</*br/*>)|(\r)|(\n)|(\[)|(\t)|</div>','', str(text1))
    text1 = text1.replace(r'<div class="contentbox" id="htmlContent">', '')
    text1 = text1.replace(u'\xa0', u'')
    text1 = text1.replace(u'\u3000', u'')
    litext_7817.append(text1)
litext_7817 = cut_sents(litext_7817)

text_7801 = build_corpus(litext_7801, 12500, 12700)
text_7802 = build_corpus(litext_7802, 12500, 12700)
text_7803 = build_corpus(litext_7803, 12500, 12700)
text_7804 = build_corpus(litext_7804, 12500, 12700)
text_7805 = build_corpus(litext_7805, 17500, 17700)
text_7806 = build_corpus(litext_7806, 17500, 17700)
text_7807 = build_corpus(litext_7807, 4200, 4400)
text_7808 = build_corpus(litext_7808, 4400, 4600)
text_7809 = build_corpus(litext_7809, 4400, 4600)
text_7810 = build_corpus(litext_7810, 12500, 12800)
text_7811 = build_corpus(litext_7811, 4000, 4200)
text_7812 = build_corpus(litext_7812, 8700, 8900)
text_7813 = build_corpus(litext_7813, 12500, 12700)
text_7814 = build_corpus(litext_7814, 12500, 12700)
text_7815 = build_corpus(litext_7815, 17500, 17700)
text_7816 = build_corpus(litext_7816, 4400, 4600)
text_7817 = build_corpus(litext_7817, 8800, 9000)

text_7801 = add_metadata(text_7801, {'time':'1990', 'genre':'literature', 'category':'general fiction', 'name':'人到中年'})
text_7802 = add_metadata(text_7802, {'time':'1985', 'genre':'literature', 'category':'general fiction', 'name':'爸爸爸'})
text_7803 = add_metadata(text_7803, {'time':'1984', 'genre':'literature', 'category':'general fiction', 'name':'绿化树'})
text_7804 = add_metadata(text_7804, {'time':'1995', 'genre':'literature', 'category':'general fiction', 'name':'许三观卖血记'})
text_7805 = add_metadata(text_7805, {'time':'1992', 'genre':'literature', 'category':'prose', 'name':'文化苦旅'})
text_7807 = add_metadata(text_7807, {'time':'1981', 'genre':'others', 'name':'美的历程'})
text_7806 = add_metadata(text_7806, {'time':'1986', 'genre':'literature', 'category':'prose', 'name':'随想录'})
text_7808 = add_metadata(text_7808, {'time':'1978', 'genre':'literature', 'category':'science fiction', 'name':'小灵通漫游未来'})
text_7809 = add_metadata(text_7809, {'time':'1978', 'genre':'literature', 'category':'science fiction', 'name':'飞向人马座'})
text_7810 = add_metadata(text_7810, {'time':'1988', 'genre':'literature', 'category':'general fiction', 'name':'洗澡'})
text_7811 = add_metadata(text_7811, {'time':'1992', 'genre':'others', 'name':'他们的世界——中国男同性恋群落透视'})
text_7812 = add_metadata(text_7812, {'time':'1995', 'genre':'literature', 'category':'others', 'name':'邓小平政治评传'})
text_7813 = add_metadata(text_7813, {'time':'1999', 'genre':'literature', 'category':'general fiction', 'name':'永远有多远'})
text_7814 = add_metadata(text_7814, {'time':'1996', 'genre':'literature', 'category':'general fiction', 'name':'丰乳肥臀'})
text_7815 = add_metadata(text_7815, {'time':'1999', 'genre':'literature', 'category':'prose', 'name':'朋友'})
text_7816 = add_metadata(text_7816, {'time':'1996', 'genre':'literature', 'category':'science fiction', 'name':'克隆之城'})
text_7817 = add_metadata(text_7817, {'time':'1997', 'genre':'literature', 'category':'detective fiction', 'name':'霍桑探案'})

corpus_78 = {**text_ppl_7799, **text_ref_7799, **rep_7799, **text_7801,**text_7802, **text_7803, **text_7804, **text_7805, **text_7806,
**text_7807, **text_7808, **text_7809, **text_7810, **text_7811, **text_7812, **text_7813, **text_7814, **text_7815, **text_7816, **text_7817}
save_text( 'corpus_78_99.txt',corpus_78)

print('The corpus 1978-1999 is built.')


'''Extracting the data published between 2000 and 2010'''

# 2000-2010 People's Daily
text_ppl_00 = get_text(ppl_base_url, '2000-1-1', '2000-12-13', 20)
text_ppl_01 = get_text(ppl_base_url, '2001-1-1', '2001-12-13', 20)
text_ppl_02 = get_text(ppl_base_url, '2002-1-1', '2002-12-13', 20)
text_ppl_03 = get_text(ppl_base_url, '2003-1-1', '2003-12-13', 20)

# Adding the metadata
text_ppl_00 = add_metadata(build_corpus(text_ppl_00, 13200,13400), {'year':'2000', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_01 = add_metadata(build_corpus(text_ppl_01, 13200,13400), {'year':'2001', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_02 = add_metadata(build_corpus(text_ppl_02, 13200,13400), {'year':'2002', 'genre': 'press reportage', 'name':'People\' Daily'})
text_ppl_03 = add_metadata(build_corpus(text_ppl_03, 13200,13400), {'year':'2003', 'genre': 'press reportage', 'name':'People\' Daily'})

text_ppl_0010 = {**text_ppl_00,**text_ppl_01,**text_ppl_02,**text_ppl_03}

# 2000-2010 Reference News
text_ref_00 = get_text(ref_base_url, '2000-1-1', '2000-12-13', 40)
text_ref_01 = get_text(ref_base_url, '2001-1-1', '2001-12-13', 40)
text_ref_02 = get_text(ref_base_url, '2002-1-1', '2002-12-13', 40)
# Adding the metadata
text_ref_00 = add_metadata(build_corpus(text_ref_00, 17500,17700), {'year':'2000', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_01 = add_metadata(build_corpus(text_ref_01, 17500,17700), {'year':'2001', 'genre': 'press reportage', 'name':'Reference News'})
text_ref_02 = add_metadata(build_corpus(text_ref_02, 17500,27700), {'year':'2002', 'genre': 'press reportage', 'name':'Reference News'})

text_ref_0010 = {**text_ref_00,**text_ref_01, **text_ref_02}

# 2000-2010 Chinese Government Report
rep_00 = build_corpus(get_report('https://web.archive.org/web/20210117004919/http://www.gov.cn/test/2006-02/16/content_201153.htm'), 5000, 5200)
rep_01 = build_corpus(get_report('https://web.archive.org/web/20200922044215/http://www.gov.cn/test/2006-02/16/content_201157.htm'), 5000, 5200)
rep_02 = build_corpus(get_report('https://web.archive.org/web/20200922044057/http://www.gov.cn/test/2006-02/16/content_201164.htm'), 5000, 5200)
rep_03 = build_corpus(get_report('https://web.archive.org/web/20200922044129/http://www.gov.cn/test/2006-02/16/content_201173.htm'), 5000, 5200)
rep_04 = build_corpus(get_report('https://web.archive.org/web/20210117002818/http://www.gov.cn/test/2006-02/16/content_201193.htm'), 5000, 5200)
rep_05 = build_corpus(get_report('https://web.archive.org/web/20200922044115/http://www.gov.cn/test/2006-02/16/content_201218.htm'), 5000, 5200)

# In some links, the report is put in different pages
# I define another function to crawl the data

def build_rep(web1,web2):
    rep=[]
    url = comp_url(2,4, web1, '.htm')
    url.append(web2)
    for x in url:
        rep.append(get_report(x))
        rep1 = [sent for sublist in rep for sent in sublist]
    rep2 = build_corpus(rep1,5000, 5200)
    return rep2
rep_06 = build_rep('https://web.archive.org/web/20200922044213/http://www.gov.cn/test/2009-03/16/content_1260216_',
                   'https://web.archive.org/web/20200922044213/http://www.gov.cn/test/2009-03/16/content_1260216.htm')


rep_07 = build_rep('https://web.archive.org/web/20200407112505/http://www.gov.cn/test/2009-03/16/content_1260216_',
                   'https://web.archive.org/web/20200407112505/http://www.gov.cn/test/2009-03/16/content_1260216.htm')


rep_08 =build_rep('https://web.archive.org/web/20210116230325/http://www.gov.cn/test/2009-03/16/content_1260198_',
         'https://web.archive.org/web/20210116230325/http://www.gov.cn/test/2009-03/16/content_1260198.htm')


rep_09 = build_rep('https://web.archive.org/web/20210119000035/http://www.gov.cn/test/2009-03/16/content_1260221_',
                   'https://web.archive.org/web/20210119000035/http://www.gov.cn/test/2009-03/16/content_1260221.htm')

rep_10 = build_corpus(get_report('https://web.archive.org/web/20201127141328/http://www.gov.cn/2010lh/content_1555767.htm'), 5000, 5200)

rep_00 =add_metadata(rep_00, {'time':'2000', 'genre':'others', 'name':'Chinese government\'s report'})
rep_01 =add_metadata(rep_01, {'time':'2001', 'genre':'others', 'name':'Chinese government\'s report'})
rep_02 =add_metadata(rep_02, {'time':'2002', 'genre':'others', 'name':'Chinese government\'s report'})
rep_03 =add_metadata(rep_03, {'time':'2003', 'genre':'others', 'name':'Chinese government\'s report'})
rep_04 =add_metadata(rep_04, {'time':'2004', 'genre':'others', 'name':'Chinese government\'s report'})
rep_05 =add_metadata(rep_05, {'time':'2005', 'genre':'others', 'name':'Chinese government\'s report'})
rep_06 =add_metadata(rep_06, {'time':'2006', 'genre':'others', 'name':'Chinese government\'s report'})
rep_07 =add_metadata(rep_07, {'time':'2007', 'genre':'others', 'name':'Chinese government\'s report'})
rep_08 =add_metadata(rep_08, {'time':'2008', 'genre':'others', 'name':'Chinese government\'s report'})
rep_09 =add_metadata(rep_09, {'time':'2009', 'genre':'others', 'name':'Chinese government\'s report'})
rep_10 =add_metadata(rep_10, {'time':'2010', 'genre':'others', 'name':'Chinese government\'s report'})

rep_0010 ={**rep_00,**rep_01,**rep_02,**rep_03,**rep_04,**rep_05,**rep_06,**rep_07,**rep_08,**rep_09,**rep_10,}


# Literature and others 2000-2010
'''
1999-2010
fiction:
https://www.kanunu8.com/book3/7437/ 夏至未至 2005
https://www.kanunu8.com/book4/8852/ 最美的时光 2009
http://www.dushu369.com/zhongguomingzhu/yjdywj/ 一句顶一万句 2009
https://www.kanunu8.com/book3/8459/ 河岸 2009
https://www.kanunu8.com/book4/10514/ 鬼吹灯 2007
https://www.kanunu8.com/files/chinese/201103/1976/ 小姨多鹤 2008

prose:
https://www.kanunu8.com/book/3937/index.html 往事并不如烟 2004
http://www.dushu369.com/shici/sanwen/bsmswj/ 毕淑敏散文 2006
https://www.kanunu8.com/book/4389/index.html 被窝是青春的坟墓 七堇年 2007
others:
https://www.kanunu8.com/book3/7576/ 周国平 偶尔远行 2010
https://www.danseshu.com/books/8814 中国农民调查 2003
https://www.kanunu8.com/book3/8112/ 刘心武揭秘红楼梦 2005
https://www.kanunu8.com/files/world/201102/1596.html 世界是平的，21世纪简史 2010
science and detective fiction:
https://www.kanunu8.com/tuili/10502/ 红色高跟鞋 2006
https://www.kanunu8.com/book3/6640/ 乡村教师 2001
https://www.kanunu8.com/book3/6639/index.html 流浪地球 2000
https://www.kanunu8.com/book3/6623/index.html 泡泡 2007'''

# 夏至未至 2005
lit_0001 = comp_url(163020, 163044, 'https://www.kanunu8.com/book3/7437/', '.html')
litext_0001 = cut_sents(get_work_gbk(lit_0001))

# 回延津记 2009
lit_0002 = comp_url(86612, 86635, 'http://www.dushu369.com/zhongguomingzhu/HTML/', '.html')
litext_0002 = cut_sents(get_work_gbk(lit_0002))

# 河岸 2009
lit_0003 = comp_url(188052, 188065, 'https://www.kanunu8.com/book3/8459/', '.html')
litext_0003 = cut_sents(get_work_gbk(lit_0003))

# 往事并不如烟 2004
lit_0004 = comp_url(41650, 41659, 'https://www.kanunu8.com/book/3937/', '.html')
litext_0004 = cut_sents(get_work_gbk(lit_0004))

# 毕淑敏散文集 2006
lit_0005 = comp_url(99802, 99856, 'http://www.dushu369.com/shici/HTML/', '.html')
litext_005 = []
for i, url in enumerate(lit_0005):
    if i % 5 == 0:
        print(str(i) + ' urls have been processed.')
    res7 = urllib.request.Request(url=url, headers=headers)
    rep7 = urllib.request.urlopen(res7).read().decode('gbk', 'ignore')
    text7 = bf(rep7, 'html.parser').find_all('p')
    text7 = re.sub(r'(</*p>)|(<br/*>)', '', str(text7))
    litext_005.append(text7)
litext_0005 = cut_sents(litext_005)

#鬼吹灯 2007
lit_0006 = comp_url(182730,184635, 'https://www.kanunu8.com/book4/10514/', '.html')
litext_0006 = cut_sents(get_work_gbk(lit_0006))

# 红色高跟鞋 2006
lit_0007 = comp_url(183122, 183129, 'https://www.kanunu8.com/tuili/10502/', '.html')
litext_0007 = cut_sents(get_work_gbk(lit_0007))

# 乡村教师 2001
lit_0008 = comp_url(116118, 116125, 'https://www.kanunu8.com/book3/6640/', '.html')
litext_0008 = cut_sents(get_work_gbk(lit_0008))

# 泡泡 2007
lit_0009 = comp_url(115827, 115831, 'https://www.kanunu8.com/book3/6623/', '.html')
litext_0009 = cut_sents(get_work_gbk(lit_0009))

# 刘心武揭秘红楼梦 2005
lit_0010 = comp_url(199422, 199437, 'https://www.kanunu8.com/book4/8914/', '.html')
litext_0010 = cut_sents(get_work_gbk(lit_0010))
# 流浪地球 2000
lit_0011 = comp_url(116113, 116116, 'https://www.kanunu8.com/book3/6639/', '.html')
litext_0011 = cut_sents(get_work_gbk(lit_0011))
# 21世纪简史 2010
lit_0012 = comp_url(37358, 37374, 'https://www.kanunu8.com/files/world/201102/1596/', '.html')
litext_0012 = cut_sents(get_work_gbk(lit_0012))
# 被窝是青春的坟墓 2007
lit_0013 = comp_url(54420, 54455, 'https://www.kanunu8.com/book/4389/', '.html')
litext_0013 = cut_sents(get_work_gbk(lit_0013))

# 小姨多鹤 2008
lit_0014 = comp_url(45910, 45926, 'https://www.kanunu8.com/files/chinese/201103/1976/', '.html')
litext_0014 = cut_sents(get_work_gbk(lit_0014))
# 最美的时光 2009
lit_0015 = comp_url(195534, 195541, 'https://www.kanunu8.com/book4/8852/', '.html')
litext_0015 = cut_sents(get_work_gbk(lit_0015))

# 偶尔远行 2010
lit_0016 = comp_url(166335,166423,'https://www.kanunu8.com/book3/7576/','.html')
litext_0016 = cut_sents(get_work_gbk(lit_0016))

text_0001 = build_corpus(litext_0001, 14600, 14800)
text_0002 = build_corpus(litext_0002, 14600, 14800)
text_0003 = build_corpus(litext_0003, 14600, 14800)
text_0004 = build_corpus(litext_0004, 17500, 17800)
text_0005 = build_corpus(litext_0005, 17500, 17800)
text_0006 = build_corpus(litext_0006, 14600, 14800)
text_0007 = build_corpus(litext_0007, 4400, 4600)
text_0008 = build_corpus(litext_0008, 4400, 4600)
text_0009 = build_corpus(litext_0009, 4400, 4600)
text_0010 = build_corpus(litext_0010, 6500, 6700)
text_0011 = build_corpus(litext_0011, 4400, 4600)
text_0012 = build_corpus(litext_0012, 6500, 6700)
text_0013 = build_corpus(litext_0013, 17300, 17500)
text_0014 = build_corpus(litext_0014, 15500, 15700)
text_0015 = build_corpus(litext_0015, 14500, 14700)
text_0016 = build_corpus(litext_0016, 17500, 17700)
text_0001 = add_metadata(text_0001, {'time': '2005', 'genre':'literature', 'category':'general fiction', 'name':'1995-2005夏至未至'})
text_0002 = add_metadata(text_0002, {'time': '2009', 'genre':'literature', 'category':'general fiction', 'name':'回延津记'})
text_0003 = add_metadata(text_0003, {'time': '2009', 'genre':'literature', 'category':'general fiction', 'name':'河岸'})
text_0004 = add_metadata(text_0004, {'time': '2004', 'genre':'literature', 'category':'prose', 'name':'往事并不如烟'})
text_0005 = add_metadata(text_0005, {'time': '2010', 'genre':'literature', 'category':'prose', 'name':'毕淑敏散文集'})
text_0006 = add_metadata(text_0006, {'time': '2007', 'genre':'literature', 'category':'general fiction', 'name':'鬼吹灯'})
text_0007 = add_metadata(text_0007, {'time': '2006', 'genre':'literature', 'category':'detective fiction', 'name':'红色高跟鞋'})
text_0008 = add_metadata(text_0008, {'time': '2001', 'genre':'literature', 'category':'science fiction', 'name':'乡村教师'})
text_0009 = add_metadata(text_0009, {'time': '2007', 'genre':'literature', 'category':'general fiction', 'name':'泡泡'})
text_0010 = add_metadata(text_0010, {'time': '2005', 'genre':'others', 'name':'刘心武揭秘红楼梦'})
text_0011 = add_metadata(text_0011, {'time': '2000', 'genre':'literature', 'category':'science fiction', 'name':'流浪地球'})
text_0012 = add_metadata(text_0012, {'time': '2010', 'genre':'others', 'name':'世界是平的：21世纪简史'})
text_0013 = add_metadata(text_0013, {'time': '2007', 'genre':'literature', 'category':'prose', 'name':'被窝是青春的坟墓'})
text_0014 = add_metadata(text_0014, {'time': '2008', 'genre':'literature', 'category':'general fiction', 'name':'小姨多鹤'})
text_0015 = add_metadata(text_0015, {'time': '2009', 'genre':'literature', 'category':'general fiction', 'name':'最美的时光'})
text_0016 = add_metadata(text_0016, {'time': '2009', 'genre':'literature', 'category':'prose', 'name':'偶尔远行'})


corpus_00 = {**text_ppl_0010, **text_ref_0010, **rep_0010, **text_0001,**text_0002,**text_0003,**text_0004,**text_0005,**text_0006,
             **text_0007,**text_0008,**text_0009,**text_0010,**text_0011,**text_0012,**text_0013,**text_0014,**text_0015,**text_0016}
save_text('corpus_00_10.txt',corpus_00)



'''
Similalry, this function is to guarantee the sample corpus
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

# Building a sample corpus

sample_corpus_50 = build_sample_corpus(corpus_50.keys(), 1200, 1300)
sample_corpus_66 = build_sample_corpus(corpus_66.keys(), 250, 450)
sample_corpus_78 = build_sample_corpus(corpus_78.keys(), 1730, 1830)
sample_corpus_00 = build_sample_corpus(corpus_00.keys(), 1750, 1850)
sample_corpus = sample_corpus_00 + sample_corpus_78 + sample_corpus_66 + sample_corpus_50

# Save it in a txt file
f = open('sample_corpus.txt', 'w', encoding='utf-8')
for sent in sample_corpus:
    f.write(sent)
f.close()


'''Have an overview of the size of the sample corpus'''
print('There are ' + str(textlen(sample_corpus)) +
      ' characters in the sample corpus (including punctuation characters).')
print('There are ' + str(characterlen(sample_corpus)) +
      ' characters in the sample (without punctuation characters).')



# print the basic data of the corpus
print('There are ', str(textlen(get_corp('corpus_50_65.txt'))), ' charachters including the punctuation markers in the corpus 1950-1965.')
print('There are ', str(textlen(get_corp('corpus_66_76.txt'))), ' charachters including the punctuation markers in the corpus 1966-1976.')
print('There are ', str(textlen(get_corp('corpus_78_99.txt'))), ' charachters including the punctuation markers in the corpus 1977-1999.')
print('There are ', str(textlen(get_corp('corpus_00_10.txt'))), ' charachters including the punctuation markers in the corpus 2000-2010.')
print('There are ', str(textlen(get_corp('corpus_50_65.txt'))+textlen(get_corp('corpus_66_76.txt')) +
                        textlen(get_corp('corpus_78_99.txt')) + textlen(get_corp('corpus_00_10.txt'))), ' charachters including the punctuation markers in the whole corpus.')


print('There are ', str(characterlen(get_corp('corpus_50_65.txt'))), ' charachters without the punctuation markers in the corpus 1950-1965.')
print('There are ', str(characterlen(get_corp('corpus_66_76.txt'))), ' charachters without the punctuation markers in the corpus 1966-1976.')
print('There are ', str(characterlen(get_corp('corpus_78_99.txt'))), ' charachters without the punctuation markers in the corpus 1977-1999.')
print('There are ', str(characterlen(get_corp('corpus_00_10.txt'))), ' charachters without the punctuation markers in the corpus 2000-2010.')
print('There are ', str(characterlen(get_corp('corpus_50_65.txt'))+characterlen(get_corp('corpus_66_76.txt')) +
                        characterlen(get_corp('corpus_78_99.txt')) + characterlen(get_corp('corpus_00_10.txt'))), ' charachters without the punctuation markers in the whole corpus.')


