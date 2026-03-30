import re

class Token:
    def __init__(self, tipo, codigo, conteudo, linha, coluna):
        self.tipo = tipo
        self.codigo = codigo
        self.conteudo = conteudo
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        # Formatação para impressão no terminal
        return (f"Token (Tipo: {self.tipo:18} | Código: {self.codigo} | "
                f"Conteúdo: {self.conteudo:10} | Linha: {self.linha} | Coluna: {self.coluna})")

class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.pivo = 0
        self.batedor = 0
        self.linha = 1
        self.coluna = 1
        self.tokens = []
        self.delimitadores = "(){}[],;+-*/=<>!&| \n\t\""
        
        # Mapeamento numérico de tipos
        self.codigos = {
            'PALAVRA_RESERVADA': 1,
            'IDENTIFICADOR': 2,
            'OPERADOR': 3,
            'SEPARADOR': 4,
            'NUMERO': 5,
            'LITERAL': 6,
        }
        
        self.palavras_reservadas = {'if', 'else', 'while', 'for', 'return', 'int', 'float', 'string', 'void', 'printf', 'bool'}
        
        # Expressões Regulares
        self.operadores = re.compile(r'==|!=|<=|>=|&&|\|\||[+\-*/=<>]')  
        self.separadores = re.compile(r'[()\{\},;]')
        self.comentarios = re.compile(r'//.*|/\*[\s\S]*?\*/')
        self.identificadores = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
        self.numeros = re.compile(r'\d+(\.\d+)?')
        self.literais = re.compile(r'"([^"\\\n]|\\.)*"')



    def move_cursor(self, texto):
        for char in texto:
            if char == '\n':
                self.linha += 1
                self.coluna = 1
            else:
                self.coluna += 1
        self.batedor += len(texto)

    def ajustar_pivo(self):
        self.pivo = self.batedor
        
    def verifica_erro(self):
        posicao_aux = self.batedor    
        while (posicao_aux < len(self.codigo_fonte) and 
            self.codigo_fonte[posicao_aux] not in self.delimitadores):
            posicao_aux += 1
    
        token_invalido = self.codigo_fonte[self.pivo : posicao_aux]
    
        return token_invalido


    def analisar(self):
        while self.batedor < len(self.codigo_fonte):
            char_atual = self.codigo_fonte[self.batedor]

            # Ignora espaços em branco
            if char_atual.isspace():
                self.move_cursor(char_atual)
                self.ajustar_pivo()
                continue

            linha_atual = self.linha
            coluna_atual = self.coluna

            # Comentários
            if char_atual == "/":
                match = self.comentarios.match(self.codigo_fonte, self.batedor)
                
                if match:
                    conteudo = match.group()
                    self.move_cursor(conteudo)
                    self.ajustar_pivo()
                    continue
                else:
                    proximo_char = self.codigo_fonte[self.batedor+1 : self.batedor+2]
                    
                    if proximo_char == "*":
                        print(f"Comentário de bloco não fechado - Linha: {linha_atual}, Coluna: {coluna_atual}")
                        conteudo_errado = self.codigo_fonte[self.batedor:]
                        self.move_cursor(conteudo_errado)
                        self.ajustar_pivo()
                        continue
                
            
            # Literais
            if char_atual == '"':
                match = self.literais.match(self.codigo_fonte, self.batedor)
                if match:
                    conteudo = match.group()
                    self.tokens.append(Token("LITERAL", self.codigos["LITERAL"], conteudo, linha_atual, coluna_atual))
                    self.move_cursor(conteudo) # Move o cursor para o que está CERTO
                else:
                    posicao_fim_linha = self.codigo_fonte.find('\n', self.batedor + 1)
                    if posicao_fim_linha == -1: 
                        posicao_fim_linha = len(self.codigo_fonte)
                    
                    conteudo_errado = self.codigo_fonte[self.batedor : posicao_fim_linha]
                    print(f"Literal não fechado - Linha: {linha_atual}, Coluna: {coluna_atual}")
                    self.move_cursor(conteudo_errado)

                self.ajustar_pivo()
                continue

            # Operadores
            match = self.operadores.match(self.codigo_fonte, self.batedor)
            if match:
                conteudo = match.group()
                self.tokens.append(Token("OPERADOR", self.codigos["OPERADOR"], conteudo, linha_atual, coluna_atual))
                self.move_cursor(conteudo)
                self.ajustar_pivo()
                continue

            # Separadores
            match = self.separadores.match(self.codigo_fonte, self.batedor)
            if match:
                conteudo = match.group()
                self.tokens.append(Token("SEPARADOR", self.codigos["SEPARADOR"], conteudo, linha_atual, coluna_atual))
                self.move_cursor(conteudo)
                self.ajustar_pivo()
                continue

            # Números
            match = self.numeros.match(self.codigo_fonte, self.batedor)
            if match:
                conteudo = match.group()
                proxima_pos = self.batedor + len(conteudo)
                if self.codigo_fonte[proxima_pos] not in self.delimitadores:
                    token_invalido = self.verifica_erro()
                    print(f"Token numérico inválido: {token_invalido} - Linha: {linha_atual}, Coluna: {coluna_atual}")
                    self.move_cursor(token_invalido)
                else:
                    self.tokens.append(Token("NUMERO", self.codigos["NUMERO"], conteudo, linha_atual, coluna_atual))
                    self.move_cursor(conteudo)
                    self.ajustar_pivo()
                continue

            # Identificadores e Palavras Reservadas
            match = self.identificadores.match(self.codigo_fonte, self.batedor)
            if match:
                conteudo = match.group()
                proxima_pos = self.batedor + len(conteudo)
                if self.codigo_fonte[proxima_pos] not in self.delimitadores:
                    token_invalido = self.verifica_erro()
                    print(f"Token inválido: {token_invalido} - Linha: {linha_atual}, Coluna: {coluna_atual}")
                    self.move_cursor(token_invalido)
                else:
                    if conteudo in self.palavras_reservadas:
                        self.tokens.append(Token("PALAVRA_RESERVADA", self.codigos["PALAVRA_RESERVADA"], conteudo, linha_atual, coluna_atual))
                    else:
                        self.tokens.append(Token("IDENTIFICADOR", self.codigos["IDENTIFICADOR"], conteudo, linha_atual, coluna_atual))
                    self.move_cursor(conteudo)
                    self.ajustar_pivo()
                continue
            
            print(f"Caractere inválido: {char_atual} na Linha: {linha_atual}, Coluna: {coluna_atual}")
            self.move_cursor(char_atual)
            self.ajustar_pivo()

    def get_tokens(self):
        return self.tokens
