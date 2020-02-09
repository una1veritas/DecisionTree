#
#
import math
#import MeCab

class DecisionTree:
    label = None
    children = None
    
    def __init__(self, labelObj=None, childs=None):
        self.label = labelObj
        self.children = childs
    
    def makeDecisionTree(self, database, selections, testColumn, targetColumn, queryType='simpleregex'):
        if self.data_is_pure(database, selections, targetColumn) :
            self.label = database[selections[0]][targetColumn]
            self.children = None
            return
        #print(selections, testColumn, targetColumn)
        if queryType == 'simpleregex' :
            wordset = self.collect_substrings(database, selections, testColumn)
            (word, decisions) = self.choose_substring(database, selections, wordset, testColumn, targetColumn)
            self.label = word
        elif queryType == 'analyzedword' :
            print('error: type \''+str(queryType)+'\' is still not supported.')
            return
        else: 
            print('error: type \''+str(queryType)+'\' is still not supported.')
            return
        self.children = dict()
        print(decisions)
        for key in decisions :
            self.children[key] = DecisionTree()
            self.children[key].makeDecisionTree(database, decisions[key], testColumn, targetColumn, queryType)
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
    
    def data_is_pure(self, database, indices, targetColumn):
        target_classes = set()
        for idx in indices:
            target_classes.add(database[idx][targetColumn])
        return len(target_classes) == 1
    
    def collect_substrings(self, databases, selections, textIndex):
        words = set()
        for idx in selections:
            a_line = databases[idx][textIndex]
            if len(a_line) == 0 :
                continue
            for a_word in [ a_line[i:j] for i in range(0, len(a_line)) for j in range(i+1, len(a_line))]:
                words.add(a_word)
        return words
        
    def choose_substring(self, database, selections, words, textColumn, targetColumn):
        #if len(target_classes) == 1 :
        #    print('choose_simpleregx: error, "Already uniquely classified."')
        #    return ('', None)
        (bestword, bestgain, bestdecision) = ('', 0, None)
        for a_word in words:
            decision = self.classify_simpleregx(a_word, database, selections, textColumn, targetColumn)
            val = self.info_gain(database, decision, targetColumn)
            #print(a_word, val, decision)
            if bestgain < val or (bestgain == val and len(bestword) < len(a_word) ):
                bestgain = val
                bestword = a_word
                bestdecision = decision
            #print('-----')
        #print(bestword, bestdecision)
        return (bestword, bestdecision)
        
    def classify_simpleregx(self, labelobj, database, selections, testColumn, targetColumn):
        res = dict()
        for idx in selections:
            ans = labelobj in database[idx][testColumn]
            #print(labelobj, ans, rec[propertyIndex], rec[targetIndex])
            if ans not in res:
                res[ans] = list()
            res[ans].append( idx )
        return res
    
    def info_gain(self, database, decisions, targetColumn):
        total = sum([ len(val) for key, val in decisions.items()])
        info = 0
        for a_decision, selections in decisions.items():
            decision_entropy = 0
            target_class = set([ database[idx][targetColumn] for idx in selections])
            for a_class in target_class:
                prob = len([idx for idx in selections if database[idx][targetColumn] == a_class])/len(selections) if len(selections) > 0 else 0
                decision_entropy +=  - prob * math.log(prob) if prob > 0 else 0 
            #print(ans_entropy)
            total += len(selections)
            info += len(selections) * decision_entropy
        info = info/total
        #print(info, 1 - info)
        return 1 - info
    
    def is_leaf(self):
        return self.children == None
    
    def is_empty(self):
        return self.label == None

    def collect_graphdefs(self, nodes, edges):
        nodes.append(self.label)
        for key, value in self.children.items():
            edges.append( (self.label, value.label, key) )
        for a_child in self.children.values() :
            if not a_child.is_leaf() :
                a_child.collect_graphdefs(nodes, edges)
        return (nodes, edges)

    def dot_script(self):
        header = """digraph graph_name {
  graph [
    charset = "UTF-8";
    label = "sample graph",
    labelloc = "t",
    labeljust = "c",
    bgcolor = "#343434",
    fontcolor = white,
    fontsize = 18,
    style = "filled",
    rankdir = TB,
    margin = 0.2,
    splines = spline,
    ranksep = 1.0,
    nodesep = 0.9
  ];

  node [
    colorscheme = "rdylgn11"
    style = "solid,filled",
    fontsize = 16,
    fontcolor = 6,
    fontname = "Migu 1M",
    color = 7,
    fillcolor = 11,
    fixedsize = true,
    height = 0.6,
    width = 1.2
  ];

  edge [
    style = solid,
    fontsize = 14,
    fontcolor = white,
    fontname = "Migu 1M",
    color = white,
    labelfloat = true,
    labeldistance = 2.5,
    labelangle = 70
  ];
"""
        footer = ' }'
        
        nodes = list()
        edges = list()
        self.collect_graphdefs(nodes, edges)
        nodestr = '  // node definitions\n'
        for a_node in nodes :
            nodestr += '  ' + str(a_node) + ' [shape = box];\n'
        edgestr = '  // edge definitions\n'
        for an_edge in edges :
            edgestr += '  ' + str(an_edge[0]) + ' -> ' + str(an_edge[1]) + ' [label = "{}", arrowhead = normal];\n'.format(an_edge[2])
        return header+nodestr+edgestr+footer


#program begins

db = list()
idx = 0
with open('./kranke.csv') as dbfile:
    for a_record in [ a_line.strip().split(',') for a_line in dbfile.readlines()]:
        if len(a_record) == 0:
            continue
        db.append(tuple([idx]+[ an_item.strip() for an_item in a_record]))
        idx += 1
#db_pos = ''.split('\n')
#db_neg = ''.split('\n')
print(db)
dtree = DecisionTree()
dtree.makeDecisionTree(db, range(0, len(db)), 1, 2, 'simpleregex')
print('\nResult: ')
print(dtree)
print(dtree.dot_script())
