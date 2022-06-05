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
    print("#include <stdio.h>")
    print("#include <stdbool.h>")
def p_block(p):
    'block : const_block type_block var_block procedure_and_function_block' #operation_block'
    pass
constdef=[]
def p_const_block(p):
    '''const_block : CONST_SYM const_def SEMI_COLON const_def_list
                    | empty'''

def p_const_def_list(p):
    '''const_def_list : const_def_list const_def SEMI_COLON
                      | empty'''
    pass
def p_const_def(p):
    'const_def : id EQUAL const_value'
    if str(constdef[-1])[0]=='\"':
        print("const char "+str(constdef[0])+"["+str(len(str(constdef[-1])))+"] = "+str(constdef[-1])+";")
    elif str(constdef[-1]).isnumeric():
        print("const int " + str(constdef[0]) + " = " + str(constdef[-1])+";")
    else:
        print("const double " + str(constdef[0]) + " = " + str(constdef[-1])+";")
    constdef.clear()
def p_id(p):
    'id : ID'
    constdef.append(p[1])

def p_id1(p):
    'id1 : ID'
    print(p[1], end=" ")
def p_const_value(p):
    '''const_value :  sign id
                    | real_number
                    | sign real_number
                    | TEXT'''
    if p[1]is not None and str(p[1])[0]=='\'':
        x=str(p[1])
        constdef.append(x.replace('\'','\"'))
def p_sign(p):
    '''sign : OPER_ADD
                    | OPER_SUB'''
    if len(constdef)==1:
        constdef.append(p[1])
    else:
        constdef.append(str(constdef.pop(-1)) + str(p[1]))
def p_real_number(p):
    '''real_number : num
                    | num dot num
                    | num e sign num
                    | num dot num e sign num'''
def p_num(p):
    '''num : NUMBER'''
    if len(constdef) == 1:
        constdef.append(p[1])
    else:
        constdef.append(str(constdef.pop(-1)) + str(p[1]))
def p_dot(p):
    '''dot : DOT'''
    constdef.append(str(constdef.pop(-1)) + str(p[1]))
def p_e(p):
    'e : ID'
    if p[1] !='e':
        print("Syntax error in input!")
    else:
        constdef.append(str(constdef.pop(-1)) + str(p[1]))




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
                    | id1'''
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
        if i== id_list[0]:
            continue
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


# def p_operation_block(p):
#     'operation_block : BEGIN_SYM statement_sequence END_SYM'
#     pass
#
# def p_statement_sequence(p):
#     'statement_sequence : statement statement_list'
#     pass
#
# def p_statement_list(p):
#     '''statement_list : statement_list SEMI_COLON statement
#                         | empty'''
#     pass
#
# def p_statement(p):
#     '''statement :  structured_statement''' #simple statement |
#     pass

# def p_simple_statement(p):
#     '''simple_statement : assign_statement
#                         | procedure_statement
#                         | procedure_method_statement
#                         | empty'''
#     pass

# def p_structured_statement(p):
#     '''structured_statement : conditional_statement
#                         | repetitive_statement''' #operation_block |
#     pass
#
# def p_repetitive_statement(p):
#     'repetitive_statement : while_statement'
#     #'''repetitive_statement : repeat_statement
#     #                    | while_statement
#     #                    | for_statement'''
#     pass
#
# def p_while_statement(p):
#     'while_statement : WHILE_SYM expression DO_SYM statement'
#     pass

# def p_repeat_statement(p):
#     'repeat_statement : REPEAT_SYM statement_sequence UNTIL_SYM expression'
#     pass
#
# def p_for_statement(p):
#     '''for_statement : FOR_SYM ID ASSIGN_SYM expression TO_SYM expression
#                         | FOR_SYM ID ASSIGN_SYM expression DOWNTO_SYM expression'''
#     pass
#
# def p_conditional_statement(p):
#     '''conditional_statement : if_statement
#                         | case_statement'''
#     pass
#
# def p_if_statement(p):
#     '''if_statement : IF_SYM expression THEN_SYM statement else_part
#                         | IF_SYM expression THEN_SYM statement'''
#     pass
#
# def p_else_part(p):
#     'else_part : ELSE_SYM statement'
#     pass
#
# def p_case_statement(p):
#     '''case_statement : CASE_SYM expression case_body SEMI_COLON END_SYM
#                         | CASE_SYM expression case_body END_SYM'''
#     pass
#
# def p_case_body(p):
#     '''case_body : case_list_elements SEMI_COLON case_statement_completer
#                         | case_list_elements case_statement_completer
#                         | case_statement_completer'''
#     pass
#
# def p_case_list_elements(p):
#     'case_list_elements : case_list_element case_list_element_list'
#     pass
#
# def p_case_list_element_list(p):
#     '''case_list_element_list : case_list_element_list SEMI_COLON case_list_element
#                         | empty'''
#     pass
#
# def p_case_list_element(p):
#     'case_list_element : case_constant_list COLON statement'
#     pass
#
# def p_case_constant_list(p):
#     'case_constant_list : case_specifier case_specifier_list'
#     pass
#
# def p_case_specifier_list(p):
#     '''case_specifier_list : case_specifier_list COMMA case_specifier
#                         | empty'''
#     pass
#
# def p_case_specifier(p):
#     '''case_specifier : constant DOUBLE_DOT constant
#                         | constant'''
#     pass
#
# def p_case_specifier_competer(p):
#     'case_specifier_completer : ELSE_SYM statement_sequence'
#     pass

# def p_expression(p):
#     '''expression : simple expression relational_operator simple_expression
#                         | simple expression'''
#     pass
#
# def p_relational_operator(p):
#     '''relational_operator : EQUAL
#                         | NOT_EQUAL
#                         | LOWER
#                         | LW_EQ
#                         | GREATER
#                         | GR_EQ
#                         | empty'''
#     pass
#
# def p_simple_expression(p):
#     'simple_expression : term add_oper_list'
#     pass
#
# def p_add_oper_list(p):
#     '''add_oper_list : add_oper_list add_oper term
#                         | empty'''
#     pass
#
# def p_add_oper(p):
#     '''add_oper : OPER_ADD
#                         | OPER_SUB
#                         | OR_SYM'''
#     pass
#
# def p_term(p):
#     'term : factor factor_list'
#     pass
#
# def p_factor_list(p):
#     '''factor_list : factor_list mult_oper factor
#                         | empty'''
#     pass
#
# def p_mult_oper(p):
#     '''mult_oper : OPER_MULT
#                         | OPER_DIV
#                         | DIV_SYM
#                         | MOD_SYM
#                         | AND_SYM'''
#     pass



parser = yacc.yacc()
result = parser.parse(data)
