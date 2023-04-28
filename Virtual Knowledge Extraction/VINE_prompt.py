import json

data = json.load(open('datas/VINE.json', 'r' ))

predicate_all = []
for line in data:
    predicate_all.append( line['relation'])

predicate_all_set = set(predicate_all)
predicate_all = list(predicate_all_set)
print(predicate_all)
print(len(predicate_all))

li = 0
data = json.load(open('datas/VINE_sample.json', 'r', encoding='utf-8'))
with open('prompts/VINE-prompt.txt', 'w', encoding='utf-8') as f:
    while li < len(data):

        dict = data[li]
        sentence_1 = str(dict["tokens"])
        triple_1 = "["+str(dict["h"])+", "+ str(dict["relation"])+", "+str(dict["t"])+"]"

        li = li+1
        dict = data[li]
        sentence_2 = str(dict["tokens"])
        triple_2 = "["+str(dict["h"])+", "+ str(dict["relation"])+", "+str(dict["t"])+"]"

        li = li+1
        while  2 <= li % 10 <= 9:
            dict = data[li]

            sentence = str(dict["tokens"])
            triple = "[" + str(dict["h"]) + ", " + str(dict["relation"]) + ", " + str(dict["t"]) + "]"

            prompt = "There might be Subject-Predicate-Object triples in the following sentence. The predicate between the head and tail entities is known to be: "+str(dict["relation"])+"." \
                     "\nPlease find these two entities and give your answers in the form of [subject, predicate, object]."+ \
                     "\n\nExample: "+\
                     "\nThe given sentence is : " + sentence_1 + \
                     "\nTriples: " + triple_1+ \
                     "\nThe given sentence is : " + sentence_2 + \
                     "\nTriples: " + triple_2 + \
                     "\n\nThe given sentence is : " + str(dict['tokens']) + \
                     "\nTriples: \n"

            f.write(str(li % 10-1))
            li = li+1
            f.write("\n")
            print(prompt)
            f.write(prompt)
            f.write("\nVINE:\n["+str(dict["h"])+", "+ str(dict["relation"])+", "+str(dict["t"])+"]")
            f.write("\nsubj_type:  "+str(dict["subj_type"])+", "+ "obj_type: "+str(dict["obj_type"]))
            f.write("\n\n")
f.close()
