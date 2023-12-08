from FA import FiniteAutomata
from HashTable import MyHashTable
from Grammar import Grammar
from Parser import Parser
import copy

from ParserOutput import ParserOutput


def test_hash_tbl():
    m=MyHashTable(10)
    n=MyHashTable(50)
    m.add("a")
    m.add("a")
    m.add("b")
    m.add("c")
    m.add("d")

    for i in range(100):
        n.add(i)

    assert m.lookup("a") == True
    assert m.lookup(2) == False

    assert n.lookup("c") == False
    assert n.lookup(95) == True
    assert n.lookup(102) == False


def test_int(fa):

    assert fa.is_accepted("2190") == True
    assert fa.is_accepted("-101") == True
    assert fa.is_accepted("-01") == False
    assert fa.is_accepted("-1") == True
    assert fa.is_accepted("6443198310-") == False
    assert fa.is_accepted("0") == True
    assert fa.is_accepted("02") == False

def test_identifier(fa):

    assert fa.is_accepted("array_List") == True
    assert fa.is_accepted("pongBall") == True
    assert fa.is_accepted("Class") == False
    assert fa.is_accepted("02an") == False
    assert fa.is_accepted("a1") == True
    assert fa.is_accepted("_cnt") == False
    assert fa.is_accepted("f1_A") == True


def test_parser_actions():

    terminals=set()
    terminals.add("a")
    terminals.add("b")
    terminals.add("c")
    non_terminals=set()
    non_terminals.add("S")
    prod=dict()
    prod["S"]=[["a","S","b","S"],["a","S"],["c"]]
    g=Grammar(terminals,non_terminals,"S",prod)

    test = Parser('q', 1, [], ["S"], g ,"acbc",identifiers_sym_tbl,consts_sym_tbl)
    test.parse()
    #print("PO:")
    #po = ParserOutput(test.working_stack, g)
    #po.tranform()
    #po.print()
    p1=Parser('q',6,[("S",1),"a",("S",2),"a",("S",3),"c","b",("S",3),"c"],[],g,"aacbc",identifiers_sym_tbl,consts_sym_tbl)

    succes_test=copy.deepcopy(p1)
    succes_test.succes()
    assert p1.state !='f'
    assert succes_test.state =='f'
    assert p1.position==succes_test.position
    assert p1.input_stack==succes_test.input_stack
    assert p1.working_stack==succes_test.working_stack


    p2 = Parser('b', 6, [("S", 1), "a", ("S", 1), "a", ("S", 3), "c", "b", ("S", 3), "c"], ["S","b"], g, "aacbc",identifiers_sym_tbl,consts_sym_tbl)
    back_test = copy.deepcopy(p2)
    back_test.back()
    assert back_test.state == 'b'
    assert p2.state == 'b'
    assert p2.position - 1 == back_test.position
    assert back_test.working_stack == [("S", 1), "a", ("S", 1), "a", ("S", 3), "c", "b", ("S", 3)]
    assert back_test.input_stack == ["S","b","c"]


    p3 = Parser('b', 3, [("S", 1), "a", ("S", 1), "a", ("S", 1)], ["S","b","S","b","S","b","S","a"], g, "aacbc",identifiers_sym_tbl,consts_sym_tbl)
    another_try1 = copy.deepcopy(p3)
    another_try1.another_try()
    assert another_try1.state == 'q'
    assert p3.state == 'b'
    assert p3.position == another_try1.position
    assert another_try1.working_stack == [("S", 1), "a", ("S", 1), "a", ("S", 2)]
    assert another_try1.input_stack ==  ["S", "b","S","b","S","a"]

    p4= Parser('b', 1, [("S", 3)], ["c"], g, "cc",identifiers_sym_tbl,consts_sym_tbl)
    another_try2 = copy.deepcopy(p4)
    another_try2.another_try()
    assert another_try2.state == 'e'
    assert p4.state == 'b'
    assert p4.position == another_try2.position
    assert another_try2.working_stack == []
    assert another_try2.input_stack ==  []

    p5 = Parser('b', 5, [("S", 1),"a",("S",1),"a",("S",3),"c","b",("S",3)], ["S","b","c"], g, "aacbc",identifiers_sym_tbl,consts_sym_tbl)
    another_try3 = copy.deepcopy(p5)
    another_try3.another_try()
    assert another_try3.state == 'b'
    assert p5.state == 'b'
    assert p5.position == another_try3.position
    assert another_try3.working_stack == [("S", 1),"a",("S",1),"a",("S",3),"c","b"]
    assert another_try3.input_stack == ["S","b","S"]


    terminals = set()
    terminals.add("a")
    terminals.add("b")
    terminals.add("c")
    non_terminals = set()
    non_terminals.add("S")
    prod = dict()
    prod["S"] = [["a","S","b","S"], ["a","S"], ["c"]]
    g = Grammar(terminals, non_terminals, ["S"], prod)

    p1 = Parser('q', 6, [("S", 1), "a", ("S", 1), "a", ("S", 3), "c", "b", ("S", 3), "c"], ["S", "b"], g, "aacbc",identifiers_sym_tbl,consts_sym_tbl)
    p1.advance()

    assert p1.state == 'q'
    assert p1.position == 7
    assert p1.working_stack == [("S", 1), "a", ("S", 1), "a", ("S", 3), "c", "b", ("S", 3), "c", "b"]
    assert p1.input_stack == ["S"]

    p1.momentary_insuccess()
    assert p1.state == 'b'
    assert p1.position == 7
    assert p1.working_stack == [("S", 1), "a", ("S", 1), "a", ("S", 3), "c", "b", ("S", 3), "c", "b"]
    assert p1.input_stack == ["S"]

    #p2 = Parser('q', 6, [("S", 1), "a", ("S", 1), "a", ("S", 3), "c", "b", ("S", 3), "c"], ["aSbS", "aS", "c"], g,
    #            "aacbc")
    #p2.expand()
    #assert p2.state == 'q'
    #assert p2.position == 6
    #assert p2.working_stack == [('S', 1), 'a', ('S', 1), 'a', ('S', 3), 'c', 'b', ('S', 3), 'c', ('S', 3)]
    #assert p2.input_stack == [prod['S'][0][::-1]]


