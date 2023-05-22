import random
w = open('sample.tsv','w')
f2 =open("train_sample.tsv")
f3=open("test_sample.tsv")

l=[]
ll=[]
for i in f2.readlines():
    l.append(i.strip('\n'))
    ll.append(i.split('\t')[1])

ss=[]
for i in f3.readlines():
    ss.append(i.strip('\n').split('	')[1])



rel_set=[]
lines =f.readlines()
random.shuffle(lines)
print(lines[0])
for line in lines:
    head,rel,tail=line.strip('\n').split('\t')
    # print(rel)
    if rel not in rel_set:
        rel_set.append(rel)
        s=ss[ll.index(rel)].split('	')[-1]
        sh=l[ll.index(rel)].split('\t')[0]
        w.write(line)
        w.write("predict the tail entity [MASK] from the given ({}, {}, [MASK]) by completing the sentence \"{}\".The answer is {}.\n".format(head,rel,s,tail))
        w.write("predict the tail entity [MASK] from the given ({}, {}, [MASK]) by completing the sentence \"{}\".The answer is \n".format(sh,rel,s))
    
print(len(rel_set))


