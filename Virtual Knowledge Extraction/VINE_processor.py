import json
import random

data = json.load(open('datas/VINE.json', 'r'))
predicate_all = []
for line in data:
    predicate_all.append(line['relation'])

predicate_all_set = set(predicate_all)
predicate_all = list(predicate_all_set)
# print(predicate_all)
# print(len(predicate_all))

all_sampled=[]
for i in range(len(predicate_all)):
    train = []
    #获取每个关系的例子，每个关系选取10个例子
    data = json.load(open('datas/VINE.json', 'r', encoding='utf-8'))
    for line in data:
        if line['relation'] == predicate_all[i]:
            train.append(line)
    type_sampled = random.sample(train,10)
    random.shuffle(type_sampled)
    all_sampled = all_sampled+type_sampled

print(len(all_sampled))
with open('datas/VINE_sample.json', 'w', encoding='utf-8') as f:
    json.dump(all_sampled, f, indent=4)
f.close()




