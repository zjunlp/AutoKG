import json
f =open("example.tsv")
fw=open("1_CHATGPT.json",'w')
for it in f.readlines():
    i=it.strip().split('\t')
    print(i)
    js={}
    js['head']=i[0]
    js['relation'] =i[1]
    js['tails']=i[2].split('    ')[0]
    js['generations']=[i for i in i[2].split('    ')[1].split(',')]
    js['greedy']=i[2].split('    ')[1].split(',')[0]
    fw.write(json.dumps(js)+'\n')