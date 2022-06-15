import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'and': 'AND_SYM',
    'array': 'ARRAY_SYM',
    'begin': 'BEGIN_SYM',
    'const': 'CONST_SYM',
    'div': 'DIV_SYM',
    'do': 'DO_SYM',
    'downto': 'DOWNTO_SYM',
    'else': 'ELSE_SYM',
    'end': 'END_SYM',
    'for': 'FOR_SYM',
    'function': 'FUNCTION_SYM',
    'if': 'IF_SYM',
    'mod': 'MOD_SYM',
    'not': 'NOT_SYM',
    'of': 'OF_SYM',
    'or': 'OR_SYM',
    'procedure': 'PROCEDURE_SYM',
    'program': 'PROGRAM_SYM',
    'record': 'RECORD_SYM',
    'then': 'THEN_SYM',
    'to': 'TO_SYM',
    'type': 'TYPE_SYM',
    'var': 'VAR_SYM',
    'while': 'WHILE_SYM',
    'char': 'CHAR_SYM',
    'integer': 'INTEGER_SYM',
    'real': 'REAL_SYM',
    'boolean': 'BOOLEAN_SYM',
    'string': 'STRING_SYM',
    'writeln': 'WRITELN_SYM',
    'readln': 'READLN_SYM'
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
             'ASSIGN_SYM',
             'NUMBER',
             'ID',
             'TEXT',
             'SINGLE_LINE_COMMENT',
             'MULTI_LINE_COMMENT'
         ] + list(reserved.values())

t_COLON = r':'
t_SEMI_COLON = r';'
t_COMMA = r','
t_DOT = r'\.'
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
t_ASSIGN_SYM = r':='


def t_NUMBER(t):
    r"""[0-9][0-9]*"""
    t.value = int(t.value)
    return t


def t_ID(t):
    r"""[a-zA-Z][a-zA-Z0-9]*"""
    t.type = reserved.get(t.value, 'ID')
    return t


def t_TEXT(t):
    r"""\'[^\'\n]*\'"""
    return t


def t_SINGLE_LINE_COMMENT(t):
    r"""\(\*[^\*\n]*[^\)\n]*\*\)"""
    return


def t_MULTI_LINE_COMMENT(t):
    r"""{[^{}]*}"""
    return


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise Exception("Illegal character {} at line {}.".format(t.value[0],t.lexer.lineno))


outputstr = ""
t_ignore = '  \t'

id_list = []
type1 = ""
text = []
pf_type = []
id_list_pom = []
isMain = [True]
statement_seq = []
constdef = []
id_in_loop=""
declared_id={}
declared_type={}
function_name=""

def init(data):
    global outputstr
    outputstr = ""
    lexer = lex.lex()
    # with open('test.txt', 'r') as file:
    #     data = file.read()
    lexer.input(data)
    # for token in lexer:
    # print("line %d: %s(%s)" %(token.lineno, token.type, token.value))

    parser = yacc.yacc()
    result = parser.parse(data)
    return outputstr


def p_pascal_program(p):
    """pascal_program : program_header SEMI_COLON block DOT"""
    pass


def p_program_header(p):
    """program_header : PROGRAM_SYM ID"""
    global outputstr
    outputstr += "//Program: " + p[2] + "\n"
    outputstr += "#include <stdio.h>\n"
    outputstr += "#include <stdbool.h>\n"


def p_block(p):
    """block : const_block type_block var_block procedure_and_function_block operation_block"""
    pass


def p_const_block(p):
    """const_block : CONST_SYM const_def SEMI_COLON const_def_list
                    | empty"""


def p_const_def_list(p):
    """const_def_list : const_def_list const_def SEMI_COLON
                      | empty"""
    pass


def p_const_def(p):
    """const_def : id EQUAL const_value"""
    global outputstr
    if str(constdef[-1])[0] == '\"':
        outputstr += "const char " + str(constdef[0]) + "[" + str(len(str(constdef[-1]))) + "] = " + str(
            constdef[-1]) + ";\n"
        declared_id[str(constdef[0])]="const char*"
    elif str(constdef[-1]).isnumeric():
        outputstr += "const int " + str(constdef[0]) + " = " + str(constdef[-1]) + ";\n"
        declared_id[str(constdef[0])] = "const int"
    else :
        outputstr += "const double " + str(constdef[0]) + " = " + str(constdef[-1]) + ";\n"
        declared_id[str(constdef[0])] = "const double"
    constdef.clear()


