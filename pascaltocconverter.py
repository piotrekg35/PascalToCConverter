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
for token in lexer:
    print("line %d: %s(%s)" %(token.lineno, token.type, token.value))


def p_pascal_program(p):
    'pascal_program : pogram_header SEMI_COLON block DOT'
    pass
def p_program_header(p):
    'pogram_header : PROGRAM_SYM ID'
    print("//Program: "+p[2])
def p_block(p):
    'block : const_block type_block var_block'# procedure_and_function_block operation_block'
    pass
def p_const_block(p):
    '''const_block : CONST_SYM const_def SEMI_COLON const_def_list
                    | empty'''
    pass

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
    print(p[1],end=" ")
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
    pass
def p_type_def(p):
    '''type_def : ID EQUAL type_denoter'''
    pass
def p_type_denoter(p):
    '''type_denoter : type_general
                    | enumerated_type
                    | array_type
                    | record_type
                    | ID'''
    pass
def p_type_general(p):
    '''type_general : CHAR_SYM
                    | INTEGER_SYM
                    | REAL_SYM
                    | BOOLEAN_SYM
                    | STRING_SYM'''
    pass
def p_enumerated_type(p):
    '''enumerated_type : NAWL id_list NAWR'''
    pass
def p_id_list(p):
    '''id_list : ID
                | id_list COMMA ID'''
    pass
def p_array_type(p):
    '''array_type : ARRAY_SYM NAWKL NUMBER DOUBLE_DOT NUMBER NAWKR OF_SYM type_denoter
                | ARRAY_SYM NAWKL sign NUMBER DOUBLE_DOT NUMBER NAWKR OF_SYM type_denoter
                | ARRAY_SYM NAWKL NUMBER DOUBLE_DOT sign NUMBER NAWKR OF_SYM type_denoter
                | ARRAY_SYM NAWKL sign NUMBER DOUBLE_DOT sign NUMBER NAWKR OF_SYM type_denoter'''
    pass
def p_record_type(p):
    '''record_type : RECORD_SYM END_SYM
                | RECORD_SYM record_section record_section_list  SEMI_COLON END_SYM
                | RECORD_SYM record_section  record_section_list END_SYM'''
    pass
def p_record_section_list(p):
    '''record_section_list : record_section_list SEMI_COLON record_section
                    | empty'''
    pass
def p_record_section(p):
    '''record_section : id_list COLON type_denoter'''
    pass
def p_var_block(p):
    '''var_block : VAR_SYM var_decl var_decl_list
                | empty'''
    pass
def p_var_decl(p):
    '''var_decl : id_list COLON type_denoter SEMI_COLON'''
    pass
def p_var_decl_list(p):
    '''var_decl_list : var_decl_list var_decl
                    | empty'''
    pass
def p_error(p):
    print("Syntax error in input!!!")
def p_empty(p):
    'empty :'
    pass

parser = yacc.yacc()
result = parser.parse(data)