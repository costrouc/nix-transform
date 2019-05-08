import sly
from sly.yacc import YaccError


# class TableauParser(sly.Parser):
#     tokens = TableauLexer.tokens

#     precedence = (
#         ('left', 'OR'),
#         ('left', 'AND'),
#         ('nonassoc', 'LT', 'GT', 'GTEQ', 'LTEQ', 'NEQ', 'EQ'),
#         ('left', 'PLUS', 'MINUS'),
#         ('left', 'TIMES', 'DIVIDE'),
#         ('left', 'POWER'),
#         ('right', 'UMINUS', 'NOT')
#     )

#     @_('expr PLUS expr',
#        'expr MINUS  expr',
#        'expr TIMES  expr',
#        'expr DIVIDE expr',
#        'expr POWER expr',
#        # comparison operation
#        'expr LT   expr',
#        'expr LTEQ expr',
#        'expr NEQ  expr',
#        'expr EQ   expr',
#        'expr GT   expr',
#        'expr GTEQ expr',
#        # boolean operation
#        'expr AND expr',
#        'expr OR expr')
#     def expr(self, p):
#         op_map = {
#             '+': 'PLUS',
#             '-': 'SUBTRACT',
#             '*': 'MULTIPLY',
#             '/': 'DIVIDE',
#             '^': 'POWER',
#             '<': 'LESSTHAN',
#             '<=': 'LESSTHANEQUAL',
#             '<>': 'NOTEQUAL',
#             '!=': 'NOTEQUAL',
#             '=': 'EQUAL',
#             '==': 'EQUAL',
#             '>': 'GREATERTHAN',
#             '>=': 'GREATERTHANEQUAL',
#             'AND': 'AND',
#             'OR': 'OR',
#         }
#         return FunctionNode(op_map[p[1]], p.expr0, p.expr1)

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
