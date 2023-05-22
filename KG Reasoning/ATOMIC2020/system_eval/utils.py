import json
import sys
import csv
import operator
import random


def read_csv(input_file, quotechar='"', delimiter=",", skip_header=False):
    """Reads a tab separated value file."""
    with open(input_file, "r") as f:
        reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar, quoting=csv.QUOTE_ALL, skipinitialspace=True)
        lines = []
        for line in reader:
            if sys.version_info[0] == 2:
                line = list(unicode(cell, 'utf-8') for cell in line)
            lines.append(line)
        if skip_header:
            lines = lines[1:]
        return lines


def write_tsv(output_file, data, header=False):
    keys = list(data[0].keys())
    with open(output_file, 'w') as f:
        w = csv.DictWriter(f, keys, delimiter='\t', lineterminator='\n')
        if header:
            w.writeheader()
        for r in data:
            entry = {k: r[k] for k in keys}
            w.writerow(entry)


def write_array2tsv(output_file, data, header=False):
    keys = range(len(data[0]))
    with open(output_file, 'w') as f:
        w = csv.DictWriter(f, keys, delimiter='\t', lineterminator='\n')
        if header:
            w.writeheader()
        for r in data:
            entry = {k: r[k] for k in keys}
            w.writerow(entry)


def write_csv(filename, data, fieldnames):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for d in data:
            formatted_d = {}
            for key, val in d.items():
                formatted_d[key] = json.dumps(val)
            writer.writerow(formatted_d)


def read_jsonl(filename):
    data = []
    with open(filename, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return data


def write_items(output_file, items):
    with open(output_file, 'w') as f:
        for concept in items:
            f.write(concept + "\n")
    f.close()


def write_jsonl(f, d):
    write_items(f, [json.dumps(r) for r in d])


def count_relation(d):
    relation_count = {}
    prefix_count = {}
    head_count = {}
    for l in d:
        r = l[1]
        if r not in relation_count.keys():
            relation_count[r] = 0
        relation_count[r] += 1

        prefix = l[0]+l[1]
        if prefix not in prefix_count.keys():
            prefix_count[prefix] = 0
        prefix_count[prefix] += 1

        head = l[0]
        if head not in head_count.keys():
            head_count[head] = 0
        head_count[head] += 1

    sorted_relation_count = dict(sorted(relation_count.items(), key=operator.itemgetter(1), reverse=True))
    sorted_prefix_count = dict(sorted(prefix_count.items(), key=operator.itemgetter(1), reverse=True))
    sorted_head_count = dict(sorted(head_count.items(), key=operator.itemgetter(1), reverse=True))

    print("Relations:")
    for r in sorted_relation_count.keys():
        print(r, sorted_relation_count[r])

    print("\nPrefixes:")
    print("uniq prefixes: ", len(sorted_prefix_count.keys()))
    i = 0
    for r in sorted_prefix_count.keys():
        print(r, sorted_prefix_count[r])
        i += 1
        if i > 20:
            break

    print("\nHeads:")
    i = 0
    for r in sorted_head_count.keys():
        print(r, sorted_head_count[r])
        i += 1
        if i > 20:
            break


def get_head_set(d):
    return set([l[0] for l in d])


def head_based_split(data, dev_size, test_size, head_size_threshold=500, dev_heads=[], test_heads=[]):
    """
    :param data: the tuples to split according to the heads, where the head is the first element of each tuple
    :param dev_size: target size of the dev set
    :param test_size: target size of the test set
    :param head_size_threshold: Maximum number of tuples a head can be involved in,
    in order to be considered for the dev/test set'
    :param dev_heads: heads that are forced to belong to the dev set
    :param test_heads: heads that are forced to belong to the test set
    :return:
    """
    head_count = {}
    for l in data:
        head = l[0]
        if head not in head_count.keys():
            head_count[head] = 0
        head_count[head] += 1

    remaining_heads = dict(head_count)

    test_selected_heads = {}
    test_head_total_count = 0

    for h in test_heads:
        if h in remaining_heads:
            c = remaining_heads[h]
            test_selected_heads[h] = c
            test_head_total_count += c
            remaining_heads.pop(h)

    while test_head_total_count < test_size:
        h = random.sample(remaining_heads.keys(), 1)[0]
        c = remaining_heads[h]
        if c < head_size_threshold:
            test_selected_heads[h] = c
            test_head_total_count += c
            remaining_heads.pop(h)

    test = [l for l in data if l[0] in test_selected_heads.keys()]

    dev_selected_heads = {}
    dev_head_total_count = 0

    for h in dev_heads:
        if h in remaining_heads:
            c = remaining_heads[h]
            dev_selected_heads[h] = c
            dev_head_total_count += c
            remaining_heads.pop(h)

    while dev_head_total_count < dev_size:
        h = random.sample(remaining_heads.keys(), 1)[0]
        c = remaining_heads[h]
        if c < head_size_threshold:
            dev_selected_heads[h] = c
            dev_head_total_count += c
            remaining_heads.pop(h)

    dev = [l for l in data if l[0] in dev_selected_heads.keys()]

    dev_test_heads = set(list(dev_selected_heads.keys()) + list(test_selected_heads.keys()))
    train = [l for l in data if l[0] not in dev_test_heads]

    return train, dev, test


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]