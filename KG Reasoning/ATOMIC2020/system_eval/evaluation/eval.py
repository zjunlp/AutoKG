from evaluation.bleu.bleu import Bleu
from evaluation.meteor.meteor_nltk import Meteor
from evaluation.rouge.rouge import Rouge
from evaluation.cider.cider import Cider
# from evaluation.bert_score.bert_score import BertScore
from collections import defaultdict
from argparse import ArgumentParser

import sys
import json
#reload(sys)
#sys.setdefaultencoding('utf-8')

class QGEvalCap:
    def __init__(self, model_key, gts, res, results_file=None):
        self.gts = gts
        self.res = res
        self.results_file = results_file
        self.model_key = model_key

    def evaluate(self):
        output = []
        scorers = [
            (Bleu(1), ["Bleu_1"]),
        ]

        # =================================================
        # Compute scores
        # =================================================
        score_dict = {}
        scores_dict = {}
        #scores_dict["model_key"] = self.model_key
        for scorer, method in scorers:
            # print 'computing %s score...'%(scorer.method())
            score, scores = scorer.compute_score(self.gts, self.res)
            if type(method) == list:
                for sc, scs, m in zip(score, scores, method):
                    #print("%s: %0.5f"%(m, sc))
                    output.append(sc)
                    score_dict[m] = str(sc)
                    scores_dict[m] = list(scs)
            else:
                #print("%s: %0.5f"%(method, score))
                output.append(score)
                score_dict[method] = score
                scores_dict[method] = list(scores)

        if self.results_file != None:
            with open(self.results_file, "a") as f:
                f.write(json.dumps(score_dict)+"\n")

        return score_dict, scores_dict

def eval(model_key, sources, references, predictions, results_file=None):
    """
        Given a filename, calculate the metric scores for that prediction file
        isDin: boolean value to check whether input file is DirectIn.txt
    """

    pairs = []
    
    for tup in sources:
        pair = {}
        pair['tokenized_sentence'] = tup
        pairs.append(pair)

    cnt = 0
    for line in references:
        pairs[cnt]['tokenized_question'] = line
        cnt += 1

    output = predictions

    for idx, pair in enumerate(pairs):
        pair['prediction'] = output[idx]

    ## eval
    from evaluation.eval import QGEvalCap
    import json
    from json import encoder
    encoder.FLOAT_REPR = lambda o: format(o, '.4f')

    res = defaultdict(lambda: [])
    gts = defaultdict(lambda: [])
    for pair in pairs[:]:
        key = pair['tokenized_sentence']
        #res[key] = [pair['prediction']]
        res[key] = pair['prediction']
 
        ## gts 
        gts[key].append(pair['tokenized_question'])

    QGEval = QGEvalCap(model_key, gts, res, results_file)
    return QGEval.evaluate()


def preprocess(file_name, keys):
    with open(file_name) as f:
        data = f.readlines()
        generations = [json.loads(elem) for elem in data]

    predictions = {}
    references = {}
    sources = {}
    keys_list = keys if keys!=None else generations["generations"]
    for key in keys_list:
        references[key] = []
        predictions[key] = []
        sources[key] = []

    for elem in generations:
        label = elem["label"]
        hyp = elem["hyp"+label]
        for key in keys_list:
            if key in elem["generations"]:
                references[key].append(hyp)
                predictions[key].append(elem["generations"][key])
                sources[key].append((elem["obs1"], elem["obs2"]))

    return sources, references, predictions


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-gen_file", "--gen_file", dest="gen_file", help="generations file with gold/references")
    parser.add_argument("--keys", type=str, default=None, help="comma-separated list of model keys")
    parser.add_argument("--results_file", default="eval_results.jsonl")
    args = parser.parse_args()

    print("scores: \n")
    keys=None
    if args.keys:
        keys = args.keys.split(",")
    
    sources, references, predictions = preprocess(args.gen_file, keys)
    for key in references.keys():
        print("\nEvaluating %s" %key)
        eval(key, sources[key], references[key], predictions[key], args.results_file)

