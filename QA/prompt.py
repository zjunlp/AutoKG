import os 
import json
import random

def fbqa_prompt(shot: int=0, test_path='./FreebaseQA/FreebaseQA-20-sample.json'):
    prefix = 'Please answer the following question: \n'
    if shot == 1:
        save_path = './FreebaseQA/FreebaseQA-20-sample-prompt-1_shot.json'
    else:
        save_path = './FreebaseQA/FreebaseQA-20-sample-prompt-0_shot.json'
    # save_path = './FreebaseQA/FreebaseQA-20-sample-prompt-davinci.json'
    with open(test_path, 'r') as f:
        data = json.load(f)
    prompt_ans = []
    for sample in data:
        # prompt = prefix + sample['Question']
        # prompt = sample['Question']
        if shot == 0:
            prompt = prefix + 'Question: ' + sample['Question'] + '\nAnswer: '
        elif shot == 1:
            icl = "Question: Who wrote the 1956 novel '101 Dalmatians'?\nAnswer: dodie smith\n"
            prompt = prefix + icl + 'Question: ' + sample['Question'] + '\nAnswer: '
        ans = sample['Answer']
        example = {'prompt': prompt, 'answer': ans}
        prompt_ans.append(example)

    with open(save_path, 'w') as f_w:
        json_obj = json.dumps(prompt_ans, indent=4)
        f_w.write(json_obj)
        print(f'{save_path} write done.')


def meta_prompt(shot: int=0, test_path='./MetaQA/MetaQA-20-sample.json'):
    prefix = 'Please answer the following question. Note that there may be more than one answer to the question. \n'
    if shot == 0:  
        save_path = './MetaQA/MetaQA-20-sample-prompt-0_shot.json'
    else:
        save_path = './MetaQA/MetaQA-20-sample-prompt-1_shot.json'
    # save_path = './MetaQA/MetaQA-20-sample-prompt-davinci.json'
    with open(test_path, 'r') as f:
        data = json.load(f)
    prompt_type_ans = []
    for k, v in data.items():
        for sample in v:
            # prompt = prefix + sample['Question'] + ' ?'
            # prompt = sample['Question'] + ' ?'
            if shot == 0:
                prompt = prefix + 'Question: ' + sample['Question'] + ' ?' + '\nAnswer: '
            elif shot == 1:
                icl_1 = "Question: [Aaron Lipstadt] was the director of which movies ?\nAnswer: Android|City Limits\n"
                icl_2 = "Question: the director of [Five Weeks in a Balloon] also directed which movies ?\nAnswer: The Swarm|The Poseidon Adventure|Voyage to the Bottom of the Sea|Beyond the Poseidon Adventure|The Lost World\n"
                icl_3 = "Question: what were the release years of the films that share directors with the film [Yor, the Hunter from the Future] ?\nAnswer: 1964|1965\n"
                prompt = prefix + icl_1 + icl_2 + icl_3 + 'Question: ' + sample['Question'] + ' ?' + '\nAnswer: '
            type_ = k
            ans = sample['Answer']
            example = {'prompt': prompt, 'type': type_, 'answer': ans}
            prompt_type_ans.append(example)

    with open(save_path, 'w') as f_w:
        json_obj = json.dumps(prompt_type_ans, indent=4)
        f_w.write(json_obj)
        print(f'{save_path} write done.')

if __name__ == "__main__":
    fbqa_prompt(0)
    meta_prompt(0)
    fbqa_prompt(1)
    meta_prompt(1)