def read_fa(file_path):
    with open(file_path, 'r') as file:
        content = file.read().split('\n')

    states = content[0].split(': ')[1].split()
    alphabet = content[1].split(': ')[1].split()
    initial = content[2].split(': ')[1]
    final = set(content[3].split(': ')[1].split())
    transitions = [line.split() for line in content[4:] if line.strip() and line != 'transitions:']

    transitions_dict = {}
    for transition in transitions:
        from_state, symbol, to_state = transition
        if (from_state,to_state) not in transitions_dict:
            transitions_dict[(from_state,to_state)] = set()
        transitions_dict[(from_state,to_state)].add(symbol)

    fa=FiniteAutomata(states, alphabet, transitions_dict, initial,final)

    while True:
        print("Select one:")
        print("1) Print the FA states")
        print("2) Print the FA alphabet")
        print("3) Print the FA transitions")
        print("4) Print the FA initial state")
        print("5) Print the FA final states")
        print("0) Continue")
        n=input()
        if n=="0":
            break
        else:
            fa.print(n)
    if file_path=="FA2.in":
        test_int(fa)
    elif file_path=="FA.in":
        test_identifier(fa)
    return fa

def validate_cfg(gr):
    for non_terminal in gr.non_terminals:
        if non_terminal not in gr.productions:
            return False
    return True
def read_grammar(file_path):
    with open(file_path, 'r') as file:
        content = file.read().split('\n')

    non_terminals = set(content[0].split(': ')[1].split())
    terminals = set(content[1].split(': ')[1].split())
    terminals.add('\n')
    terminals.add('\t')
    terminals.add(' ')
    starting_point = content[2].split(': ')[1]

    grammar_dict = {}
    for line in content[4:]:
        if line:
            key, value = line.split(' -> ')
            if key not in grammar_dict:
                groups = value.split(' | ')
                grammar_dict[key] = [group.split() for group in groups]
            else:
                grammar_dict[key].extend(value.split(' | '))

    gr = Grammar(terminals, non_terminals, starting_point, grammar_dict)
    if validate_cfg(gr):
        while True:
            print("Select one:")
            print("1) Print the Grammar terminals")
            print("2) Print the Grammar non-terminals")
            print("3) Print the Grammar starting point")
            print("4) Print the Grammar productions")
            print("5) Print productions for a given non-terminal")
            print("0) Continue")
            n=input()
            if n=="0":
                break
            else:
                gr.print(n)
        return gr
    else:
        print("Not a CFG grammar!!!")

