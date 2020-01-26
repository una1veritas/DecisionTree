
import sys

class SuffixTree:
    labelstr = ''
    children = dict()
    
    def __init__(self, astr):
        self.labelstr = astr
        
    def __str__(self):
        ostr = self.label() + '('
        for ea in self.children:
            ostr += ea
            ostr += ', '
        ostr += ')'
        return ostr
    
    def label(self):
        return self.labelstr
        
    def append(self, astr):
        return self.find(self, astr)
        
    def find(self, node, astr):
        if len(astr) == 0:
    #         if not '' in node:
    #             node[''] = ''
    #         return node[''] 
            return
        if astr[0] in node.children:
            node = astr[0]
            lstr = node.label()
            length = 0
            for a, l in zip(astr, lstr):
                if a != l :
                    break
                length += 1
            if length == len(lstr):
                return node
            else:
                newnode = dict()
                newnode[lstr[length]] = [lstr[length:], node]
                node[lstr[0]] = [lstr[0:length], newnode]
                anothernewnode = dict()
                newnode[astr[length]] = [astr[length:], anothernewnode]
                self.find(newnode, astr[length:])
            return
        else:
            node.children[astr[0]] = SuffixTree(astr)
            return
        
print(sys.argv)

stree = SuffixTree('')

with open(sys.argv[1]) as textfile:
    lnum = 0
    for tline in textfile:
        tline = tline.strip()
        if len(tline) != 0:
            for i in range(0,len(tline) - 1):
                s = tline[i:]
                print(s, (lnum, i) )
                stree.append(s)
                print(stree)
        lnum += 1
        if lnum > 3:
            break

print(stree)