def p_id(p):
    """id : ID"""
    constdef.append(p[1])


def p_id1(p):
    """id1 : ID"""
    global outputstr
    outputstr += p[1] + " "  # , end=" "


def p_id2(p):
    """id2 : ID"""
    if len(statement_seq) > 0 and statement_seq[-1][-1]=="\t":
        statement_seq[-1] = statement_seq[-1] + str(p[1])+" = "
    else:
        statement_seq.append(str(p[1]) + " = ")

def p_id3(p):
    'id3 : ID'
    statement_seq.append(str(p[1]) + "(")

def p_const_value(p):
    """const_value :  real_number
                    | sign real_number
                    | TEXT"""
    if p[1] is not None and str(p[1])[0] == '\'':
        x = str(p[1])
        constdef.append(x.replace('\'', '\"'))


def p_sign(p):
    """sign : OPER_ADD
                    | OPER_SUB"""
    if len(constdef) == 1:
        constdef.append(p[1])
    elif len(constdef) > 1:
        constdef.append(str(constdef.pop(-1)) + str(p[1]))
    if len(statement_seq) > 0:
        statement_seq[-1] = statement_seq[-1] + str(p[1])


def p_real_number(p):
    """real_number : num
                    | num dot num
                    | num e sign num
                    | num dot num e sign num"""


def p_num(p):
    """num : NUMBER"""
    if len(constdef) == 1 or len(constdef) > 0 and str(str(constdef[-1])[-1]).isdigit():
        constdef.append(p[1])
    elif len(constdef) > 1:
        constdef.append(str(constdef.pop(-1)) + str(p[1]))
    if len(statement_seq) > 0:
        statement_seq[-1] = statement_seq[-1] + str(p[1])


def p_dot(p):
    """dot : DOT"""
    if len(constdef) > 0:
        constdef.append(str(constdef.pop(-1)) + str(p[1]))
    if len(statement_seq) > 0:
        statement_seq[-1] = statement_seq[-1] + str(p[1])


def p_e(p):
    """e : ID"""
    global outputstr
    if p[1] != 'e':
        raise Exception("Expected e got {} at line {}".format(str(p[1]),p.lexer.lineno))
    else:
        if len(constdef) > 0:
            constdef.append(str(constdef.pop(-1)) + str(p[1]))
        if len(statement_seq) > 0:
            statement_seq[-1] = statement_seq[-1] + str(p[1])


def p_type_block(p):
    """type_block : TYPE_SYM type_def SEMI_COLON type_def_list
                    | empty"""
    pass


def p_type_def_list(p):
    """type_def_list : type_def_list type_def SEMI_COLON
                    | empty"""
    global outputstr
    outputstr += ';\n'


def p_type_def(p):
    """type_def : id_list EQUAL type_denoter_td"""
    global outputstr
    for i in id_list:
        if i != id_list[-1]:
            outputstr += i + ", "  # ,end=", "
        else:
            outputstr += i  # ,end="")
        declared_type[str(i)]=type1
    id_list.clear()


def p_type_denoter(p):
    """type_denoter : type_general
                    | enumerated_type
                    | array_type
                    | record_type
                    | id1"""
    pass


def p_type_denoter_td(p):
    """type_denoter_td : type_general_td
                    | enumerated_type_td
                    | array_type_td
                    | record_type_td"""
    pass


def p_type_general(p):
    """type_general : CHAR_SYM
                    | INTEGER_SYM
                    | REAL_SYM
                    | BOOLEAN_SYM
                    | STRING_SYM"""
    global outputstr, type1
    if p[1] == 'integer':
        outputstr += "int "  # ,end=" ")
        type1 = "int"
    elif p[1] == 'real':
        outputstr += "double "  # , end=" ")
        type1 = "double"
    elif p[1] == 'char':
        outputstr += "char "  # , end=" ")
        type1 = "char"
    elif p[1] == 'boolean':
        outputstr += "bool "  # , end=" ")
        type1 = "bool"
    elif p[1] == 'string':
        outputstr += "char "  # , end=" ")
        type1 = "char*"