test_hash_tbl()
identifiers_sym_tbl = MyHashTable(10)
consts_sym_tbl = MyHashTable(20)
PIF = []
tokens=[]
separators=[]
operators=[]

with open("token.in", 'r') as file:
    for line in file:
        tokens.append(line.replace('\n',''))

separators=tokens[17:27]
separators.append('\n')
separators.append('\t')

operators=tokens[2:17]
print("\n")
file_path = input("Enter the file name (e.g., a.txt):")

glb_error=False
line_cntr=0

fa_id=read_fa('FA.in')
fa_int=read_fa('FA2.in')
gr=read_grammar('g2.txt')
program=[]
with open(file_path, 'r') as file:
    for line in file:
        line_cntr+=1
        token=""
        ok=True
        for i in line:
            if i=='"':
                if ok==False:       # we found the closing "
                    token+='"'
                    consts_sym_tbl.add(token)
                    PIF.append(("const",(consts_sym_tbl.hash_fct(token),consts_sym_tbl.get_poz(token))))
                    program.append(token)                                              #!
                    #print(token+" is a string const!")
                    token=""
                ok=not ok
            if ok==False:
                token+=i
                continue
            if i in separators or i in operators:
                if token not in tokens and token !="":

                    if fa_int.is_accepted(token):
                        consts_sym_tbl.add(token)
                        PIF.append(("const", (consts_sym_tbl.hash_fct(token), consts_sym_tbl.get_poz(token))))
                        program.append(token)                           #!
                        if i != ' ' and i != '\n' and i != '\t':
                            PIF.append((tokens.index(i), -1))
                            program.append(i)
                    elif fa_id.is_accepted(token):
                        identifiers_sym_tbl.add(token)
                        PIF.append(("id", (identifiers_sym_tbl.hash_fct(token), identifiers_sym_tbl.get_poz(token))))
                        program.append(token)                                   #!
                        if i != ' ' and i != '\n' and i != '\t':
                            PIF.append((tokens.index(i), -1))
                            program.append(i)                                   #!
                    else:
                        print(token + " is undefined; On line: " + str(line_cntr))
                        glb_error = True
                else:
                    if token !="":
                        PIF.append((tokens.index(token), -1))
                        program.append(token)                                   #!
                    if i != ' ' and i != '\n' and i != '\t' and i!='"':
                        if not isinstance(PIF[len(PIF)-1][0],str):
                            op=tokens[PIF[len(PIF)-1][0]]+i
                            if tokens[PIF[len(PIF)-1][0]] in operators and i in operators and op in operators:
                                PIF.pop()
                                PIF.append((tokens.index(op),-1))
                                program.pop()                                   #!
                                program.append(op)                              #!
                            else:
                                PIF.append((tokens.index(i), -1))
                                program.append(i)                               #!
                        else:
                            PIF.append((tokens.index(i), -1))
                            program.append(i)                                   #!
                token = ""
            else:
                token+=i

        if ok==False:
            print("You forgot to close the \" on line " +str(line_cntr))
            glb_error=True


    if not glb_error:
        print("Program is lexically correct!")
        with open('ST.out', 'w') as file:
            file.write("The data structure used for the ST is hashmap.\n\n")
            file.write("Identifier Symbol Table.\n")
            file.write(str(identifiers_sym_tbl))
            file.write("\n")
            file.write("Constants Symbol Table.\n")
            file.write(str(consts_sym_tbl))

        with open('PIF.out', 'w') as file:
            for pair in PIF:
                file.write(str(pair)+ "\n")
        parser = Parser('q', 1, [], [gr.starting_point], gr,program,identifiers_sym_tbl,consts_sym_tbl)
        print(program)
        #test_parser_actions()
        parser.parse()

        print("PO:")
        po = ParserOutput(parser.working_stack, gr)
        po.tranform()
        po.print()
        po.write_to_file("out1.txt")
    else:
        with open('ST.out', 'w'):
            pass
        with open('PIF.out', 'w'):
            pass
