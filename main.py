from ddparser import DDParser
import re



# using ddparser
ddp = DDParser(use_pos=True)

# define a function to cut sentences
def cut_sent(text):
    new_sents =[]
    sents = re.split(r'(。”*"*）*」*|！”*"*）*」*|？”*"*|\.{6}”*」"*）*|……”*）*"*」*|\.」*"*)', text)
    for i in range(int(len(sents) / 2)):
        sent = sents[2 * i] + sents[2 * i + 1]
        new_sents.append(sent)
    return new_sents

# Define a function to count type
def count_type(parsedsents):
    type_list =[]
    for sent in parsedsents:
        for word in sent['word']:
            if word not in type_list:
                type_list.append(word)
    return len(type_list)


# define a function to generate conllx format
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

# count the character of the sentences
def characterlen(text):
    pat = r"\w"
    num = 0
    for i in range(len(text)):
        num += len(re.findall(pat, text[i]))
    return num


# define a function to only get the text from the corpus
def get_corp(textname):
    corpus = []
    doc =open(textname, 'r')
    for line in doc.readlines():
        line=line.strip()
        k = line.split('\t')[0]
        corpus.append(k)
    return corpus
