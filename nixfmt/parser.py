import sly
from sly.yacc import YaccError

from .lexer import NixLexer, NixStringLexer, NixIndentedStringLexer


class NixParser(sly.Parser):
    tokens = NixLexer.tokens | NixStringLexer.tokens | NixIndentedStringLexer.tokens

    @_('IF expr THEN expr ELSE expr')
    def expr(self, p):
        return ('IF', p.expr0, p.expr1, p.expr2)

    @_('WITH expr SEMICOLON expr')
    def expr(self, p):
        return ('WITH', p.expr0, p.expr1)

    @_('IMPORT expr',
       'ABORT expr')
    def expr(self, p):
        unaryop_map = {
            'import': 'IMPORT',
            'abort': 'ABORT'
        }
        return (unaryop_map[p[0]], p.expr)

    @_('expr PLUS expr',
       'expr MINUS  expr',
       'expr TIMES  expr',
       'expr DIVIDE expr',
       # comparison operation
       'expr LESS   expr',
       'expr LEQ expr',
       'expr NEQ  expr',
       'expr EQ   expr',
       'expr GREATER expr',
       'expr GEQ expr',
       # boolean operation
       'expr AND expr',
       'expr OR expr',
       'expr OR_KW expr',
       'expr CONCAT expr')
    def expr(self, p):
        binop_map = {
            '+': 'PLUS',
            '-': 'SUBTRACT',
            '*': 'TIMES',
            '/': 'DIVIDE',
            '^': 'POWER',
            '<': 'LESSTHAN',
            '<=': 'LESSTHANEQUAL',
            '<>': 'NOTEQUAL',
            '!=': 'NOTEQUAL',
            '=': 'ASSIGN',
            '==': 'EQUAL',
            '>': 'GREATERTHAN',
            '>=': 'GREATERTHANEQUAL',
            '&&': 'AND',
            '||': 'OR',
            'or': 'OR_KW',
            '++': 'CONCAT'
        }
        return (binop_map[p[1]], p.expr0, p.expr1)

    @_('LBRACKET list_fillers RBRACKET')
    def expr(self, p):
        return ('LIST',) + p.list_fillers

    @_('LBRACKET expr list_exprs RBRACKET')
    def expr(self, p):
        return ('LIST', p.expr) + p.list_exprs

    @_('expr list_exprs')
    def list_exprs(self, p):
        return (p.expr,) + p.list_exprs

    @_('empty')
    def list_exprs(self, p):
        return ()

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return ('PARENTHESIS', p.expr)

    @_('WHITESPACE expr')
    def expr(self, p):
        return p.expr[:1] + (('WHITESPACE', p.WHITESPACE),) + p.expr[1:]

    @_('expr WHITESPACE')
    def expr(self, p):
        return p.expr + (('WHITESPACE', p.WHITESPACE),)

    @_('COMMENT expr')
    def expr(self, p):
        return p.expr[:1] + (('COMMENT', p.COMMENT),) + p.expr[1:]

    @_('expr COMMENT')
    def expr(self, p):
        return p.expr + (('COMMENT', p.COMMENT),)

    @_('factor')
    def expr(self, p):
        return p.factor

    # ====== FILLER =======
    @_('COMMENT')
    def comment(self, p):
        return ('COMMENT', p.COMMENT)

    @_('WHITESPACE')
    def whitespace(self, p):
        return ('WHITESPACE', p.WHITESPACE)

    @_('comment list_fillers',
       'whitespace list_fillers')
    def filler(self, p):
        return (p[0],) + p.list_fillers

    @_('comment list_fillers',
       'whitespace list_fillers')
    def list_fillers(self, p):
        return (p[0],) + p.list_fillers

    @_('empty')
    def list_fillers(self, p):
        return ()

    # ====== FACTOR =======
    @_('PATH')
    def factor(self, p):
        return ('PATH', p.PATH)

    @_('HPATH')
    def factor(self, p):
        return ('HPATH', p.HPATH)

    @_('SPATH')
    def factor(self, p):
        return ('SPATH', p.SPATH)

    @_('URI')
    def factor(self, p):
        return ('URI', p.URI)

    @_('STRING_QUOTE STRING STRING_QUOTE')
    def factor(self, p):
        return ('STRING', p.STRING)

    @_('INDENTED_STRING_QUOTE INDENTED_STRING INDENTED_STRING_QUOTE')
    def factor(self, p):
        return ('INDENTED_STRING', p.INDENTED_STRING)

    @_('NULL')
    def factor(self, p):
        return ('NULL', p.NULL)

    @_('FALSE')
    def factor(self, p):
        return ('FALSE', p.FALSE)

    @_('TRUE')
    def factor(self, p):
        return ('TRUE', p.TRUE)

    @_('INT')
    def factor(self, p):
        return ('INT', p.INT)

    @_('FLOAT')
    def factor(self, p):
        return ('FLOAT', p.FLOAT)

    @_('ID attribute_list')
    def factor(self, p):
        return ('ATTRIBUTE', p.ID) + p.attribute_list

    @_('DOT ID attribute_list')
    def attribute_list(self, p):
        return (p.ID,) + p.attribute_list

    @_('DOT DOLLAR_LBRACE expr RBRACE attribute_list')
    def attribute_list(self, p):
        return (('EXPRESSION', p.expr),)

    @_('empty')
    def attribute_list(self, p):
        return ()

    @_('')
    def empty(self, p):
        pass

    def error(self, p):
        if p:
            raise YaccError(f'Syntax error at line {p.lineno}, token={p.type}, value={p.value}\n')
        else:
            raise YaccError('Parse error in input. EOF\n')

    def parse(self, text):
        lexer = NixLexer()
        tokens = lexer.tokenize(text)
        tree = super().parse(tokens)
        return tree


