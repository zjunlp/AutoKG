import json
import random
data = open('datas/duie_dev.json', 'r', encoding='utf-8')
valid  = []

for line in data.readlines():
    dict = json.loads(line)
    # print(dict.keys())
    ins = {}
    ins['text'] = dict['text']
    ins["spo_list"] = dict["spo_list"]
    valid.append(ins)

all_list_sampled = random.sample(valid,40)

with open('datas/duie_sample.json', 'w', encoding='utf-8') as f:
    for line in all_list_sampled:
        f.write(json.dumps(line, ensure_ascii=False))
        f.write("\n")
f.close()