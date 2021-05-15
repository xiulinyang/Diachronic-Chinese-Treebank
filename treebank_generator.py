from main import ddp

# Read the dictionary from a txt file
def get_dic(corpname):
    dic={}
    doc =open(corpname, 'r')
    for line in doc.readlines():
        line=line.strip()
        k = line.split('\t')[0]
        v = line.split('\t')[-1]
        dic[k]=v
    return dic

# Append the metadata information to the parsed result.
def append_dic(doc):
    data_time=[]
    try:
        for key, value in doc.items():
            parse = ddp.parse(key)
            for sent in parse:
                sent.update({key:value})
                data_time.append(sent)
    except TypeError:
        print(doc.items())
    return data_time

# write a function to make the output in the format of conLL-X
def build_conllx(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for iid, item in enumerate(data):
            key = list(item.values())[4]
            key = list(key.split(','))
            if len(key) ==3:
                file.write('\n'+'#sent_id:'+ str(iid))
                file.write('\n'+'#time:'+str(key[0][8:]))
                file.write('\n'+'#genre:'+ str(key[1][9:]))
                file.write('\n'+'#name:'+str(key[-1][8:-1]))
                file.write('\n'+'#sent:'+str(list(item.keys())[4]) +'\n')
            if len(key)==4:
                file.write('\n'+'#sent_id:' + str(iid))
                file.write('\n'+'#time:' + str(key[0][8:]))
                file.write('\n'+'#genre:' + str(key[1][9:]))
                file.write('\n'+'#category:' +str(key[-2][12:]))
                file.write('\n'+'#name:' + str(key[-1][8:-1]))
                file.write('\n' + '#sent:' + str(list(item.keys())[4]) + '\n')
            assert len(item['word']) == len(item['head']) == len(item['deprel'])
            for idx in range(len(item['word'])):
                print(item['word'][idx])
                print("head: ", item['head'][idx])
                print('deprel', item['deprel'][idx])
                line = f"{idx+1}\t{item['word'][idx]}\t{item['word'][idx]}\t{item['postag'][idx]}\t-\t{item['head'][idx]}\t{item['deprel'][idx]}"
                file.write(line+'\n')
    print('The program is finished. ')

# Building the treebank using DDParser
treebank_1950 = get_dic('corpus_50_65.txt')
print('Get the dictionary.')
data_1950 = append_dic(treebank_1950)
print('Append the metadata')
build_conllx(data_1950, 'treebank_1950.conllx')
print('Finish building the treebank of 1950-1966.')


treebank_1966 = get_dic('corpus_66_76.txt')
print('Get the dictionary.')
data_1966 = append_dic(treebank_1966)
print('Append the metadata')
build_conllx(data_1966, 'treebank_1966.conllx')
print('Finish building the treebank of 1967-1977.')

treebank_1978 = get_dic('corpus_78_99.txt')
print('Get the dictionary.')
data_1978 = append_dic(treebank_1978)
print('Append the metadata')
build_conllx(data_1978, 'treebank_1978.conllx')
print('Finish building the treebank of 1978-1999.')

treebank_00 = get_dic('corpus_00_10.txt')
print('Get the dictionary.')
data_00 = append_dic(treebank_00)
print('Append the metadata')
build_conllx(data_00, 'treebank_2000.conllx')
print('Finish building the treebank.')

# Define a function to calculate the number of tokens
def count_token(data):
    num = 0
    for sent in data:
        num += len(sent['word'])
    return num

# calculate tokens

print('There are', str(count_token(data_1950)), 'tokens in the treebank 1950-1965.')
print('There are', str(count_token(data_1966)), 'tokens in the treebank 1966-1976.')
print('There are', str(count_token(data_1978)), 'tokens in the treebank 1978-1999.')
print('There are', str(count_token(data_00)), 'tokens in the treebank 2000-2010.')
print('There are', str(count_token(data_1950)+count_token(data_1966)+count_token(data_1978)+count_token(data_00)), 'tokens in the whole treebank.')