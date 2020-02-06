#
#
import math

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
    
    def make(self, data, propertyIndex, targetIndex, idIndex=None, query='SimpleReg'):
#         if idIndex != None :
#             tuples = zip([rec[idIndex] for rec in data], [ rec[propertyIndex] for rec in data], [ rec[targetIndex] for rec in data])
#         else:
        
        if idIndex == None: 
            tuples = zip(list(range(1,len(data)+1)), [ rec[propertyIndex] for rec in data], [ rec[targetIndex] for rec in data])
        else:
            tuples = zip([rec[idIndex] for rec in data], [ rec[propertyIndex] for rec in data], [ rec[targetIndex] for rec in data])
        if query == 'SimpleReg' :
            words = set()
            targets = set()
            dataset = list()
            for (index, a_line, a_target) in tuples:
                if len(a_line) == 0 :
                    continue
                dataset.append( (index, a_line, a_target) )
                targets.add(a_target)
                for i in range(0, len(a_line)) :
                    for j in range(i+1, len(a_line)) :
                        words.add(a_line[i:j])
            print(words)
            print(targets)
            best = 0
            bestword = ''
            for a_word in words:
                cnt = 0
                val = self.info_gain(self.classify(a_word, dataset, query))
                if best < cnt or (best == cnt and len(bestword) < len(a_word) ):
                    best = cnt
                    bestword = a_word
            return (bestword, best)
        else:
            return
        
    def classify(self, labelobj, dataset, query):
        if query =='SimpleReg' :
            res = dict()
            for (index, a_line, target) in dataset: 
                if (labelobj in a_line) not in res:
                    res[(labelobj in a_line)] = dict()
                if target not in res[(labelobj in a_line)]:
                    res[(labelobj in a_line)][target] = set()
                res[(labelobj in a_line)][target].add(index)
        return res
    
    def info_gain(self, results):
        number_answers = len(results.keys())
        sum = 0
        for an_answer in results.keys():
            subsum = 0
            for a_decided in results[an_answer].keys():
                subsum += len(results[an_answer][a_decided]) 
            number_keys = len(results[an_answer].keys())
            subinfo = 0
            print(an_answer, results[an_answer])
            if number_keys != 0 and subsum != 0 :
                for a_decided in results[an_answer].keys():
                    subinfo += math.log(len(results[an_answer][a_decided])/subsum, number_keys)
            sum += subsum
        return sum
            
    def is_empty(self):
        return self.label == None

db = list()
with open('./sampletext.csv') as dbfile:
    for a_record in [ a_line.strip().split() for a_line in dbfile.readlines()]:
        db.append([ an_item.strip() for an_item in a_record])
#db_pos = ''.split('\n')
#db_neg = ''.split('\n')
dtree = DecisionTree(None)
print(dtree)
print(dtree.make(db, 0, 1) )
