import ply.lex as lex
import ply.yacc as yacc


reserved = {
    'and' : 'AND_SYM',
    'array' : 'ARRAY_SYM',
    'begin' : 'BEGIN_SYM',
    'case' : 'CASE_SYM',
    'const' : 'CONST_SYM',
    'div' : 'DIV_SYM',
    'do' : 'DO_SYM',
    'downto' : 'DOWNTO_SYM',
    'else' : 'ELSE_SYM',
    'end' : 'END_SYM',
    'for' : 'FOR_SYM',
    'function' : 'FUNCTION_SYM',
    'if' : 'IF_SYM',
    'mod' : 'MOD_SYM',
    'not' : 'NOT_SYM',
    'of' : 'OF_SYM',
    'or': 'OR_SYM',
    'procedure' : 'PROCEDURE_SYM',
    'program' : 'PROGRAM_SYM',
    'record' : 'RECORD_SYM',
    'repeat' : 'REPEAT_SYM',
    'then' : 'THEN_SYM',
    'to' : 'TO_SYM',
    'type' : 'TYPE_SYM',
    'until' : 'UNTIL_SYM',
    'var' : 'VAR_SYM',
    'while' : 'WHILE_SYM',
    'char' : 'CHAR_SYM',
    'integer' : 'INTEGER_SYM',
    'real' : 'REAL_SYM',
    'boolean' : 'BOOLEAN_SYM',
    'string' : 'STRING_SYM',
}


tokens = [
    'COLON',
    'SEMI_COLON',
    'COMMA',
    'DOT',
    'DOUBLE_DOT',
    'OPER_ADD',
    'OPER_SUB',
    'OPER_MULT',
    'OPER_DIV',
    'EQUAL',
    'NOT_EQUAL',
    'GREATER',
    'GR_EQ',
    'LOWER',
    'LW_EQ',
    'NAWL',
    'NAWR',
    'NAWKL',
    'NAWKR',
    'ASSING_SYM',
    'NUMBER',
    'ID',
    'TEXT',
    'SINGLE_LINE_COMMENT',
    'MULTI_LINE_COMMENT'
] + list(reserved.values())

t_COLON = r':'
t_SEMI_COLON = r';'
t_COMMA = r','
t_DOT= r'\.'
t_DOUBLE_DOT = r'\.\.'
t_OPER_ADD = r'\+'
t_OPER_SUB = r'-'
t_OPER_MULT = r'\*'
t_OPER_DIV = r'/'
t_EQUAL = r'='
t_NOT_EQUAL = r'<>'
t_GREATER = r'>'
t_GR_EQ = r'>='
t_LOWER = r'<'
t_LW_EQ = r'<='
t_NAWL = r'\('
t_NAWR = r'\)'
t_NAWKL = r'\['
t_NAWKR = r'\]'
t_ASSING_SYM = r':='

def t_NUMBER(t):
  r'[0-9][0-9]*'
  t.value = int(t.value)
  return t

def t_ID(t):
  r'[a-zA-Z][a-zA-Z0-9]*'
  t.type = reserved.get(t.value, 'ID')
  return t

def t_TEXT(t):
  r'\'[^\'\n]*\''
  return t

def t_SINGLE_LINE_COMMENT(t):
  r'\(\*[^\*\n]*[^\)\n]*\*\)'
  return t

def t_MULTI_LINE_COMMENT(t):
  r'{[^{}]*}'
  return t

t_ignore = '  \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t) :
    print ("Illegal character {}".format(t.value[0]))
    t.lexer.skip(1)



lexer = lex.lex()
with open('test.txt', 'r') as file:
    data = file.read()
lexer.input(data)
#for token in lexer:
    #print("line %d: %s(%s)" %(token.lineno, token.type, token.value))

id_list=[]
type1=""

def p_pascal_program(p):
    'pascal_program : pogram_header SEMI_COLON block DOT'
    pass
def p_program_header(p):
    'pogram_header : PROGRAM_SYM ID'
    print("//Program: "+p[2])
    print("include <stdio.h>")
    print("include <stdbool.h>")
def p_block(p):
    'block : const_block type_block var_block'# procedure_and_function_block operation_block'
    pass
def p_const_block(p):
    '''const_block : CONST_SYM const_def SEMI_COLON const_def_list
                    | empty'''

def p_const_def_list(p):
    '''const_def_list : const_def_list const_def SEMI_COLON
                      | empty'''
    pass
