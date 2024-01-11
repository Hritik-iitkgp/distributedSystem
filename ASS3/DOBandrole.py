import ply.lex as lex
import ply.yacc as yacc

###DEFINING TOKENS###
tokens = ('BEGINTABLE', 
'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN',
'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE','GARBAGE','STOP')
t_ignore = '\t'

###############Tokenizer Rules################
def t_BEGINTABLE(t):
     r'<th.colspan="2".class="infobox-header".style="background-color:.\#b0c4de">Personal.information</th>'
     return t

def t_OPENTABLE(t):
    r'<tbody[^>]*>'
    return t

def t_CLOSETABLE(t):
    r'</tbody[^>]*>'
    return t

def t_OPENROW(t):
    r'<tr[^>]*>'
    return t

def t_CLOSEROW(t):
    r'</tr[^>]*>'
    return t

def t_OPENHEADER(t):
    r'<th[^>]*>'
    return t

def t_CLOSEHEADER(t):
    r'</th[^>]*>'
    return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    return t

def t_CLOSEHREF(t):
    r'</a[^>]*>'
    return t

def t_OPENDATA(t):
    r'<td[^>]*>'
    return t

def t_CLOSEDATA(t):
    r'</td[^>]*>'
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9, ]+'
    return t

def t_OPENDIV(t):
    r'<div[^>]*>'

def t_CLOSEDIV(t):
    r'</div[^>]*>'

def t_OPENSTYLE(t):
    r'<style[^>]*>'

def t_CLOSESTYLE(t):
    r'</style[^>]*>'

def t_OPENSPAN(t):
    r'<span[^>]*>'

def t_CLOSESPAN(t):
    r'</span[^>]*>'

def t_GARBAGE(t):
    r'<[^>]*>'

def t_error(t):
    t.lexer.skip(1)
####################################################################################################################################################################################################
											#GRAMMAR RULES
def p_start(p):
    '''start : table'''
    p[0] = p[1]

def p_table(p):
    '''table : BEGINTABLE skiptag handlerow handlerow handlerow handlerow handlerow  handlerow handlerow
 | '''

def p_skiptag(p):
    '''skiptag :  CLOSEROW skiptag
               | empty'''

def p_handlerow(p):
    '''handlerow : OPENROW handleheader dataCell CLOSEROW handlerow           
    | OPENROW handleheader CLOSEROW
    | '''
    if(len(p)==6 and p[2]=="Full name"):
        print(p[2],":",p[3])
    if(len(p)==6 and len(p[3].split())==5):
        print("DOB :",' '.join(p[3].split()[1:4]))
    if(len(p)==6 and p[2]=="Role"):
        print(p[2],":",p[3])
    if(len(p)==6 and p[2]=="National side"):
        print(p[2],":",p[3].split(',')[3])
    if(len(p)==6 ):
        print(p[3])
def p_dataCell(p):
    '''dataCell : OPENDATA content CLOSEDATA  dataCell 
    | OPENDATA content handlehref content CLOSEDATA dataCell
    | OPENDATA handlehref content CLOSEDATA dataCell
                | '''
    if len(p) == 5:
        p[0]=p[2]
    if len(p) == 6:
        p[0]=p[2]
    if len(p) == 7:
        #print("DOB : ", )
        p[0]=p[2] +","+p[3]


def p_handlehref(p):
    '''handlehref : OPENHREF content CLOSEHREF handlehref
	| '''
    if(len(p)==5):
        p[0]=p[2]

def p_handleheader(p):
    '''handleheader : OPENHEADER CONTENT CLOSEHEADER handleheader
                    | OPENHEADER CONTENT CONTENT CONTENT CLOSEHEADER handleheader
                    | OPENHEADER content handlehref CLOSEHEADER handleheader
                    | empty'''
    if len(p) == 7:
        p[0]=p[2]+" "+p[4]
        #print(p[0])
    elif(len(p)==5):
        p[0]=p[2]
    else:
        p[0]=p[1]






def p_empty(p):
    '''empty :'''
    pass

def p_content(p):
    '''content : CONTENT content
               | empty'''
    if len(p)==3 :              
    	p[0] = p[1]+p[2]
    else:
        p[0]=''

def p_Content(p):
    '''Content : CONTENT Content
               | empty'''
    p[0] = p[1]        

def p_error(p):
    print(p, 'error')
    #pass

#########DRIVER FUNCTION#######
def main():
    file_obj= open('webpage.html','r',encoding="utf-8")
    data=file_obj.read()
    lexer = lex.lex()
    lexer.input(data)
    for tok in lexer:
        print(tok)
    parser = yacc.yacc()
    parser.parse(data)
    file_obj.close()

if __name__ == '__main__':
    main()
