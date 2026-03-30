/* === TESTE DE ERROS LÉXICOS ESSENCIAIS === */

// 1. Identificadores Válidos e Reservadas
int main() {
    "Literal de string válido";
    int teste = (x === y);
    int variavel1 = 5;
    float _variavel2 = 3.14;
    int nota1 = variavel1 + _variavel2;
    if (nota1 >= 7){
        return 0;
    }
    else 
        return 1;
}

// 2. Símbolos Inválidos (Não pertencem à linguagem)
@
#
$
?

// 3. Literais com erros comuns
"Literal sem fechamento de aspas

// 4. Números malformados (Erros de ponto flutuante)
15.              // Ponto sem dígito depois
45.67.89         // Dois pontos no mesmo número
10..5            // Pontos seguidos

// 5. Identificadores que começam com números
88_variavel_errada
7tipo_invalido
v@riavel_errada

// 6. Comentário de bloco que nunca fecha
/* Este comentário começa aqui
e o arquivo acaba sem o fechamento de bloco