def p_const_def(p):
    'const_def : constid EQUAL const_value'
    print()
def p_constid(p):
    'constid : ID'
    print("#define "+p[1]+" ",end=" ")
def p_id(p):
    'id : ID'
    print(p[1],end="")
def p_const_value(p):
    '''const_value : ID
                    | sign id
                    | real_number
                    | sign real_number
                    | TEXT'''
    if p[1]is not None and str(p[1])[0]=='\'':
        x=str(p[1])
        print(x.replace('\'','\"'),end=" ")
    elif p[1]is not None and str(p[1])[0].isalpha():
        print(p[1],end=" ")
def p_sign(p):
    '''sign : OPER_ADD
                    | OPER_SUB'''
    print(p[1],end="")
def p_real_number(p):
    '''real_number : num
                    | num dot num
                    | num e sign num
                    | num dot num e sign num'''
def p_num(p):
    '''num : NUMBER'''
    print(p[1],end="")
def p_dot(p):
    '''dot : DOT'''
    print(p[1],end="")
def p_e(p):
    'e : ID'
    if p[1] !='e':
        print("Syntax error in input!")
    else: print(p[1], end="")




def p_type_block(p):
    '''type_block : TYPE_SYM type_def SEMI_COLON type_def_list
                    | empty'''
    pass
def p_type_def_list(p):
    '''type_def_list : type_def_list type_def SEMI_COLON
                    | empty'''
    print(';')
def p_type_def(p):
    '''type_def : id_list EQUAL type_denoter_td'''
    for i in id_list:
        if i!= id_list[-1]:
            print(i,end=", ")
        else:
            print(i,end="")
    id_list.clear()
def p_type_denoter(p):
    '''type_denoter : type_general
                    | enumerated_type
                    | array_type
                    | record_type
                    | id'''
    pass
def p_type_denoter_td(p):
    '''type_denoter_td : type_general_td
                    | enumerated_type_td
                    | array_type_td
                    | record_type_td'''
    pass
def p_type_general(p):
    '''type_general : CHAR_SYM
                    | INTEGER_SYM
                    | REAL_SYM
                    | BOOLEAN_SYM'''
    if p[1] == 'integer':
        print("int",end=" ")
        type1 ="int"
    elif p[1] == 'real':
        print("double", end=" ")
        type1 ="double"
    elif p[1] == 'char':
        print("char", end=" ")
        type1 ="char"
    elif p[1] == 'boolean':
        print("bool", end=" ")
        type1 = "bool"
def p_type_general_td(p):
    '''type_general_td : CHAR_SYM
                    | INTEGER_SYM
                    | REAL_SYM
                    | BOOLEAN_SYM'''
    if p[1] == 'integer':
        print("typedef int",end=" ")
        type1 ="int"
    elif p[1] == 'real':
        print("typedef double", end=" ")
        type1 ="double"
    elif p[1] == 'char':
        print("typedef char", end=" ")
        type1 ="char"
    elif p[1] == 'boolean':
        print("typedef bool", end=" ")
        type1 = "bool"
def p_enumerated_type(p):
    '''enumerated_type : NAWL id_list NAWR'''
    print("enum "+id_list.pop(0)+" {",end="")
    for i in id_list:
        if i!= id_list[-1]:
            print(i,end=", ")
        else:
            print(i,end="")
    print("}", end="")
    id_list.clear()
def p_enumerated_type_td(p):
    '''enumerated_type_td : NAWL id_list NAWR'''
    print("typedef enum "+" {",end="")
    for i in id_list:
        if i!= id_list[-1]:
            print(i,end=", ")
        else:
            print(i,end="")
    print("}"+id_list.pop(0), end="")
    id_list.clear()
def p_id_list(p):
    '''id_list : ID
                | id_list COMMA ID'''
    if p[1] is not None:
        id_list.append(p[1])
    else: id_list.append(p[3])
def p_array_type(p):
    '''array_type : ARRAY_SYM NAWKL NUMBER DOUBLE_DOT NUMBER NAWKR OF_SYM type_denoter'''
    size= str(int(p[5])-int(p[3]))
    print(type1 + id_list.pop(0) + "["+size+"]",end="")
def p_array_type_td(p):
    '''array_type_td : ARRAY_SYM NAWKL NUMBER DOUBLE_DOT NUMBER NAWKR OF_SYM type_denoter_td'''
    size= str(int(p[5])-int(p[3]))
    print(type1 + id_list.pop(0) + "["+size+"]",end="")
