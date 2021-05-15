from ddparser import DDParser
from main import characterlen, count_type, get_corp

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


# parse the texts of different corpora
sents_1950 = get_corp('corpus_50_65.txt')
data_1950 = ddp.parse(sents_1950)
print('Finish reading the treebank_1950.')

sents_1966 = get_corp('corpus_66_76.txt')
data_1966 = ddp.parse(sents_1966)
print('Finish reading the treebank_1966.')

sents_1978 = get_corp('corpus_78_99.txt')
data_1978 = ddp.parse(sents_1978)
print('Finish reading the treebank_1978.')

sents_2000 = get_corp('corpus_00_10.txt')
data_2000 = ddp.parse(sents_2000)
print('Finish reading the treebank_2000.')


sents_web =[]
treebank_web = open('web_fiction.txt', 'r', encoding='utf-8')
for line in treebank_web.readlines():
    line = line.strip('\n')
    sents_web.append(line)
data_web = ddp.parse(sents_web)

# Define a function to find whether the root of the sentence has a subject
def get_sub(dic_list):
    count =0
    head_num=[]
    for word in dic_list:
        root_id = int(list(word['deprel']).index('HED'))+1
        if 'SBV' in list(word['deprel']):
            subj_index = [list(word['head'])[index] for index, element in enumerate(list(word['deprel'])) if element == 'SBV']
            for i in subj_index:
                head_num.append(list(word['head'])[i])
            if root_id in head_num:
                count+=1
    return count



# How many types in various copora
print('There are ', count_type(data_1950), ' types in the corpus 1950-1965.')
print('There are ', count_type(data_1966), ' types in the corpus 1966-1977.')
print('There are ', count_type(data_1978), ' types in the corpus 1978-1999.')
print('There are ', count_type(data_2000), ' types in the corpus 2000-2010.')
print('There are ', count_type(data_1950+data_1966+data_1978+data_2000), ' types in the whole corpus.')

# conclusion 1: how many modifiers in each sentence on average in different corpora
print('There are ', count_rel(data_1950, 'deprel', 'ATT'),  'modifiers in one sentence on average (1950-1965).')
print('There are ', count_rel(data_1966, 'deprel', 'ATT'),  'modifiers in one sentence on average (1966-1977).')
print('There are ', count_rel(data_1978, 'deprel', 'ATT'),  'modifiers in one sentence on average (1978-1999).')
print('There are ', count_rel(data_2000, 'deprel', 'ATT'),  'modifiers in one sentence on average (2000-2010).')

# conclusion 2: how many subjects in each sentence on average in different corpora
print('There are ', count_rel(data_1950, 'deprel', 'SBV'),  'subjects in one sentence on average (1950-1965).')
print('There are ', count_rel(data_1966, 'deprel', 'SBV'),  'subjects in one sentence on average (1966-1977).')
print('There are ', count_rel(data_1978, 'deprel', 'SBV'),  'subjects in one sentence on average (1978-1999).')
print('There are ', count_rel(data_2000, 'deprel', 'SBV'),  'subjects in one sentence on average (2000-2010).')

# conclusion 3 the average length of sentences in different corpora
print('There are', format(characterlen(sents_1950)/len(sents_1950), '.2f'), 'characters in one sentence on average (1950-1965).')
print('There are', format(characterlen(sents_1966)/len(sents_1966), '.2f'), 'characters in one sentence on average (1966-1977).')
print('There are', format(characterlen(sents_1978)/len(sents_1978), '.2f'), 'characters in one sentence on average (1978-1999).')
print('There are', format(characterlen(sents_2000)/len(sents_2000), '.2f'), 'characters in one sentence on average (2000-2010).')

# conclusion 4 the number of subjects attached to the root in each sentence on average in different corpora
print('There are', str(get_sub(data_1950)/len(sents_1950)), 'SUBJ in each sentence on average in the corpus 1950-1965.')
print('There are', str(get_sub(data_1966)/len(sents_1966)), 'SUBJ in each sentence on average in the corpus 1966-19676.')
print('There are', str(get_sub(data_1978)/len(sents_1978)), 'SUBJ in each sentence on average in the corpus 1977-1999.')
print('There are', str(get_sub(data_2000)/len(sents_2000)), 'SUBJ in each sentence on average in the corpus 2000-2010.')
print('There are', str(get_sub(data_web)/len(data_web)), 'SUBJ in each sentence on average in the web fiction category of the corpus 2000-2010.')

# supplementary conclusions
# the average length of sentences of the internet fictions
print('There are', format(characterlen(sents_web)/len(sents_web), '.2f'), 'characters in one sentence on average (2000-2010).')
# the average number of attributes of sentences of the internet fictions
print('There are ', count_rel(data_web, 'deprel', 'ATT'), 'attributes in one sentence on average(web).')
