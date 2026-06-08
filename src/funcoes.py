import random

PERGUNTAS = [
    "Qual tipo de dado usamos para representar números inteiros em Python?",
    "Qual operador usamos para multiplicação em Python?",
    "Qual função usamos para imprimir algo na tela em Python?",
    "Qual operador verifica a igualdade entre dois valores em Python?",
    "Qual palavra reservada usamos para criar uma função em Python?",
]

RESPOSTAS_CORRETAS = ["int", "*", "print", "==", "def"]

MATRIZ_OPCOES = [
    ["INT", "FLOAT", "STR", "BOOL"],
    ["*", "**", "x", "."],
    ["PRINT", "INPUT", "VAR", "SHOW"],
    ["==", "=", "!=", ">"],
    ["DEF", "FUNC", "FUNCTION", "CREATE"],
]


def gerar_matriz_embaralhada():
    """Cria uma cópia da matriz de opções e embaralha cada linha."""
    matriz = [opcoes[:] for opcoes in MATRIZ_OPCOES]
    for linha in matriz:
        random.shuffle(linha)
    return matriz


def obter_pergunta(indice):
    """Retorna a pergunta formatada com o número."""
    return f"PERGUNTA NÚMERO {indice + 1}: \n{PERGUNTAS[indice]}"


def verificar_resposta(pergunta_indice, resposta_usuario, opcoes_embaralhadas):
    """Verifica se a resposta do usuário está correta."""
    resposta_usuario_lower = resposta_usuario.lower()
    resposta_correta = RESPOSTAS_CORRETAS[pergunta_indice].lower()
    return resposta_usuario_lower == resposta_correta


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
