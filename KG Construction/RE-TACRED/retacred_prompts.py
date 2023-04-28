import json

data = json.load(open('datas/retacred_train.json','r'))

predicate_all = []
for line in data:
    predicate_all.append( line['relation'])

predicate_all_set = set(predicate_all)
predicate_all = list(predicate_all_set)
print(predicate_all)
print(len(predicate_all))

num = 1
data = open('datas/retacred_sample.json', 'r', encoding='utf-8')
with open('prompts/retacred-1-shot-prompt.txt', 'w') as f:
    for line in data.readlines():
        ans_list = []
        dict = json.loads(line)

        f.write(str(num))
        num=num+1
        f.write("\n")

        # 0-shot
        # prompt = "The list of predicates: " + str(predicate_all)+" ." \
        #           "\nWhat Subject-Predicate-Object triples are included in the following sentence? " \
        #          "Please return the possible answers according to the list above. " \
        #              "Require the answer only in the form: [subject, predicate, object]" +\
        #          "\nThe given sentence is : " + str(dict['tokens'])  + \
        #          "\nTriples: \n"

        # 1-shot
        prompt = "The list of predicates : " + str(predicate_all) + " ." \
                 "\nWhat Subject-Predicate-Object triples are included in the following sentence? Please return the answers only in the form: [subject, predicate, object]" + \
                 "\n\nExample: "+\
                 "\nThe given sentence is : Piedra reported to the IRS that his practice gave $ 107,862 to Scientology groups in 2003 ." + \
                 "\nTriples: " +\
                 "[his, per:identity, Piedra]" + \
                 "\n\nThe given sentence is : " + str(dict['tokens']) + \
                 "\nTriples: \n"

        # print(prompt)
        f.write(prompt)
        f.write("\nRE-TACRED:\n["+str(dict["h"]["name"])+", "+ str(dict["relation"])+", "+str(dict["t"]["name"])+"]")
        f.write("\n h:"+str(dict["h"])+", t: "+str(dict["t"]))
        f.write("\n\n")
f.close()