def p_type_general_td(p):
    """type_general_td : CHAR_SYM
                    | INTEGER_SYM
                    | REAL_SYM
                    | BOOLEAN_SYM"""
    global outputstr, type1
    if p[1] == 'integer':
        outputstr += "typedef int "  # ,end=" ")
        type1 = "int"
    elif p[1] == 'real':
        outputstr += "typedef double "  # , end=" ")
        type1 = "double"
    elif p[1] == 'char':
        outputstr += "typedef char "  # , end=" ")
        type1 = "char"
    elif p[1] == 'boolean':
        outputstr += "typedef bool "  # , end=" ")
        type1 = "bool"
    elif p[1] == 'string':
        outputstr += "char "  # , end=" ")
        type1 = "char*"


def p_enumerated_type(p):
    """enumerated_type : NAWL id_list NAWR"""
    global outputstr
    outputstr += "enum " + id_list.pop(0) + " {"  # ,end="")
    for i in id_list:
        if i != id_list[-1]:
            outputstr += i + ", "  # ,end=", ")
        else:
            outputstr += i  # ,end="")
    outputstr += "}"  # , end="")
    id_list.clear()


def p_enumerated_type_td(p):
    """enumerated_type_td : NAWL id_list NAWR"""
    global outputstr
    outputstr += "typedef enum " + " {"  # ,end="")
    for i in id_list:
        if i == id_list[0]:
            continue
        if i != id_list[-1]:
            outputstr += i + ", "  # ,end=", ")
        else:
            outputstr += i  # ,end="")
    outputstr += "}" + id_list.pop(0)  # , end="")
    id_list.clear()


def p_id_list(p):
    """id_list : ID
                | id_list COMMA ID"""
    if p[1] is not None:
        id_list.append(p[1])
    else:
        id_list.append(p[3])


def p_array_type(p):
    """array_type : ARRAY_SYM NAWKL NUMBER DOUBLE_DOT NUMBER NAWKR OF_SYM type_denoter"""
    global outputstr
    size = str(int(p[5]) - int(p[3]))
    outputstr += type1 + id_list.pop(0) + "[" + size + "]"  # ,end="")


def p_array_type_td(p):
    """array_type_td : ARRAY_SYM NAWKL NUMBER DOUBLE_DOT NUMBER NAWKR OF_SYM type_denoter_td"""
    global outputstr
    size = str(int(p[5]) - int(p[3]))
    outputstr += type1 + id_list.pop(0) + "[" + size + "]"  # ,end="")


def p_record_type(p):
    """record_type :  record_sym record_section record_section_list  SEMI_COLON rec_end_sym"""
    pass


def p_record_type_td(p):
    """record_type_td :  record_sym_td record_section record_section_list  SEMI_COLON rec_end_sym_td"""
    pass


def p_rec_end_sym(p):
    """rec_end_sym :  END_SYM"""
    global outputstr
    outputstr += "}"  # ,end="")


def p_rec_end_sym_td(p):
    """rec_end_sym_td :  END_SYM"""
    global outputstr
    outputstr += "}" + text.pop(0)  # ,end="")


def p_record_sym(p):
    """record_sym :  RECORD_SYM"""
    global outputstr
    outputstr += "struct " + id_list.pop(0) + "{\n"


def p_record_sym_td(p):
    """record_sym_td :  RECORD_SYM"""
    global outputstr
    outputstr += "typedef struct " + "{\n"
    text.append(id_list.pop(0))


def p_record_section_list(p):
    """record_section_list : record_section_list SEMI_COLON record_section
                    | empty"""
    pass


def p_record_section(p):
    """record_section : id_list COLON type_denoter"""
    global outputstr
    for i in id_list:
        if i != id_list[-1]:
            outputstr += i + ", "  # , end=", ")
        else:
            outputstr += i + ";\n"  # ", end=";\n")
    id_list.clear()


def p_var_block(p):
    """var_block : VAR_SYM var_decl var_decl_list
                | empty"""
    pass


def p_var_decl(p):
    """var_decl : id_list COLON type_denoter SEMI_COLON"""
    global outputstr
    for i in id_list:
        if i != id_list[-1]:
            if type1=="char*":
                outputstr += "char "+ i + "[100], "
            else:
                outputstr += i + ", "
        else:
            if type1=="char*":
                outputstr += "char "+ i + "[100];\n"
            else:
                outputstr += i + ";\n"
        declared_id[str(i)]=type1

    id_list.clear()


