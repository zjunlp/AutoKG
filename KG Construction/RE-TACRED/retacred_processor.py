import json
import random
data = json.load(open('datas/retacred_test.json','r'))
test  = []

for line in data:
    ins = {}
    ins['relation'] = line['relation']
    ins['tokens'] = ' '.join(line['token'])
    # ins['token'] = line['token']
    ins['h'] = {}
    ins['h']['name'] = ' '.join(line['token'][line['subj_start']:line['subj_end']+1])
    ins['h']['pos'] = [line['subj_start'], line['subj_end']+1]
    ins['subj_type'] = line['subj_type']
    ins['t'] = {}
    ins['t']['name'] = ' '.join(line['token'][line['obj_start']:line['obj_start']+1])
    ins['t']['pos'] = [line['obj_start'], line['obj_start']+1]
    ins['obj_type'] = line['obj_type']
    test.append(ins)

all_list_sampled = random.sample(test,40)

with open('datas/retacred_sample.json', 'w') as f:
    for line in all_list_sampled:
        f.write(json.dumps(line))
        f.write("\n")
f.close()