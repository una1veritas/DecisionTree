import sys

class SuffixTree:
    label = ''
    children = None
    
    def __init__(self, labelstr):
        self.label = labelstr
        self.children = dict()
    
    def __str__(self):
        if self.is_root() :
            ostr = 'SuffixTree'
        else:
            ostr = self.label
        if not self.children :
            ostr += '()'
            return ostr
        ostr += '('
        for key, val in sorted(self.children.items()):
            ostr += val.__str__() + ', '
#         path = [self]
#         while len(path):
#             for a in sorted(path[-1].children.keys()):
#                 ostr += path[-1].children[a].__str__() + ', '
#             path.pop(-1)
        ostr += ')'
        return ostr
    def is_root(self):
        return self.label == ''
    
    def append(self, sstr):
        if len(sstr) == 0 :
            return self
        if not sstr[0] in self.children:
            self.children[sstr[0]] = SuffixTree(sstr)
            return self.children[sstr[0]]
        else:
            achild = self.children[sstr[0]]
            matchlen = 0
            for a, c in zip(achild.label, sstr):
                if a != c :
                    break
                matchlen += 1
            if matchlen == len(achild.label):
                if self.label == sstr:
                    return achild
                else:
                    return achild.append(sstr[matchlen:])
            if matchlen < len(achild.label):
                #print(matchlen, achild.label, sstr)
                internode = SuffixTree(achild.label[:matchlen])
                achild.label = achild.label[matchlen:]
                internode.children[achild.label[0]] = achild
                self.children[sstr[0]] = internode                
                if matchlen < len(sstr) :
                    newnode = SuffixTree(sstr[matchlen:])
                    internode.children[sstr[matchlen]] = newnode
                    return newnode
                return internode
    
stree = SuffixTree('')
print(stree)

print(sys.argv)
fname = sys.argv[1]
with open(fname) as txtdata:
    for a_line in txtdata:
        a_line = a_line.strip()
        if not len(a_line):
            continue
        print(a_line)
        for i in range(0, len(a_line)):
            #print(a_line[i:])
            stree.append(a_line[i:])

print(stree)
