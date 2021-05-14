from main import ddp, cut_sent, build_conllx
import pandas as pd
import nltk


df_ddparser= pd.read_csv('sample_ddparser.conllx', delimiter ='\t', header= None)
df_ddparser_gold = pd.read_csv('gold_ddparser.conllx', delimiter='\t', header = None)
df_ddparser_gold.columns = ['ID', 'FORM','LEMMA','POS','FEATS','HEAD','DEPREL']
# print the id, deprel, and head of wrongly parsed sentences

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


# find the misassigned head
for i in range(len(head_ddparser2)):
    if head_ddparser[i] != head_ddparser2[i]:
        mishead_ddparser.append(rel_ddparser[i])

# find the misassigned deprel
misrel = []

for i in range(len(rel_ddparser)):
    if rel_ddparser[i] != rel_ddparser2[i]:
        misrel.append(rel_ddparser[i])


mispos_ddparser=[]
# find the misassigned pos
for i in range(len(pos_ddparser2)):
    if pos_ddparser[i]!=pos_ddparser2[i]:
        mispos_ddparser.append(pos_ddparser[i])


wrong_sents = []
for i in range(len(head_ddparser)):
    if head_ddparser[i] != head_ddparser2[i] or rel_ddparser[i] != rel_ddparser2[i] or pos_ddparser2[i]!= pos_ddparser[i]:
        wrong_sents.append(df_ddparser_gold.index[i])
        wrong_sents.append(df_ddparser_gold.iloc[i])
print(wrong_sents)

wrong_pos_rel =[]
#
# for i in range(len(head_ddparser2)):
#     if rel_ddparser[i] != rel_ddparser2[i] and pos_ddparser2[i] != pos_ddparser[i]:
#         wrong_pos_rel.append(df_ddparser_gold.index[i])
#         wrong_pos_rel.append(df_ddparser_gold.iloc[i])
#
# print(wrong_pos_rel)
# # get the frequency of wrongly parsed head and deprel
# nltk.FreqDist(misrel).tabulate()
# nltk.FreqDist(mishead_ddparser).tabulate()
# nltk.FreqDist(mispos_ddparser).tabulate()
# nltk.FreqDist(misrel).plot(15, cumulative=False, title='Corrected Relations in the Original Parsing Result')
# nltk.FreqDist(mishead_ddparser).plot(15, cumulative=False,
#                                      title='Corrected Heads in the Original Parsing Result')
# nltk.FreqDist(mispos_ddparser).plot(18, cumulative=False,
#                                      title='Corrected POSs in the Original Parsing Result')