def p_var_decl_list(p):
    """var_decl_list : var_decl_list var_decl
                    | empty"""
    pass


def p_procedure_and_function_block(p):
    """procedure_and_function_block : procedure_and_function_block procedure_decl
                                    | procedure_and_function_block function_decl
                                    | empty"""
    pass


def p_procedure_decl(p):
    """procedure_decl : procedure_header SEMI_COLON block SEMI_COLON"""
    isMain[0] = True


def p_procedure_header(p):
    """procedure_header : PROCEDURE_SYM ID
                        | PROCEDURE_SYM ID NAWL param_section param_section_list NAWR"""
    global outputstr
    isMain[0] = False
    outputstr += "void " + p[2] + "("  # ,end="")
    for i in id_list_pom:
        if i != id_list_pom[-1]:
            outputstr += i + ", "  # ,end=", ")
        else:
            outputstr += i  # , end="")
    outputstr += ")" + "\n"  # , end="\n")
    id_list_pom.clear()
    pf_type.clear()
    id_list.clear()


def p_param_section(p):
    """param_section : id_list COLON type_general_pf"""
    id_pom = []
    for i in id_list:
        st = pf_type[-1] + " " + i
        id_pom.append(st)
    id_list.clear()
    for i in id_pom:
        id_list.append(i)
    pf_type.clear()


def p_param_section_list(p):
    """param_section_list : param_section_list SEMI_COLON param_section
                        | empty"""
    for i in id_list:
        id_list_pom.append(i)
    id_list.clear()


def p_type_general_pf(p):
    """type_general_pf : CHAR_SYM
                    | INTEGER_SYM
                    | REAL_SYM
                    | BOOLEAN_SYM"""
    if p[1] == 'integer':
        pf_type.append("int")
    elif p[1] == 'real':
        pf_type.append("double")
    elif p[1] == 'char':
        pf_type.append("char")
    elif p[1] == 'boolean':
        pf_type.append("bool")


def p_function_decl(p):
    """function_decl : function_header SEMI_COLON block SEMI_COLON"""
    isMain[0] = True


def p_function_header(p):
    """function_header : FUNCTION_SYM ID COLON type_general_pf
                        | FUNCTION_SYM ID NAWL param_section param_section_list NAWR COLON type_general_pf"""
    global outputstr,function_name
    isMain[0] = False
    outputstr += pf_type.pop(-1) + " " + p[2] + "("  # , end="")
    for i in id_list_pom:
        if i != id_list_pom[-1]:
            outputstr += i + ", "  # , end=", ")
        else:
            outputstr += i  # , end="")
    outputstr += ")" + "\n"  # , end="\n")
    id_list_pom.clear()
    id_list_pom.clear()
    pf_type.clear()
    function_name=str(p[2])


def p_error(p):
    raise Exception("Syntax error at {}!\n".format(p.value))


def p_empty(p):
    """empty :"""
    pass


def p_operation_block(p):
    """operation_block : BEGIN_SYM statement_sequence END_SYM"""
    global outputstr,function_name
    if isMain[0] is True:
        outputstr += "void main()\n"
    outputstr += "{\n"
    for st in statement_seq:
        outputstr += "\t" + st + "\n"
    if function_name !="":
        outputstr += "\treturn "+function_name+";\n"
        function_name=""
    outputstr += "}\n"
    statement_seq.clear()


def p_statement_sequence(p):
    """statement_sequence : statement statement_list"""
    pass


def p_statement_list(p):
    """statement_list : statement_list SEMI_COLON statement
                        | empty"""
    pass


def p_statement(p):
    """statement : simple_statement
                    | structured_statement"""
    pass


def p_simple_statement(p):
    """simple_statement : assign_statement
                        | procedure_statement
                        | empty"""


def p_structured_statement(p):
    """structured_statement : operation_sub_block
                        | conditional_statement
                        | repetitive_statement"""
    pass


def p_repetitive_statement(p):
    """repetitive_statement :  while_statement
                        | for_statement"""
    pass


def p_while_statement(p):
    """while_statement : while expression do statement"""
    pass

