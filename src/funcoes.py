import random
 
PERGUNTAS = [
    {
        "pergunta": "Qual tipo de dado usamos para representar números inteiros em Python?",
        "opcoes": ["INT", "FLOAT", "STR", "BOOL"],
        "resposta": "int"
    },
    {
        "pergunta": "Qual operador usamos para multiplicação em Python?",
        "opcoes": ["*", "**", "x", "."],
        "resposta": "*"
    },
    {
        "pergunta": "Qual função usamos para imprimir algo na tela em Python?",
        "opcoes": ["PRINT", "INPUT", "VAR", "SHOW"],
        "resposta": "print"
    },
    {
        "pergunta": "Qual operador verifica a igualdade entre dois valores em Python?",
        "opcoes": ["==", "=", "!=", ">"],
        "resposta": "=="
    },
    {
        "pergunta": "Qual palavra reservada usamos para criar uma função em Python?",
        "opcoes": ["DEF", "FUNC", "FUNCTION", "CREATE"],
        "resposta": "def"
    },
]
 
 
def gerar_matriz_embaralhada():
    """Cria uma lista com as opções de cada pergunta embaralhadas."""
    matriz = []
    for pergunta in PERGUNTAS:
        opcoes = pergunta["opcoes"][:]
        random.shuffle(opcoes)
        matriz.append(opcoes)
    return matriz
 
 
def obter_pergunta(indice):
    """Retorna o texto da pergunta formatado com o número."""
    return "PERGUNTA NÚMERO " + str(indice + 1) + ": " + PERGUNTAS[indice]["pergunta"]
 
 
def verificar_resposta(pergunta_indice, resposta_usuario):
    """Verifica se a resposta do usuário está correta."""
    resposta_correta = PERGUNTAS[pergunta_indice]["resposta"].lower()
    return resposta_usuario.lower() == resposta_correta
 
 
def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos
 
 
def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano
 
 
def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0
 
 
def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor
 
 
def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)
