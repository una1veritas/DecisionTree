#
#
class DecisionTree:
    label = None
    children = None
    
    def __init__(self, labelobj):
        self.label = labelobj
        self.children = dict()
    
    def __str__(self):
        if self.is_empty() :
            ostr = 'DecisionTree'
        else:
            ostr = str(self.label)
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
    
    def make(self, data, query='SimpleReg'):
        if query == 'SimpleReg' :
            words = set()
            for a_line in data:
                if len(a_line) == 0 :
                    continue
                for i in range(0, len(a_line)) :
                    for j in range(i+1, len(a_line)) :
                        words.add(a_line[i:j])
            print(words)
            best = 0
            bestword = ''
            for a_word in words:
                cnt = 0
                for a_line in data :
                    if a_word in a_line :
                        cnt += 1
                if best < cnt or (best == cnt and len(bestword) < len(a_word) ):
                    best = cnt
                    bestword = a_word
            return (bestword, best)
        else:
            return
        
    def is_empty(self):
        return self.label == None

with open('../会話が不自由な入院患者のやりとり事例/医療データセット.txt') as dbfile:
    db = dbfile.readlines()
#print(db)
#db_pos = ''.split('\n')
#db_neg = ''.split('\n')
dtree = DecisionTree(None)
print(dtree)
print(dtree.make(db))
