import json
import random
data = open('datas/scierc_test.json', 'r', encoding='utf-8')
test  = []

for line in data.readlines():
    dict = json.loads(line)
    ins = {}
    ins['relation'] = dict['relation']
    ins['tokens'] = ' '.join(dict['token'])
    ins["h"] = dict['h']
    ins["t"] = dict['t']
    test.append(ins)

all_list_sampled = random.sample(test,40)

relation_list=[]
with open('datas/scierc_sample.json', 'w') as f:
    for line in all_list_sampled:
        f.write(json.dumps(line))
        f.write("\n")
f.close()