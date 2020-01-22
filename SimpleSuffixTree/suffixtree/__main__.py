
import sys

def suffixtree_root():
    return { '':[''] }
    
def suffixtree_find(node, astr):
    while (astr[0] in node):
        node = node[astr[0]]
        node[0].
        astr = astr[1:]
    return (node, astr)
    
def suffixtree_add(node, astr):
    (node, astr) = suffixtree_find(node, astr)
    node[astr[0]] = [astr]

print(sys.argv)

suftree = suffixtree_root()

with open(sys.argv[1]) as textfile:
    lnum = 0
    for tline in textfile:
        tline = tline.strip()
        if len(tline) != 0:
            for i in range(0,len(tline) - 1):
                s = tline[i:]
                print(s, (lnum, i) )
                suffixtree_add(suftree,s)
                print(suftree)
        lnum += 1