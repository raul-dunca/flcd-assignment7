
class Row:
    def __init__(self,i,inf,par,rsib):
        self.index=i
        self.info=inf
        self.parent=par
        self.right_sibling=rsib

    def __str__(self):
        return f"Index: {self.index} Info: {self.info} Parent: {self.parent} Right Sibling: {self.right_sibling}"


class ParserOutput:
    def __init__(self, pars_tree, gr):
        self.parsing_tree=pars_tree
        self.table=[]
        self.grammar=gr

    def tranform(self):
        idx=1
        parents=[]
        right_sibling=0
        for i in range(len(self.parsing_tree)):
            if self.parsing_tree[i] not in self.grammar.terminals:
                non_terminal=self.parsing_tree[i][0]
                prod_nr=self.parsing_tree[i][1]-1
                if idx==1:
                    self.table.append(Row(idx,non_terminal,0,right_sibling))
                    parents.append(idx)
                    idx+=1
                right_sibling = 0

                parent = parents.pop(0)
                for item in self.grammar.productions[non_terminal][prod_nr]:
                    self.table.append(Row(idx, item, parent, right_sibling))
                    right_sibling = idx
                    if item not in self.grammar.terminals:
                        parents.append(idx)
                    idx += 1


    def print(self):
        for i in range(len(self.table)):
            print(str(self.table[i]))

    def write_to_file(self, file_name):
        with open(file_name, 'w') as file:
            for row in self.table:
                file.write(str(row) + '\n')