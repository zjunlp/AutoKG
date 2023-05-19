import os
import json
import random

def statistics(hop_num: int, split: str, ):
    path = f'./MetaQA/{hop_num}-hop/qa_{split}_qtype.txt'
    qtype_set = set()
    qtype_list = []
    with open(path, 'r') as f:
        data = f.readlines()
        print(f'MetaQA {hop_num}-hop {split} set: {len(data)} questions.')
        for line in data:
            qtype_set.add(line.strip())
            qtype_list.append(line.strip())
    return qtype_set, qtype_list

def sample(hop_num: int, sample_size=3, seed=1):
    path = f'./MetaQA/{hop_num}-hop/vanilla/qa_test.txt'
    qtype_example = dict()
    with open(path, 'r') as f:
        data = f.readlines()
        qtype_set, qtype_list = statistics(hop_num, 'test')
        for i in range(len(data)):
            line = data[i]
            qtype = qtype_list[i]
            if qtype not in qtype_example:
                qtype_example[qtype] = []
            ex = dict()
            ex['Question'] = line.strip().split('\t')[0]
            ex['Answer'] = line.strip().split('\t')[1].split('|')
            qtype_example[qtype].append(ex)
    random.seed(seed)
    for k, v in qtype_example.items():
        random.shuffle(v)
    # sample
    sample_dict = dict()
    for k, v in qtype_example.items():
        sample_dict[k] = v[:sample_size]
    # write
    with open(f'./MetaQA/{hop_num}-hop/vanilla/qa_test-{sample_size}-sample.json', 'w') as f_w:
        json_obj = json.dumps(sample_dict, indent=4)
        f_w.write(json_obj)
        print(f'./MetaQA/{hop_num}-hop/vanilla/qa_test-{sample_size}-sample.json', 'write done.')   

if __name__ == "__main__":
    for hop_num in [1, 2, 3]:
        sample(hop_num, sample_size=1, seed=1)

    # for hop_num in [1, 2, 3]:
    #     train_qtype_set, train_qtype_list = statistics(hop_num, 'train')
    #     dev_qtype_set, dev_qtype_list = statistics(hop_num, 'dev')
    #     test_qtype_set, test_qtype_list = statistics(hop_num, 'test')
    #     print(f'MetaQA {hop_num}-hop train set: {len(train_qtype_set)} question types.')
    #     print(f'MetaQA {hop_num}-hop dev set: {len(dev_qtype_set)} question types.')
    #     print(f'MetaQA {hop_num}-hop test set: {len(test_qtype_set)} question types.')

