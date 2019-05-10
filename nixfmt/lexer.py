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

    @_(r'#.*|\/\*([^*]|\*+[^*/])*\*+\/')
    def COMMENT(self, t):
        return t

    @_(r'"')
    def STRING_QUOTE(self, t):
        self.push_state(NixStringLexer)
        return t

    @_(r"''")
    def INDENTED_STRING_QUOTE(self, t):
        self.push_state(NixIndentedStringLexer)
        return t

    @_(r'(([1-9]\d*\.\d*)|(0?\.\d+))([Ee][+-]?\d+)?')
    def FLOAT(self, t):
        return t

    @_(r'\d+')
    def INT(self, t):
        return t

    @_(r'[\w.\-+]*(\/[\w.\-+]+)+\/?')
    def PATH(self, t):
        return t

    @_(r'\~(\/[\w.\-+]+)+\/?')
    def HPATH(self, t):
        return t

    @_(r'\<[\w.\-+]+(\/[\w.\-+]+)*\>')
    def SPATH(self, t):
        return t

    @_(r'[a-zA-Z][a-zA-Z0-9+\-.]*\:[a-zA-Z0-9\%\/\?\:\@\&\=\+\$\,\-\_\.\!\~\*\']+')
    def URI(self, t):
        return t

    @_(r'[a-zA-Z_][\w\'-]*')
    def ID(self, t):
        keywords = {
            'null': 'NULL',
            'true': 'TRUE',
            'false': 'FALSE',
            'abort': 'ABORT',
            'assert': 'ASSERT',
            'import': 'IMPORT',
            'inherit': 'INHERIT',
            'with': 'WITH',
            'let': 'LET',
            'in': 'IN',
            'if': 'IF',
            'then': 'THEN',
            'else': 'ELSE',
            'rec': 'REC',
            'or': 'OR_KW'
        }
        if t.value in keywords:
            t.type = keywords[t.value]
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

    @_(r'\s+')
    def WHITESPACE(self, t):
        self.lineno += t.value.count('\n')
        return t

    def tokenize(self, text):
        return super().tokenize(text)

    def error(self, t):
        raise LexError(f"(NixLexer) Illegal character '({t.value[0]}){t.value[1:10]}' and lineno {t.lineno} and index {self.index}", t.value, self.index)


class NixStringLexer(sly.Lexer):
    tokens = { STRING }

    @_(r'\$\{')
    def DOLLAR_LBRACE(self, t):
        self.push_state(NixLexer)
        return t

    @_(r'(?:[^\$"\\]|\$[^\$\{"]|\\[\s\S])+')
    def STRING(self, t):
        self.lineno += t.value.count('\n')
        return t

    @_('"')
    def STRING_QUOTE(self, t):
        self.pop_state()
        return t

    @_(r'\$')
    def STRING_1(self, t):
        t.type = 'STRING'
        return t

    def error(self, t):
        raise LexError(f"(NixStringLexer) Illegal character '({t.value[0]}){t.value[1:10]}' and lineno {t.lineno} and index {self.index}", t.value, self.index)


class NixIndentedStringLexer(sly.Lexer):
    tokens = { INDENTED_STRING }

    @_(r'\$\{')
    def DOLLAR_LBRACE(self, t):
        self.push_state(NixLexer)
        return t

    @_(r"(?:[^'\$]|'[^'\$]|\$[^\$\{']|''[^;\}\)\]\s])+")
    def INDENTED_STRING(self, t):
        self.lineno += t.value.count('\n')
        return t

    @_(r"''")
    def INDENTED_STRING_QUOTE(self, t):
        self.pop_state()
        return t

    @_(r"\$")
    def INDENTED_STRING_1(self, t):
        t.type = 'INDENTED_STRING'
        return t

    @_(r"'")
    def INDENTED_STRING_2(self, t):
        t.type = 'INDENTED_STRING'
        return t

    def error(self, t):
        raise LexError(f"(NixIndentedStringLexer) Illegal character '({t.value[0]}){t.value[1:10]}' and lineno {t.lineno} and index {self.index}", t.value, self.index)
