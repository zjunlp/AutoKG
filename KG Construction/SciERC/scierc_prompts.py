import json

data = open('datas/scierc_test.json', 'r')

predicate_all=[]
for line in data.readlines():
    dict = json.loads(line)
    predicate_all.append(dict['relation'])

predicate_all_set = set(predicate_all)
predicate_all = list(predicate_all_set)
print(predicate_all)
print(len(predicate_all))

num = 1
data = open('datas/scierc_sample.json', 'r', encoding='utf-8')
with open('prompts/scierc-1-shot-prompt.txt', 'w') as f:
    for line in data.readlines():
        ans_list = []
        dict = json.loads(line)

        f.write(str(num))
        num=num+1
        f.write("\n")

        # 0-shot
        # prompt = "The list of predicates: " + str(predicate_all)+" ." \
        #           "\nWhat Subject-Predicate-Object triples are included in the following sentence? Please return the possible answers according to the list above. Require the answer only in the form : [subject, predicate, object]" +\
        #          "\nThe given sentence is : " + str(dict['tokens'])  + \
        #          "\nTriples: \n"

        # 1-shot
        prompt = "The list of predicates: " + str(predicate_all)+" ." \
                  "\nWhat Subject-Predicate-Object triples are included in the following sentence? Please return the possible answers according to the list above. Require the answer only in the form: [subject, predicate, object]" +\
                 "\n\nExample: "+\
                 "\nThe given sentence is :  We show that various features based on the structure of email-threads can be used to improve upon lexical similarity of discourse segments for question-answer pairing . " + \
                 "\nTriples: " +\
                 "[lexical similarity , FEATURE-OF , discourse segments]" + \
                 "\n\nThe given sentence is : " + str(dict['tokens']) + \
                 "\nTriples: \n"

        # print(prompt)
        f.write(prompt)
        f.write("\nSciERC:\n["+str(dict["h"]["name"])+", "+ str(dict["relation"])+", "+str(dict["t"]["name"])+"]")
        f.write("\n h:"+str(dict["h"])+", t: "+str(dict["t"]))
        f.write("\n\n")
f.close()
