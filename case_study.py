from ddparser import DDParser
from main import cut_sent, build_conllx, characterlen, count_type

ddp = DDParser(use_pos=True)
# count the frequency of a specific deprel term
def count_rel(text, head, info):
    count = 0
    for i, sentence in enumerate(text):
        if i%1000 == 0:
            print(str(i) + ' sentences have been processed.')
        if sentence[head].count(info) > 0:
            count+= sentence[head].count(info)
    return format(count/len(text), '.2f')

print('Begin reading the treebank.')
treebank_1950 = open('corpus_50_65.txt', 'r', encoding = 'utf-8').read()
print('a')
sents_1950 = cut_sent(treebank_1950)
print('b')
data_1950 = ddp.parse(sents_1950)
print('Finish reading the treebank_1950.')

treebank_1966 = open('corpus_66_76.txt', 'r', encoding = 'utf-8').read()
sents_1966 = cut_sent(treebank_1966)
data_1966 = ddp.parse(sents_1966)
print('Finish reading the treebank_1966.')

treebank_1978 = open('corpus_78_99.txt', 'r', encoding = 'utf-8').read()
sents_1978 = cut_sent(treebank_1978)
data_1978 = ddp.parse(sents_1978)
print('Finish reading the treebank_1978.')

treebank_2000 = open('corpus_00_10.txt', 'r', encoding = 'utf-8').read()
sents_2000 = cut_sent(treebank_2000)
data_2000 = ddp.parse(sents_2000)
print('Finish reading the treebank_2000.')



treebank_web = open('web_fiction.txt', 'r', encoding='utf-8').read()
sents_web = cut_sent(treebank_web)
data_web = ddp.parse(sents_web)

build_conllx(data_web, 'treebank_web.conllx')
treebank_news = open('news.txt', 'r', encoding='utf-8').read()
sents_news = cut_sent(treebank_news)
data_news = ddp.parse(sents_news)


treebank_news_1950 = open('news_1950.txt', 'r', encoding='utf-8').read()
sents_news_1950 = cut_sent(treebank_news_1950)
data_news_1950 = ddp.parse(sents_news_1950)

treebank_news_1966 = open('news_1966.txt', 'r', encoding='utf-8').read()
sents_news_1966 = cut_sent(treebank_news_1966)
data_news_1966 = ddp.parse(sents_news_1966)

treebank_news_1978 = open('news_1978.txt', 'r', encoding='utf-8').read()
sents_news_1978 = cut_sent(treebank_news_1978)
data_news_1978 = ddp.parse(sents_news_1978)

treebank_lit_1950 = open('literature_1950.txt', 'r', encoding='utf-8').read()
sents_lit_1950= cut_sent(treebank_lit_1950)
data_lit_1950 = ddp.parse(sents_lit_1950)

treebank_lit_1966 = open('literature_1966.txt', 'r', encoding='utf-8').read()
sents_lit_1966= cut_sent(treebank_lit_1966)
data_lit_1966 = ddp.parse(sents_lit_1966)

treebank_lit_1978 = open('literature_1978.txt', 'r', encoding='utf-8').read()
sents_lit_1978= cut_sent(treebank_lit_1978)
data_lit_1978 = ddp.parse(sents_lit_1978)

treebank_lit_00 = open('literature_00.txt', 'r', encoding='utf-8').read()
sents_lit_00= cut_sent(treebank_lit_00)
data_lit_00 = ddp.parse(sents_lit_00)
# How many sentences in various copora
print('There are ', len(sents_1950), ' sentences in the corpus 1950-1965.')
print('There are ', len(sents_1966), ' sentences in the corpus 1966-1977.')
print('There are ', len(sents_1978), ' sentences in the corpus 1978-1999.')
print('There are ', len(sents_2000), ' sentences in the corpus 2000-2010.')
print('There are ', len(sents_1950+sents_1966+sents_1978+sents_2000), ' sentences in the whole corpus.')

# How many types in various copora
print('There are ', count_type(data_1950), ' types in the corpus 1950-1965.')
print('There are ', count_type(data_1966), ' types in the corpus 1966-1977.')
print('There are ', count_type(data_1978), ' types in the corpus 1978-1999.')
print('There are ', count_type(data_2000), ' types in the corpus 2000-2010.')
print('There are ', count_type(data_1950+data_1966+data_1978+data_2000), ' types in the whole corpus.')
# conclusion 1
print('There are ', count_rel(data_1950, 'deprel', 'ATT'),  'modifiers in one sentence on average (1950-1965).')
print('There are ', count_rel(data_1966, 'deprel', 'ATT'),  'modifiers in one sentence on average (1966-1977).')
print('There are ', count_rel(data_1978, 'deprel', 'ATT'),  'modifiers in one sentence on average (1978-1999).')
print('There are ', count_rel(data_2000, 'deprel', 'ATT'),  'modifiers in one sentence on average (2000-2010).')

# conclusion 2
print('There are ', count_rel(data_1950, 'deprel', 'SBV'),  'subjects in one sentence on average (1950-1965).')
print('There are ', count_rel(data_1966, 'deprel', 'SBV'),  'subjects in one sentence on average (1966-1977).')
print('There are ', count_rel(data_1978, 'deprel', 'SBV'),  'subjects in one sentence on average (1978-1999).')
print('There are ', count_rel(data_2000, 'deprel', 'SBV'),  'subjects in one sentence on average (2000-2010).')
print('There are ', count_rel(data_web, 'deprel', 'SBV'),  'subjects in one sentence on average (web).')
print('There are ', count_rel(data_news_1950, 'deprel', 'SBV'),  'subjects in one sentence on average.')
print('There are ', count_rel(data_news_1966, 'deprel', 'SBV'),  'subjects in one sentence on average.')
print('There are ', count_rel(data_news_1978, 'deprel', 'SBV'),  'subjects in one sentence on average.')
print('There are ', count_rel(data_news, 'deprel', 'SBV'),  'subjects in one sentence on average.')
print('There are ', count_rel(data_news, 'deprel', 'SBV'),  'subjects in one sentence on average.')
print('There are ', count_rel(data_lit_1950, 'deprel', 'SBV'),  'subjects in one sentence on average.')
print('There are ', count_rel(data_lit_1966, 'deprel', 'SBV'),  'subjects in one sentence on average.')
print('There are ', count_rel(data_lit_1978, 'deprel', 'SBV'),  'subjects in one sentence on average.')
print('There are ', count_rel(data_lit_00, 'deprel', 'SBV'),  'subjects in one sentence on average.')

# conclusion 3
print('There are', format(characterlen(sents_1950)/len(sents_1950), '.2f'), 'characters in one sentence on average (1950-1965).')
print('There are', format(characterlen(sents_1966)/len(sents_1966), '.2f'), 'characters in one sentence on average (1966-1977).')
print('There are', format(characterlen(sents_1978)/len(sents_1978), '.2f'), 'characters in one sentence on average (1978-1999).')
print('There are', format(characterlen(sents_2000)/len(sents_2000), '.2f'), 'characters in one sentence on average (2000-2010).')

print('There are', format(characterlen(sents_news_1950)/len(sents_news_1950), '.2f'), 'characters in one sentence on average (news 1950-1965).')
print('There are', format(characterlen(sents_news_1966)/len(sents_news_1966), '.2f'), 'characters in one sentence on average (news 1966-1976).')
print('There are', format(characterlen(sents_news_1978)/len(sents_news_1978), '.2f'), 'characters in one sentence on average (news 1978-1999).')
print('There are', format(characterlen(sents_news)/len(sents_news), '.2f'), 'characters in one sentence on average (news 2000-2010).')