def p_record_type(p):
    '''record_type :  record_sym record_section record_section_list  SEMI_COLON rec_end_sym'''
    pass
def p_record_type_td(p):
    '''record_type_td :  record_sym_td record_section record_section_list  SEMI_COLON rec_end_sym_td'''
    pass
def p_rec_end_sym(p):
    '''rec_end_sym :  END_SYM'''
    print("}",end="")
text=[]
def p_rec_end_sym_td(p):
    '''rec_end_sym_td :  END_SYM'''
    print("}"+text.pop(0),end="")
def p_record_sym(p):
    '''record_sym :  RECORD_SYM'''
    print("struct "+id_list.pop(0)+ "{")
def p_record_sym_td(p):
    '''record_sym_td :  RECORD_SYM'''
    print("typedef struct "+ "{")
    text.append(id_list.pop(0))
def p_record_section_list(p):
    '''record_section_list : record_section_list SEMI_COLON record_section
                    | empty'''
    pass
def p_record_section(p):
    '''record_section : id_list COLON type_denoter'''
    print(type1, end=" ")
    for i in id_list:
        if i != id_list[-1]:
            print(i, end=", ")
        else:
            print(i, end=";\n")
    id_list.clear()
def p_var_block(p):
    '''var_block : VAR_SYM var_decl var_decl_list
                | empty'''
    pass
def p_var_decl(p):
    '''var_decl : id_list COLON type_denoter SEMI_COLON'''
    for i in id_list:
        if i!= id_list[-1]:
            print(i,end=", ")
        else:
            print(i,end=";\n")
    id_list.clear()
def p_var_decl_list(p):
    '''var_decl_list : var_decl_list var_decl
                    | empty'''
    pass



pf_type=[]
id_list_pom=[]
def p_procedure_and_function_block(p):
    '''procedure_and_function_block : procedure_and_function_block procedure_decl
                                    | procedure_and_function_block function_decl
                                    | empty'''
    pass
def p_procedure_decl(p):
    '''procedure_decl : procedure_header SEMI_COLON block'''
    pass
def p_procedure_header(p):
    '''procedure_header : PROCEDURE_SYM ID
                        | PROCEDURE_SYM ID NAWL param_section param_section_list NAWR'''
    print("void " + p[2] + "(",end="")
    for i in id_list_pom:
        if i!= id_list_pom[-1]:
            print(i,end=", ")
        else:
            print(i, end="")
    print(")", end="\n")
    id_list_pom.clear()
    pf_type.clear()
    id_list.clear()
def p_param_section(p):
    '''param_section : id_list COLON type_general_pf'''
    id_pom=[]
    for i in id_list:
        st =pf_type[-1]+" "+i
        id_pom.append(st)
    id_list.clear()
    for i in id_pom:
        id_list.append(i)
    pf_type.clear()
def p_param_section_list(p):
    '''param_section_list : param_section_list SEMI_COLON param_section
                        | empty'''
    for i in id_list:
        id_list_pom.append(i)
    id_list.clear()
def p_type_general_pf(p):
    '''type_general_pf : CHAR_SYM
                    | INTEGER_SYM
                    | REAL_SYM
                    | BOOLEAN_SYM'''
    if p[1] == 'integer':
        pf_type.append("int")
    elif p[1] == 'real':
        pf_type.append("double")
    elif p[1] == 'char':
        pf_type.append("char")
    elif p[1] == 'boolean':
        pf_type.append("bool")
def p_function_decl(p):
    '''function_decl : function_header SEMI_COLON block'''
    pass
def p_function_header(p):
    '''function_header : FUNCTION_SYM ID COLON type_general_pf
                        | FUNCTION_SYM ID NAWL param_section param_section_list NAWR COLON type_general_pf'''
    print(pf_type.pop(-1) +" "+ p[2] + "(", end="")
    for i in id_list_pom:
        if i != id_list_pom[-1]:
            print(i, end=", ")
        else:
            print(i, end="")
    print(")", end="\n")
    id_list_pom.clear()
    id_list_pom.clear()
    pf_type.clear()

def p_error(p):
    print("Syntax error in input!!!")
def p_empty(p):
    'empty :'
    pass

parser = yacc.yacc()
result = parser.parse(data)
