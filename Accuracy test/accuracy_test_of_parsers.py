from ddparser import DDParser
from main import build_conllx, cut_sent
import pandas as pd
import stanza
from stanza.utils.conll import CoNLL
import spacy


sample = open('sample_corpus.txt', 'r', encoding='utf-8').read()
sample_sents = cut_sent(sample)

'''Construct the sample corpus'''
# begin ddparser
ddp = DDParser(use_pos=True)
data = ddp.parse(sample_sents)
build_conllx(data, 'sample_ddparser.conllx')
print('DDParser has finished the parsing.')


# begin SpaCy
nlp = spacy.load('zh_core_web_sm')
file_spacy = open('sample_spacy.conllx', 'w', encoding ='utf-8')
# file_spacy_gold = open('gold_spacy.conllx', 'r', encoding='utf-8')
for sent in sample_sents:
    file_spacy.write('\n\n')
    # file_spacy_gold.write('\n\n')
    for idx, token in enumerate(nlp(sent)):
        print(token.text)
        print(token.pos_)
        print(token.dep_)
        line = f'{idx+1}\t{token.text}\t{token.pos_}\t{token.dep_}\t{token.head}\t{token.head.i}'
        file_spacy.write(line+'\n')
        # file_spacy_gold.write(line + '\n')
file_spacy.close()
# file_spacy_gold.close()
print('SpaCy has finished the parsing.')

# begin stanza
stanza.download('zh', processors = 'tokenize, lemma, pos, depparse', logging_level='WARN')
print('Downloading finished.')
nlpp = stanza.Pipeline('zh', processors = 'tokenize, lemma, pos, depparse',  logging_level = 'WARN') #keep logging and only printing errors and warnings
print('Pipeline is ready.')
file_stanza = open('sample_stanza.conllx', 'w', encoding='utf-8')
# file_stanza_gold = open('gold_stanza.conllx', 'r', encoding='utf-8')
for idx, sent in enumerate(sample_sents):
    # file_stanza_gold.write('\n\n' + '# ' + str(idx) + '\n' + '#' + sent)
    dicts = nlpp(sent)
    dicts = dicts.to_dict()
    conll = CoNLL.convert_dict(dicts)
    for token in conll:
        file_stanza.write('\n')
        # file_stanza_gold.write('\n')
        for id, info in enumerate(token):
            file_stanza.write('\n')
            # file_stanza_gold.write('\n')
            for x in info:
                print(x)
                file_stanza.write(x+"\t")
                # file_stanza_gold.write(x + "\t")

print('Stanza has finished the parsing.')

'''The following codes are related to accuracy tests of three models.'''
# Read the dataframe

df_spacy_gold = pd.read_csv("gold_spacy.conllx", delimiter='\t')
df_spacy = pd.read_csv('sample_spacy.conllx', delimiter = '\t')
df_ddparser= pd.read_csv('sample_ddparser.conllx', delimiter ='\t', header= None)
df_ddparser_gold = pd.read_csv('gold_ddparser.conllx', delimiter='\t', header = None)
df_ddparser_gold.columns = ['ID', 'FORM','LEMMA','POS','FEATS','HEAD','DEPREL']
df_stanza_gold = pd.read_csv('gold_stanza.conllx', delimiter='\t')
df_stanza = pd.read_csv('sample_stanza.conllx', delimiter='\t')


'''Accuracy test of SpaCy'''
# read the head column in the sample corpus and gold corpus respectively
head_spacy = df_spacy_gold[df_spacy_gold.columns[4]]
head_spacy2 = df_spacy[df_spacy.columns[4]]
# read the deprel column in the sample corpus and gold corpus respectively
rel_spacy = df_spacy_gold[df_spacy_gold.columns[3]]
rel_spacy2 = df_spacy[df_spacy.columns[3]]

# read the pos column in the sample corpus and gold corpus respectively
pos_spacy = df_spacy_gold[df_spacy_gold.columns[2]]
pos_spacy2 = df_spacy[df_spacy.columns[2]]

# find the misassigned head
mishead_spacy = []
las_spacy = []
postag_spacy=[]
for i in range(len(head_spacy2)):
    if head_spacy[i] != head_spacy2[i]:
        mishead_spacy.append(head_spacy[i])

# find the correctly assigned head and deprel
for i in range(len(head_spacy)):
    if head_spacy[i] == head_spacy2[i]:
        if rel_spacy[i] == rel_spacy2[i]:
            las_spacy.append(rel_spacy[i])

# find the correctly assigned pos tag
for i in range(len(pos_spacy2)):
    if pos_spacy[i] == pos_spacy2[i]:
        postag_spacy.append(pos_spacy2[i])

'''Accuracy test of DDParser'''
# read the head column in the sample corpus and gold corpus respectively
head_ddparser = df_ddparser_gold[df_ddparser_gold.columns[5]]
head_ddparser2 = df_ddparser[df_ddparser.columns[5]]

