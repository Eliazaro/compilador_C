from analisadorLexico import AnalisadorLexico   
import sys

def ler_arquivo():
    if len(sys.argv) < 2:
        print("Uso: python script.py arquivo.c")
        return

    caminho = sys.argv[1]    
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            return conteudo
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
        return None

if __name__ == "__main__":
    codigo_fonte = ler_arquivo()
    analisador = AnalisadorLexico(codigo_fonte)
    analisador.analisar()

print(f"{'\nTABELA FINAL':^80}\n" + "-"*80)
for t in analisador.get_tokens():
    print(t)