def p_while(p):
    """while : WHILE_SYM"""
    statement_seq.append("while(")

def p_do(p):
    """do : DO_SYM"""
    if len(statement_seq) > 0:
        statement_seq[-1] = statement_seq[-1] + ")\n\t{\n\t"

def p_operation_sub_block(p):
    """operation_sub_block : BEGIN_SYM statement_sequence END_SYM"""
    if len(statement_seq) > 0:
        statement_seq[-1] = statement_seq[-1] + "\n\t}"


def p_for_statement(p):
    """for_statement : for_id ASSIGN_SYM expression to_downto expression for_do statement"""
    pass

def p_for_id(p):
    """for_id : FOR_SYM ID"""
    global  id_in_loop
    statement_seq.append("for("+str(p[2])+"=")
    id_in_loop=str(p[2])

def p_to_downto(p):
    """to_downto : TO_SYM
                | DOWNTO_SYM"""
    global id_in_loop
    if len(statement_seq) > 0:
        if p[1]=="to":
            statement_seq[-1] = statement_seq[-1] +";"+id_in_loop+">="
            id_in_loop = id_in_loop+"+"
        else:
            statement_seq[-1] = statement_seq[-1] + ";" + id_in_loop + "<="
            id_in_loop = id_in_loop + "-"
def p_for_do(p):
    """for_do : DO_SYM"""
    if len(statement_seq) > 0:
        if id_in_loop[-1] == "+":
            statement_seq[-1] = statement_seq[-1] +";++"+id_in_loop[:-1]+"){\n\t"
        else:
            statement_seq[-1] = statement_seq[-1] + ";--" + id_in_loop[:-1]+"){\n\t"

def p_conditional_statement(p):
    """conditional_statement : if expression then statement else_part
                        | if expression then statement"""
    pass


def p_if(p):
    """if : IF_SYM"""
    if len(statement_seq) > 0 and len(statement_seq[-1]) > 6 and statement_seq[-1][-4:]=='else':
        statement_seq[-1]=str(statement_seq[-1]).replace("else","else if(")
    else:
        statement_seq.append("if (")

def p_then(p):
    """then : THEN_SYM"""
    if len(statement_seq) > 0:
        statement_seq[-1] = statement_seq[-1] + ")"

def p_else_part(p):
    """else_part : else statement"""
    pass
def p_else(p):
    """else : ELSE_SYM"""
    if len(statement_seq) > 0:
        statement_seq[-1] = statement_seq[-1] + "\n\telse"

def p_expression(p):
    """expression : simple_expression relational_operator simple_expression
                        | simple_expression"""
    pass


def p_relational_operator(p):
    """relational_operator : EQUAL
                        | NOT_EQUAL
                        | LOWER
                        | LW_EQ
                        | GREATER
                        | GR_EQ
                        | empty"""
    if p[1] is not None and len(statement_seq) > 0:
        if p[1] == "=":
            statement_seq[-1] = statement_seq[-1] + "=="
        elif p[1] == "<>":
            statement_seq[-1] = statement_seq[-1] + "!="
        else:
            statement_seq[-1] = statement_seq[-1] + str(p[1])


def p_simple_expression(p):
    """simple_expression : term add_oper_list"""
    pass


def p_add_oper_list(p):
    """add_oper_list : add_oper_list add_oper term
                        | empty"""
    pass


def p_add_oper(p):
    """add_oper : OPER_ADD
                        | OPER_SUB
                        | OR_SYM"""
    if len(statement_seq) > 0:
        statement_seq[-1] = statement_seq[-1] + str(p[1])


def p_term(p):
    """term : factor factor_list"""
    pass


def p_factor_list(p):
    """factor_list : factor_list mult_oper factor
                        | empty"""
    pass


def p_mult_oper(p):
    """mult_oper : OPER_MULT
                        | OPER_DIV
                        | DIV_SYM
                        | MOD_SYM
                        | AND_SYM"""
    if len(statement_seq) > 0:
        statement_seq[-1] = statement_seq[-1] + str(p[1])


def p_factor(p):
    """factor : real_number
            | ID
            | NAWL expression NAWR
            | NOT_SYM factor"""
    if p[1] is not None and p[1]!="(" and p[1]!="not":
        if len(statement_seq) > 0:
            statement_seq[-1] = statement_seq[-1] + str(p[1])