# read the deprel column in the sample corpus and gold corpus respectively
rel_ddparser = df_ddparser_gold[df_ddparser_gold.columns[6]]
rel_ddparser2 = df_ddparser[df_ddparser.columns[6]]

# read the pos column in the sample corpus and the gold corpus respectively
pos_ddparser = df_ddparser_gold[df_ddparser_gold.columns[3]]
pos_ddparser2 = df_ddparser[df_ddparser.columns[3]]



mishead_ddparser = []
las_ddparser = []
postag_ddparser =[]

# find the misassigned head
for i in range(len(head_ddparser2)):
    if head_ddparser[i] != head_ddparser2[i]:
        mishead_ddparser.append(rel_ddparser[i])

# find the correctly assigned head and deprel
for i in range(len(head_ddparser)):
    if head_ddparser[i] == head_ddparser2[i]:
        if rel_ddparser[i] == rel_ddparser2[i]:
            las_ddparser.append(rel_ddparser[i])

# find the correctly assigned pos tag
for i in range(len(pos_ddparser2)):
    if pos_ddparser[i] == pos_ddparser2[i]:
        postag_ddparser.append(pos_ddparser2[i])

'''Accuracy test of stanza'''
# read the head column in the sample corpus and gold corpus respectively
head_stanza = df_stanza_gold[df_stanza_gold.columns[6]]
head_stanza2 = df_stanza[df_stanza.columns[6]]

# read the deprel column in the sample corpus and gold corpus respectively
rel_stanza = df_stanza_gold[df_stanza_gold.columns[7]]
rel_stanza2 = df_stanza[df_stanza.columns[7]]

#read the pos column in the sample corpus and gold corpus respectively
pos_stanza = df_stanza_gold[df_stanza_gold.columns[3]]
pos_stanza2 = df_stanza[df_stanza.columns[3]]
mishead_stanza = []
las_stanza = []
postag_stanza =[]
# find the misassigned head
for i in range(len(head_stanza2)):
    if head_stanza2[i] != head_stanza[i]:
        mishead_stanza.append(head_stanza[i])

# find the correctly assigned head and deprel
for i in range(len(head_stanza2)):
    if head_stanza2[i] == head_stanza[i]:
        if rel_stanza[i] == rel_stanza2[i]:
            las_stanza.append(rel_stanza[i])

# find the correctly assigned pos tag
for i in range(len(pos_stanza2)):
    if pos_stanza[i] == pos_stanza2[i]:
        postag_stanza.append(pos_stanza[i])


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

# get the pos tag accuracy
print('The POS arruracy of ddparser is ')
print(format(len(postag_ddparser)/len(pos_ddparser)*100, '.2f'), '%')
print('The POS arruracy of Spacy is ')
print(format(len(postag_spacy)/len(pos_spacy)*100, '.2f'), '%')
print('The POS arruracy of stanza is ')
print(format(len(postag_stanza)/len(pos_stanza)*100, '.2f'), '%')

'''NER OF THREE MODELS'''

# compute the NER accuracy of ddparser

# read the named entity text
entity = pd.read_csv("named_entities.csv", sep=',')
words = list(entity.word)
mydict = dict(zip(entity.word, entity.pos))
ddp_token=[]
ddp_pos =[]

for sent in data:
    for i, word in enumerate(sent['word']):
        if word in words:
            ddp_token.append(word)
            if sent['postag'][i] == mydict[word]:
                ddp_pos.append(sent['postag'][i])

recall_ddp = round(len(ddp_token)/len(words),2)
precision_ddp = round(len(ddp_pos)/len(ddp_token),2)
f1_ddp = round(2*recall_ddp*precision_ddp/(recall_ddp+precision_ddp),2)


# Form two lists containing the token and its pos tag respectively.
spacy_token=[]
spacy_pos =[]
for sent in sample_sents:
    for token in nlp(sent):
        spacy_token.append(token.text)
        spacy_pos.append(token.pos_)


stanza_token = []
stanza_pos =[]
for sent in sample_sents:
    parsed_stanza= nlpp(sent).to_dict()
    for token in parsed_stanza:
        for inf in token:
            stanza_token.append(inf['text'])
            stanza_pos.append(inf['upos'])

# define a function to calculate the NER accuracy of SpaCy and Stanza
# as the named entities are labeled as PROPN in both models
def ner(lst1, lst2):
    name_recall =[]
    name_prec =[]
    for i, word in enumerate(lst1):
        if word in words:
            name_recall.append(word)
            if lst2[i] =='PROPN':
                name_prec.append(token)
    recall = round(len(name_recall)/len(words),2)
    precision = round(len(name_prec)/len(name_recall),2)
    f1 = round(recall*precision*2/(recall+precision),2)
    return recall, precision,f1

print('The NER recall, precision and F1 of SpaCy is ', ner(spacy_token, spacy_pos))
print('The NER recall, precision and F1 of DDParser is ', recall_ddp, precision_ddp, f1_ddp)
print('The NER recall, precision and F1 of stanza is ', ner(stanza_token, stanza_pos))