#     @_('NOT expr')
#     def expr(self, p):
#         return FunctionNode('NOT', p.expr)

#     @_('MINUS expr %prec UMINUS')
#     def expr(self, p):
#         return FunctionNode('UMINUS', p.expr)

#     @_('LPAREN expr RPAREN')
#     def expr(self, p):
#         return p.expr

#     @_('IDENTIFIER LPAREN empty RPAREN')
#     def expr(self, p):
#         return FunctionNode(p.IDENTIFIER)

#     @_('IDENTIFIER LPAREN expr list_args RPAREN')
#     def expr(self, p):
#         p.list_args.append(p.expr)
#         return FunctionNode(p.IDENTIFIER, *p.list_args[::-1])

#     @_('IF expr THEN expr if_expr END')
#     def expr(self, p):
#         p.if_expr.append((p.expr0, p.expr1))
#         conditions = []
#         values = []
#         default = ValueNode('NULL', None)
#         for expr0, expr1 in p.if_expr:
#             if expr0 == '__default__':
#                 default = expr1
#             else:
#                 conditions.append(expr0)
#                 values.append(expr1)
#         return ConditionNode(conditions, values, default)

#     @_('ELSEIF expr THEN expr if_expr')
#     def if_expr(self, p):
#         p.if_expr.append((p.expr0, p.expr1))
#         return p.if_expr

#     @_('ELSE expr')
#     def if_expr(self, p):
#         return [('__default__', p.expr)]

#     @_('empty')
#     def if_expr(self, p):
#         return []

#     @_('CASE COLUMN WHEN factor THEN factor case_expr END')
#     def expr(self, p):
#         p.case_expr.append((p.factor0, p.factor1))
#         conditions = []
#         values = []
#         default = ValueNode('NULL', None)
#         for factor, value in p.case_expr:
#             if factor == '__default__':
#                 default = value
#             else:
#                 conditions.append(FunctionNode('EQUAL', p.COLUMN, factor))
#                 values.append(value)
#         return ConditionNode(conditions, values, default)

#     @_('WHEN factor THEN factor case_expr')
#     def case_expr(self, p):
#         p.case_expr.append((p.factor0, p.factor1))
#         return p.case_expr

#     @_('ELSE factor')
#     def case_expr(self, p):
#         return [('__default__', p.factor)]

#     @_('empty')
#     def case_expr(self, p):
#         return []

#     @_('factor')
#     def expr(self, p):
#         return p.factor

#     @_('INTEGER',
#        'FLOAT',
#        'COLUMN',
#        'TRUE',
#        'FALSE',
#        'NULL',
#        'STRING',
#        'DATETIME')
#     def factor(self, p):
#         return p[0]

#     @_('LBRACKET expr RBRACKET')
#     def expr(self, p):
#         return LODNode('FIXED', [], p.expr)

#     @_('LBRACKET lod_factor COLON expr RBRACKET')
#     def expr(self, p):
#         return LODNode(p.lod_factor, [ ], p.expr)

#     @_('LBRACKET lod_factor expr list_args COLON expr RBRACKET')
#     def expr(self, p):
#         p.list_args.append(p.expr0)
#         return LODNode(p.lod_factor, p.list_args[::-1], p.expr1)

#     @_('FIXED',
#        'EXCLUDE',
#        'INCLUDE')
#     def lod_factor(self, p):
#         return p[0]

#     @_('COMMA expr list_args')
#     def list_args(self, p):
#         p.list_args.append(p.expr)
#         return p.list_args

#     @_('empty')
#     def list_args(self, p):
#         return []

#     @_('')
#     def empty(self, p):
#         pass

#     def error(self, p):
#         if p:
#             raise YaccError(f'Syntax error at line {p.lineno}, token={p.type}, value={p.value}\n')
#         else:
#             raise YaccError('Parse error in input. EOF\n')

#     def parse(self, text):
#         lexer = TableauLexer()
#         tokens = lexer.tokenize(text)
#         tree = super().parse(tokens)
#         return tree
