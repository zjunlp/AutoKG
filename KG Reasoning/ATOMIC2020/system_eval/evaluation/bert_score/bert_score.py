from bert_score import score
# Code for BertScore reused from original implementation: https://github.com/Tiiiger/bert_score

class BertScore:
    def __init__(self):
        self._hypo_for_image = {}
        self.ref_for_image = {}

    def compute_score(self, gts, res):

        assert(gts.keys() == res.keys())
        imgIds = gts.keys()

        hyp_input = []
        ref_input = []
        same_indices = []
        for id in imgIds:
            hypo = res[id]
            ref = gts[id]

            # Sanity check.
            assert(type(hypo) is list)
            assert(len(hypo) == 1)
            assert(type(ref) is list)
            assert(len(ref) >= 1)

            hyp_input += [hypo[0]] * len(ref)
            ref_input += ref
            same_indices.append(len(ref_input))

        p, r, f_scores = score(hyp_input, ref_input, model_type="bert-base-uncased")
 
        prev_idx = 0
        aggreg_f1_scores = []
        for idx in same_indices:
            aggreg_f1_scores.append(f_scores[prev_idx: idx].mean().cpu().item())
            prev_idx = idx

        return sum(aggreg_f1_scores)/len(aggreg_f1_scores), aggreg_f1_scores

    def method(self):
        return "Bert Score"
