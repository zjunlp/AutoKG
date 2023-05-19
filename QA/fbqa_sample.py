import os
import json
import random

fbqa_test_path = './FreebaseQA/FreebaseQA-eval.json'
seed = 1
sample_size = 20
sample_list = []
with open(fbqa_test_path, 'r') as f:
    data = json.load(f)
    questions = data["Questions"]
    # print('The number of questions in freebase_qa_test_set: ', len(questions))
    random.seed(seed)
    random.shuffle(questions)
    for i in range(sample_size):
        question = questions[i]
        sample = dict()
        sample["Question"] = question["RawQuestion"]
        sample["Answer"] = question["Parses"][0]["Answers"][0]["AnswersName"][0]
        sample_list.append(sample)

with open(f'./FreebaseQA/FreebaseQA-{sample_size}-sample.json', 'w') as f_w:
    json_obj = json.dumps(sample_list, indent=4)
    f_w.write(json_obj)
    print(f'./FreebaseQA/FreebaseQA-{sample_size}-sample.json', 'write done.')