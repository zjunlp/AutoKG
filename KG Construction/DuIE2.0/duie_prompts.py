# -*- coding:utf-8 -*-
import json

data = open('datas/duie_dev.json', 'r', encoding='utf-8')

predicate_all=[]
for line in data.readlines():
    dict = json.loads(line)
    for spo in dict["spo_list"]:
        predicate_all.append(spo['predicate'])

predicate_all_set = set(predicate_all)
predicate_all = list(predicate_all_set)
print(predicate_all)
print(len(predicate_all))

num = 1
data = open('datas/duie_sample.json','r',encoding='utf-8')
with open('prompts/duie-1-shot-prompt.txt', 'w', encoding='utf-8') as f:
    for line in data.readlines():
        ans_list = []
        dict = json.loads(line)

        f.write(str(num))
        num=num+1
        f.write("\n")

        #0-shot
        # prompt =  "已知候选谓词列表： " + str(predicate_all)+" ." + \
        #           "\n请从以下文本中提取可能的主语-谓语-宾语三元组(SPO三元组)，并以[[主语，谓语，宾语]，...]的形式回答" + \
        #           "\n给定句子： " + str(dict['text']) + "." + \
        #           "\nSPO三元组: \n"

        #1-shot
        prompt = "已知候选谓词列表： " + str(predicate_all) + " ." + \
                 "\n请从以下文本中提取可能的主语-谓语-宾语三元组(SPO三元组)，并以[[主语，谓语，宾语]，...]的形式回答" + \
                 "\n\n例如: "+\
                 "\n给定句子: 641年3月2日文成公主入藏，与松赞干布和亲. " + \
                 "\nSPO三元组: " +\
                 "[松赞干布 , 妻子 , 文成公主 ]、[文成公主 , 丈夫 , 松赞干布 ]" + \
                 "\n\n给定句子: " + str(dict['text']) + \
                 "\nSPO三元组: \n"

        # print(prompt)
        f.write(prompt)
        f.write("\nDuie2.0 :\n")
        for spo in dict["spo_list"]:
            f.write("["+str(spo["subject"])+" , "+str(spo["predicate"])+" , "+str(spo["object"]["@value"])+" ]\n")
        f.write("\n\n")
f.close()