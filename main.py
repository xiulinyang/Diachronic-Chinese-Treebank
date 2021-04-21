from ddparser import DDParser
import re
import spacy
import stanza
import pandas as pd
from stanza.utils.conll import CoNLL


# define a function to cut sentences
def cut_sent(text):
    new_sents =[]
    sents = re.split(r'(。”*"*）*」*|！”*"*）*」*|？”*"*|\.{6}”*」"*）*|……”*）*"*」*|\.」*"*)', text)
    for i in range(int(len(sents) / 2)):
        sent = sents[2 * i] + sents[2 * i + 1]
        new_sents.append(sent)
    return new_sents

sample = open('sample_corpus.txt', 'r', encoding='utf-8').read()
sample_sents = cut_sent(sample)

# begin ddparser
ddp = DDParser(use_pos=True)
data = ddp.parse(sample_sents)

def build_conllx(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for iid, item in enumerate(data):
            if iid != 0:
                file.write('\n')
            assert len(item['word']) == len(item['head']) == len(item['deprel'])
            for idx in range(len(item['word'])):
                print(item['word'][idx])
                print("head: ", item['head'][idx])
                print('deprel', item['deprel'][idx])
                line = f"{idx+1}\t{item['word'][idx]}\t{item['word'][idx]}\t{item['postag'][idx]}\t-\t{item['head'][idx]}\t{item['deprel'][idx]}"
                file.write(line+'\n')
    print('The program is finished. ')

build_conllx(data, 'sample_ddparser.conllx')
build_conllx(data, 'gold_ddparser.conllx')
print('DDParser has finished the parsing.')



# begin SpaCy
nlp = spacy.load('zh_core_web_sm')
file_spacy = open('sample_spacy.conllx', 'w', encoding ='utf-8')
file_spacy_gold = open('gold_spacy.conllx', 'w', encoding= 'utf-8')
for sent in sample_sents:
    file_spacy.write('\n\n')
    file_spacy_gold.write('\n\n')
    for idx, token in enumerate(nlp(sent)):
        print(token.text)
        print(token.pos_)
        print(token.dep_)
        line = f'{idx+1}\t{token.text}\t{token.pos_}\t{token.dep_}\t{token.head}\t{token.head.i}'
        file_spacy.write(line+'\n')
        file_spacy_gold.write(line + '\n')
file_spacy.close()
file_spacy_gold.close()
print('SpaCy has finished the parsing.')

# begin stanza
stanza.download('zh', processors = 'tokenize, lemma, pos, depparse', logging_level='WARN')
print('Downloading finished.')
nlpp = stanza.Pipeline('zh', processors = 'tokenize, lemma, pos, depparse',  logging_level = 'WARN') #keep logging and only printing errors and warnings
print('Pipeline is ready.')
file_stanza = open('sample_stanza.tsv', 'w', encoding='utf-8')
file_stanza_gold = open('gold_stanza.tsv', 'w', encoding='utf-8')
for idx, sent in enumerate(sample_sents):
    file_stanza.write('\n\n'+ '# ' + str(idx) + '\n' + '#' + sent)
    file_stanza_gold.write('\n\n' + '# ' + str(idx) + '\n' + '#' + sent)
    dicts = nlpp(sent)
    dicts = dicts.to_dict()
    conll = CoNLL.convert_dict(dicts)
    for token in conll:
        file_stanza.write('\n')
        file_stanza_gold.write('\n')
        for id, info in enumerate(token):
            file_stanza.write('\n')
            file_stanza_gold.write('\n')
            for x in info:
                print(x)
                file_stanza.write(x+"\t")
                file_stanza_gold.write(x + "\t")

print('Stanza has finished the parsing.')
# to get the explanation of depdel
# a = ['acl', 'loc', 'dvp', 'loc', 'rcomp', 'amod', 'ordmod','asp', 'ba', 'aux:modal', 'aux:prtmod', 'auxpass', 'case', 'cc', 'ccomp', 'compound:nn', 'compound:vc', 'conj', 'cop', 'dep', 'discourse','dobj', 'etc', 'mark', 'mark:clf', 'nmod:assmod', 'nmod:poss', 'nmod:prep', 'nmod:range', 'nmod:tmod', 'nmod:topic', 'nsubj', 'nsubj:xsubj', 'nsubjpass','nummod', 'parataxis:prnmod', 'xcomp']
# b= []
# for x in a:
#     b.append(re.sub(r'.*:', '', x))
# print(b)
# for term in b:
#     print(term + '\n' + str(spacy.explain(term)))
#


df_spacy_gold = pd.read_csv("gold_spacy.conllx", delimiter='\t')
df_spacy = pd.read_csv('sample_spacy.conllx', delimiter = '\t')
df_ddparser_gold = pd.read_csv('gold_ddparser.conllx', delimiter='\t')
df_ddparser= pd.read_csv('sample_ddparser.conllx', delimiter = '\t')
df_stanza_gold = pd.read_csv('gold_stanza.tsv', delimiter='\t')
df_stanza = pd.read_csv('sample_stanza.tsv', delimiter='\t')


head_spacy = df_spacy_gold[df_spacy_gold.columns[4]]
head_spacy2 = df_spacy[df_spacy.columns[4]]
rel_spacy = df_spacy_gold[df_spacy_gold.columns[3]]
rel_spacy2 = df_spacy[df_spacy.columns[3]]
print(rel_spacy2)
mishead_spacy = []
las_spacy = []
for i in range(len(head_spacy2)):
    if head_spacy[i] != head_spacy2[i]:
        mishead_spacy.append(head_spacy[i])
for i in range(len(head_spacy)):
    if head_spacy[i] == head_spacy2[i]:
        if rel_spacy[i] == rel_spacy2[i]:
            las_spacy.append(rel_spacy[i])

head_ddparser = df_ddparser_gold[df_ddparser_gold.columns[5]]
head_ddparser2 = df_ddparser[df_ddparser.columns[5]]
rel_ddparser = df_ddparser_gold[df_ddparser_gold.columns[6]]
rel_ddparser2 = df_ddparser[df_ddparser.columns[6]]
mishead_ddparser = []
las_ddparser = []

for i in range(len(head_ddparser2)):
    if head_ddparser[i] != head_ddparser2[i]:
        mishead_ddparser.append(head_ddparser[i])

for i in range(len(head_ddparser)):
    if head_ddparser[i] == head_ddparser2[i]:
        if rel_ddparser[i] == rel_ddparser2[i]:
            las_ddparser.append(rel_ddparser[i])


head_stanza = df_stanza_gold[df_stanza_gold.columns[6]]
head_stanza2 = df_stanza[df_stanza.columns[6]]
rel_stanza = df_stanza_gold[df_stanza_gold.columns[7]]
rel_stanza2 = df_stanza[df_stanza.columns[7]]
mishead_stanza = []
las_stanza = []

for i in range(len(head_stanza2)):
    if head_stanza2[i] != head_stanza[i]:
        mishead_stanza.append(head_stanza[i])

for i in range(len(head_stanza2)):
    if head_stanza2[i] == head_stanza[i]:
        if rel_stanza[i] == rel_stanza2[i]:
            las_stanza.append(rel_stanza[i])

# Get the UAS and LAS of the parsing results of different parsers.
print('The UAS of stanza is: ')
print(format((1-len(mishead_stanza)/len(head_stanza))*100,'.2f'), '%')
print('The LAS of staza is: ')
print(format(len(las_stanza)*100/len(head_stanza), '.2f'), '%')
print('The UAS of SapCay is: ')
print(format((1-len(mishead_spacy)/len(head_spacy2))*100,'.2f'), '%')
print('The LAS of SapCay is: ')
print(format(len(las_spacy)*100/len(head_spacy), '.2f'), '%')
print('The UAS of DDParser is: ')
print(format((1-len(mishead_ddparser)/len(head_ddparser2))*100,'.2f'), '%')
print('The LAS of DDParser is: ')
print(format(len(las_ddparser)*100/len(head_ddparser), '.2f'), '%')

# Building the treebank using DDParser
treebank_1950 = open('corpus_50_65.txt', 'r', encoding='utf-8').read()
sents_1950 = cut_sent(treebank_1950)
data_1950 = ddp.parse(sents_1950)
build_conllx(data_1950, 'treebank_1950.conllx')
print('Finish building the treebank of 1950-1966.')

treebank_1966 = open('corpus_66_76.txt', 'r', encoding='utf-8').read()
sents_1966 = cut_sent(treebank_1966)
print('Text is segmented.')
data_1966 = ddp.parse(sents_1966)
build_conllx(data_1966, 'treebank_1966.conllx')
print('Finish building the treebank of 1967-1977.')



treebank_1978 = open('corpus_78_99.txt', 'r', encoding='utf-8').read()
sents_1978 = cut_sent(treebank_1978)
print('Text is segmented.')
data_1978 = ddp.parse(sents_1978)
build_conllx(data_1978, 'treebank_1978.conllx')
print('Finish building the treebank of 1978-1999.')

treebank_2000 = open('corpus_00_10.txt', 'r', encoding='utf-8').read()
sents_2000 = cut_sent(treebank_2000)
print('Text is segmented.')
data_2000 = ddp.parse(sents_2000)
build_conllx(data_2000, 'treebank_2000.conllx')
print('Finish building the treebank.')

# count the frequency of a specific deprel term
def count_rel(text, head, info):
    count = 0
    for i, sentence in enumerate(text):
        if i%1000 == 0:
            print(str(i) + ' sentences have been processed.')
        if sentence[head].count(info) > 0:
            count+= sentence[head].count(info)
    return format(count/len(text), '.2f')

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

# count the character of the sentences
def characterlen(text):
    pat = r"\w"
    num = 0
    for i in range(len(text)):
        num += len(re.findall(pat, text[i]))
    return num

# conclusion 3
print('There are', format(characterlen(sents_1950)/len(sents_1950), '.2f'), 'characters in one sentence on average (1950-1965).')
print('There are', format(characterlen(sents_1966)/len(sents_1966), '.2f'), 'characters in one sentence on average (1966-1977).')
print('There are', format(characterlen(sents_1978)/len(sents_1978), '.2f'), 'characters in one sentence on average (1978-1999).')
print('There are', format(characterlen(sents_2000)/len(sents_2000), '.2f'), 'characters in one sentence on average (2000-2010).')