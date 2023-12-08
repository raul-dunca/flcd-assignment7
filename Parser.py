from ParserOutput import ParserOutput


class Parser:
    def __init__(self, s,i,w_st,in_st,gr,w,id_sym_tbl,const_sym_tbl):
        self.state=s
        self.position=i             #position of current symbol in input sequence
        self.working_stack=w_st
        self.input_stack= in_st
        self.grammar=gr
        self.sequence=w
        self.id_symbol_table=id_sym_tbl
        self.const_sym_table=const_sym_tbl

    def is_identifier(self,id):
        return  self.id_symbol_table.lookup(id)

    def is_const(self,c):
        return  self.const_sym_table.lookup(c)

    def parse(self):
        while self.state!='f' and self.state!='e':
            if self.state=='q':
                if (self.position==len(self.sequence)+1) and len(self.input_stack)<=0:
                    self.succes()
                else:
                    if (len(self.input_stack)>0  and (self.input_stack[len(self.input_stack)-1] in self.grammar.non_terminals)):
                        self.expand()
                    elif ( len(self.input_stack)>0 and self.position-1<len(self.sequence) and((self.input_stack[len(self.input_stack)-1]==self.sequence[self.position-1]) or (self.is_identifier(self.sequence[self.position-1])) or (self.is_const(self.sequence[self.position-1])))):
                        self.advance()
                    else:
                        self.momentary_insuccess()
            else:
                if self.state=='b' and len(self.working_stack)>0 :
                    if (self.working_stack[len(self.working_stack)-1] in self.grammar.terminals):
                        self.back()
                    else:
                        self.another_try()
        if self.state=='e':
            print("Error! :(")
            print(self.working_stack)
            print(self.input_stack)
        else:
            print("Sequence accepted !")
            print(self.working_stack)
            print(self.input_stack)


    def advance(self):
        self.position += 1
        terminal = self.input_stack.pop()
        self.working_stack.append(terminal)

    def momentary_insuccess(self):
        self.state = 'b'

    def expand(self):
        non_terminal = self.input_stack.pop()

        if non_terminal in self.grammar.productions:
            prod = self.grammar.productions[non_terminal][0]
            prod_nr = 1

            self.working_stack.append((non_terminal, prod_nr))
            for i in range(len(prod) - 1, -1, -1):
                self.input_stack.append(prod[i])

    def back(self):
        self.position-=1
        terminal=self.working_stack.pop()
        self.input_stack.append(terminal)

    def another_try(self):
        pair = self.working_stack.pop()
        non_terminal = pair[0]
        prod_nr = int(pair[1])
        index=prod_nr-1                                            #indexu in lista incepe de la 0 deci prod_nr-1
        if prod_nr<len(self.grammar.productions[non_terminal]):    #exista productie deci o folosim pe aia
            self.state='q'
            self.working_stack.append((non_terminal,prod_nr+1))
            for i in range(len(self.grammar.productions[non_terminal][index])):                     #scoate din input stack vechea productie
                if self.grammar.productions[non_terminal][index][i]==self.input_stack[len(self.input_stack)-1]:  #ifu nu ii necesar e just in case
                    self.input_stack.pop()
            for i in range(len(self.grammar.productions[non_terminal][index+1])-1,-1,-1):           #si o punem pe aia noua in ordine inversa
                    self.input_stack.append(self.grammar.productions[non_terminal][index+1][i])
        elif self.position==1 and self.grammar.starting_point==non_terminal:
            for i in range(
                    len(self.grammar.productions[non_terminal][index])):                            # scoate din input stack vechea productie
                if self.grammar.productions[non_terminal][index][i] == self.input_stack[len(self.input_stack) - 1]:  #ifu nu ii necesar e just in case
                    self.input_stack.pop()
            self.state='e'
        else:
            for i in range(len(self.grammar.productions[non_terminal][index])):                     #scoate din input stack vechea productie
                if self.grammar.productions[non_terminal][index][i]==self.input_stack[len(self.input_stack)-1]:
                    self.input_stack.pop()
            self.input_stack.append(non_terminal)                                                   #si adaugam non terminalu

    def succes(self):
        self.state='f'
