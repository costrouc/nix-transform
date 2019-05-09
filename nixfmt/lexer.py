import sly
from sly.lex import LexError


class NixLexer(sly.Lexer):
    tokens = {
        WHITESPACE, COMMENT,
        TRUE, FALSE,
        STRING, INDENTED_STRING,
        ID, INT, FLOAT, PATH, HPATH, SPATH, URI,
        ABORT, ASSERT, IMPORT, INHERIT, WITH,
        LET, IN,
        IF, THEN, ELSE, REC, ELLIPSIS,
        EQ, ASSIGN, NEQ, LEQ, LESS, GEQ, GREATER, AND, OR, OR_KW,
        IMPL, UPDATE, CONCAT,
        NOT,
        DOT,
        PLUS, MINUS, TIMES, DIVIDE,
        DEFAULT,
        AT,
        DOLLAR_LBRACE,
        LBRACE, RBRACE,
        LBRACKET, RBRACKET,
        LPAREN, RPAREN,
        SEMICOLON, COLON, COMMA
    }

    TRUE = r'true'
    FALSE = r'false'

    ABORT = r'abort'
    ASSERT = r'assert'
    IMPORT = r'import'
    INHERIT = r'inherit'
    WITH = r'with'

    LET = r'let'
    IN = r'in'

    IF = r'if'
    THEN = r'then'
    ELSE = r'else'
    REC = r'rec'

    OR_KW = 'or'

    @_(r'#.*|\/\*([^*]|\*+[^*/])*\*+\/')
    def COMMENT(self, t):
        return t

    @_(r'"[^"]*"')
    def STRING(self, t):
        return t

    @_(r'\'\'([^\']|\'+[^\'])*\'+\'')
    def INDENTED_STRING(self, t):
        return t

    @_(r'(([1-9][0-9]*\.[0-9]*)|(0?\.[0-9]+))([Ee][+-]?[0-9]+)?')
    def FLOAT(self, t):
        return t

    @_(r'[0-9]+')
    def INT(self, t):
        t.value = int(t.value)
        return t

    @_(r'[a-zA-Z0-9\.\_\-\+]*(\/[a-zA-Z0-9\.\_\-\+]+)+\/?')
    def PATH(self, t):
        return t

    @_(r'\~(\/[a-zA-Z0-9\.\_\-\+]+)+\/?')
    def HPATH(self, t):
        return t

    @_(r'\<[a-zA-Z0-9\.\_\-\+]+(\/[a-zA-Z0-9\.\_\-\+]+)*\>')
    def SPATH(self, t):
        return t

    @_(r'[a-zA-Z][a-zA-Z0-9\+\-\.]*\:[a-zA-Z0-9\%\/\?\:\@\&\=\+\$\,\-\_\.\!\~\*\']+')
    def URI(self, t):
        return t

    @_('[a-zA-Z\_][a-zA-Z0-9\_\'\-]*')
    def ID(self, t):
        return t

    ELLIPSIS = r'\.\.\.'

    EQ = r'\=\='
    ASSIGN = r'\='
    NEQ = r'\!\='
    LEQ = r'\<\='
    LESS = r'\<'
    GEQ = r'\>\='
    GREATER = r'\>'
    AND = r'\&\&'
    OR = r'\|\|'

    IMPL = r'\-\>'
    UPDATE = r'\/\/'
    CONCAT = r'\+\+'

    AT = r'\@'
    DOLLAR_LBRACE = r'\$\{'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r'\;'
    COLON = r'\:'
    COMMA = r','

    NOT = r'!'

    PLUS = r'\+'
    MINUS = r'\-'
    TIMES = r'\*'
    DIVIDE = r'\/'

    DOT = r'\.'

    DEFAULT = r'\?'

    @_(r'[ \t\r\n]+')
    def WHITESPACE(self, t):
        self.lineno += t.value.count('\n')
        return t

    def tokenize(self, text):
        return super().tokenize(text)

    def error(self, t):
        raise LexError(f"Illegal character '{t.value[0]}' and lineno {t.lineno} and index {self.index}", t.value, self.index)
