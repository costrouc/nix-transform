import sly
from sly.lex import LexError


class NixLexer(sly.Lexer):
    tokens = {
        WHITESPACE, COMMENT,
        TRUE, FALSE,
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

    # TODO
    @_(r'#.*|\/\*([^*]|\*+[^*/])*\*+\/')
    def COMMENT(self, t):
        return t

    @_(r'"')
    def STRING_QUOTE(self, t):
        self.push_state(NixStringLexer)
        return t

    @_(r'\'\'')
    def INDENTED_STRING_QUOTE(self, t):
        self.push_state(NixIndentedStringLexer)
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
    LBRACKET = r'\['
    RBRACKET = r'\]'

    @_(r'\$\{')
    def DOLLAR_LBRACE(self, t):
        self.push_state(NixLexer)
        return t

    @_(r'\{')
    def LBRACE(self, t):
        self.push_state(NixLexer)
        return t

    @_(r'\}')
    def RBRACE(self, t):
        self.pop_state()
        return t

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
        raise LexError(f"Illegal character '({t.value[0]}){t.value[1:10]}' and lineno {t.lineno} and index {self.index}", t.value, self.index)


class NixStringLexer(sly.Lexer):
    tokens = { STRING }

    # TODO
    STRING = r'([^\$\"\\]|\$[^\{\"\\]|\$\\[.\n]|\\")+'

    @_(r'\$\{')
    def DOLLAR_LBRACE(self, t):
        self.push_state(NixLexer)
        return t

    @_('"')
    def STRING_QUOTE(self, t):
        self.pop_state()
        return t


class NixIndentedStringLexer(sly.Lexer):
    tokens = { INDENTED_STRING }

    # TODO
    INDENTED_STRING = r"([^$']|$[^\{']|'[^'$]|''.)+"

    @_(r'\$\{')
    def DOLLAR_LBRACE(self, t):
        self.push_state(NixLexer)
        return t

    @_(r'\'\'')
    def INDENTED_STRING_QUOTE(self, t):
        self.pop_state()
        return t