def p_assign_statement(p):
    """assign_statement : id2 ASSIGN_SYM expression"""
    if len(statement_seq) > 0:
        statement_seq[-1] = statement_seq[-1] + ";"


def p_procedure_statement(p):
    '''procedure_statement : id3 NAWL const_value const_value_list NAWR
                            | id3 NAWL NAWR
                            | WRITELN_SYM NAWL const_value const_value_list NAWR
                            | WRITELN_SYM NAWL id_list NAWR
                            | WRITELN_SYM NAWL NAWR
                            | READLN_SYM NAWL id_list NAWR'''
    global outputstr
    if p[1]=="writeln" and p[3] is not None:
        statement_seq.append("printf(\"\\n\");")
    elif p[1]=="writeln" and p[3] is None and p[4] is None:
        stat = "printf(\""
        for i in constdef:
            if str(i)[0]=="\"":
                stat+="%s "
            elif str(i).isnumeric():
                stat += "%d "
            else:
                stat += "%f "
        stat+="\\n"
        stat+="\","
        for i in constdef:
            stat+=str(i)
            if i!=constdef[-1]:
                stat+=","
        stat+=");"
        constdef.clear()
        statement_seq.append(stat)
    elif p[1]=="writeln" and p[3] is None and p[4] is not None:
        stat = "printf(\""
        for i in id_list:
            if str(i) not in declared_id.keys():
                raise Exception("Variable " + str(i) + " not declared! ")
            elif "int" in str(declared_id[i]) or declared_id[i] in declared_type.keys() and "int" in declared_type[
                declared_id[i]]:
                stat += "%d "
            elif "double" in str(declared_id[i]) or declared_id[i] in declared_type.keys() and "double" in \
                    declared_type[declared_id[i]]:
                stat += "%f "
            elif "bool" in str(declared_id[i]) or declared_id[i] in declared_type.keys() and "bool" in declared_type[
                declared_id[i]]:
                stat += "%d "
            elif "char" in str(declared_id[i]) or declared_id[i] in declared_type.keys() and "char" in declared_type[
                declared_id[i]]:
                stat += "%s "
            else:
                outputstr += "Error!"
                raise Exception("Cannot print this type!")
        stat += "\\n"
        stat += "\","
        for i in id_list:
            stat += str(i)
            if i != id_list[-1]:
                stat += ","
        stat += ");"
        id_list.clear()
        statement_seq.append(stat)
    elif p[1]=="readln":
        stat = "scanf(\""
        for i in id_list:
            if str(i) not in declared_id.keys():
                raise Exception("Variable "+str(i)+" not declared! ")
            elif "const" in str(declared_id[i]) or declared_id[i] in declared_type.keys() and "const" in declared_type[declared_id[i]]:
                raise Exception("Cannot modify const: "+str(i)+"!")
            elif "int" in str(declared_id[i]) or declared_id[i] in declared_type.keys() and "int" in declared_type[declared_id[i]]:
                stat += "%d "
            elif "double" in str(declared_id[i]) or declared_id[i] in declared_type.keys() and "double" in declared_type[declared_id[i]]:
                stat += "%f "
            elif "bool" in str(declared_id[i]) or declared_id[i] in declared_type.keys() and "bool" in declared_type[declared_id[i]]:
                stat += "%d "
            elif "char" in str(declared_id[i]) or declared_id[i] in declared_type.keys() and "char" in declared_type[declared_id[i]]:
                stat += "%s "
            else:
                raise Exception("Cannot read this type!")
            if i==id_list[-1]:
                stat=stat[:-1]

        stat += "\","
        for i in id_list:
            if "*" not in str(declared_id[i]):
                stat+="&"
            stat += str(i)
            if i != id_list[-1]:
                stat += ","
        stat += ");"
        id_list.clear()
        statement_seq.append(stat)
    else:
        statement_seq[-1]=statement_seq[-1]+");"


def p_const_value_list(p):
    """const_value_list : const_value_list comma const_value
                            | empty"""
    pass

def p_comma(p):
    '''comma : COMMA'''
    if len(statement_seq)>0:
        statement_seq[-1]=statement_seq[-1]+str(p[1])
