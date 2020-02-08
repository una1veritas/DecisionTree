#
#
import math

class DecisionTree:
    label = None
    children = None
    
    def __init__(self, data, propIndex, targetIndex):
        target_classes = [d[targetIndex] for d in data]
        if len( set(target_classes) ) == 1 :
            self.label = target_classes[0]
            return
        (word, decisions) = self.choose_simpleregx(data, propIndex, targetIndex)
        self.label = word
        self.children = dict()
        for key in decisions :
            self.children[key] = DecisionTree(decisions[key], propIndex, targetIndex)
        return
        
    def __str__(self):
        if self.is_empty() :
            ostr = 'DecisionTree'
        else:
            ostr = str(self.label)
        if self.is_leaf() or len(self.children) == 0 :
            return ostr
        ostr += '('
        is_first_elem = True
        for key, val in sorted(self.children.items()):
            if not is_first_elem :
                ostr += ', '
            ostr += str(key) + '-> ' + val.__str__()
            is_first_elem = False
#         path = [self]
#         while len(path):
#             for a in sorted(path[-1].children.keys()):
#                 ostr += path[-1].children[a].__str__() + ', '
#             path.pop(-1)
        ostr += ')'
        return ostr
    
    def choose_simpleregx(self, data, propertyIndex, targetIndex):
        words = set()
        dataset = list()
        target_classes = set()
        for (a_line, a_target) in zip([ rec[propertyIndex] for rec in data], [ rec[targetIndex] for rec in data]):
            if len(a_line) == 0 :
                continue
            dataset.append( (a_line, a_target) )
            target_classes.add(a_target)
            for a_word in [ a_line[i:j] for i in range(0, len(a_line)) for j in range(i+1, len(a_line))]:
                words.add(a_word)
        #print(words)
        #print(targets)
        if len(target_classes) == 1 :
            print('choose_simpleregx: error, "Already uniquely classified."')
            return ('', None)
        (bestword, bestgain, bestdecision) = ('', 0, None)
        for a_word in words:
            #print(a_word)
            decision = self.classify_simpleregx(a_word, dataset)
            val = self.info_gain(decision)
            #print(decision)
            if bestgain < val or (bestgain == val and len(bestword) < len(a_word) ):
                bestgain = val
                bestword = a_word
                bestdecision = decision
            #print('-----')
        print(bestword, bestdecision)
        return (bestword, bestdecision)
        
    def classify_simpleregx(self, labelobj, dataset):
        res = dict()
        for tuple in dataset: # (a_line, target)
            #print(tuple)
            ans = labelobj in tuple[0]
            if ans not in res:
                res[ans] = list()
            res[ans].append( tuple )
        return res
    
    def info_gain(self, results):
        total = sum([ len(val) for key, val in results.items()])
        info = 0
        for ans, ans_group in results.items():
            #print(ans, results[ans])
            ans_entropy = 0
            for a_class in set([ t[-1] for t in ans_group]):
                prob = len([t for t in ans_group if t[-1] == a_class])/len(ans_group) if len(ans_group) > 0 else 0
                ans_entropy +=  - prob * math.log(prob) if prob > 0 else 0 
            #print(ans_entropy)
            total += len(ans_group)
            info += len(ans_group)/total * ans_entropy
        info = info
        #print(info, 1 - info)
        return 1 - info
    
    def is_leaf(self):
        return self.children == None
    
    def is_empty(self):
        return self.label == None

db = list()
with open('./kranke.csv') as dbfile:
    for a_record in [ a_line.strip().split(',') for a_line in dbfile.readlines()]:
        db.append([ an_item.strip() for an_item in a_record])
#db_pos = ''.split('\n')
#db_neg = ''.split('\n')
print(db)
dtree = DecisionTree(db, 0, 1)
print('\nResult: ')
print(dtree)
