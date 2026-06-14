import pygame
import random

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    BRANCO,
    PRETO,
    CINZA,
    AZUL,
    VERDE,
    VERMELHO,
    TAMANHO_FONTE_GRANDE,
    TAMANHO_FONTE_PEQUENA,
    CAMINHO_RECORDE,
)

from src.funcoes import (
    gerar_matriz_embaralhada,
    obter_pergunta,
    verificar_resposta,
    calcular_pontos,
    PERGUNTAS,
    MATRIZ_OPCOES,
)

from src.dados import (
    salvar_recorde,
    carregar_recorde,
)


def executar_jogo():
    """Executa o loop principal do jogo de perguntas."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    fonte_grande = pygame.font.Font(None, TAMANHO_FONTE_GRANDE)
    fonte_pequena = pygame.font.Font(None, TAMANHO_FONTE_PEQUENA)

    rodando = True
    tela_menu = True
    pergunta_atual = 0
    respondida = False
    game_over = False

    pontos = 0
    recorde = carregar_recorde(CAMINHO_RECORDE)

    mensagem = ""
    contador_mensagem = 0

    matriz_opcoes = gerar_matriz_embaralhada()
    rects_botoes = []

    elemento_x = 0
    elemento_velocidade = 5

    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if tela_menu and evento.type == pygame.MOUSEBUTTONDOWN:
                tela_menu = False

            if (
                not tela_menu
                and evento.type == pygame.MOUSEBUTTONDOWN
                and not respondida
                and pergunta_atual < len(PERGUNTAS)
            ):
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for i, botao in enumerate(rects_botoes):
                    if botao.collidepoint(mouse_x, mouse_y):
                        resposta_usuario = matriz_opcoes[pergunta_atual][i].lower()
                        respondida = True

                        if verificar_resposta(
                            pergunta_atual,
                            resposta_usuario,
                            matriz_opcoes[pergunta_atual],
                        ):
                            pontos = calcular_pontos(pontos, 1)
                            mensagem = "CORRETO!"
                        else:
                            mensagem = "INCORRETO!"
                            game_over =  True

                        contador_mensagem = 120

            if evento.type == pygame.MOUSEBUTTONDOWN and respondida:
                pergunta_atual += 1
                respondida = False
                mensagem = ""
                contador_mensagem = 0

        tela.fill(BRANCO)

        elemento_x += elemento_velocidade
        if elemento_x > LARGURA_TELA:
            elemento_x = -20
        pygame.draw.circle(tela, AZUL, (elemento_x, 50), 10)

        if tela_menu:
            texto_titulo = fonte_grande.render(
                "BEM-VINDO AO JOGO DE PERGUNTAS PYTHON!", True, PRETO
            )
            tela.blit(texto_titulo, (100, 250))

            texto_objetivo = fonte_pequena.render(
                "SEU OBJETIVO E ACERTAR O MAXIMO DE PERGUNTAS POSSIVEIS", True, PRETO
            )
            tela.blit(texto_objetivo, (150, 350))

            texto_clique = fonte_pequena.render("Clique para começar", True, AZUL)
            tela.blit(texto_clique, (350, 450))

        elif pergunta_atual < len(PERGUNTAS):
            pergunta = obter_pergunta(pergunta_atual)
            texto_pergunta = fonte_pequena.render(pergunta, True, PRETO)
            tela.blit(texto_pergunta, (50, 80))

            rects_botoes = []
            for i, opcao in enumerate(matriz_opcoes[pergunta_atual]):
                y = 250 + i * 80
                rect = pygame.draw.rect(tela, CINZA, (100, y, 800, 70))
                rects_botoes.append(rect)

                texto_opcao = fonte_pequena.render(opcao, True, PRETO)
                tela.blit(texto_opcao, (120, y + 20))

            texto_pontos = fonte_pequena.render(f"Pontos: {pontos}", True, PRETO)
            tela.blit(texto_pontos, (50, 600))

            if respondida and contador_mensagem > 0:
                cor_msg = VERDE if "CORRETO" in mensagem else VERMELHO
                texto_msg = fonte_grande.render(mensagem, True, cor_msg)
                tela.blit(texto_msg, (300, 500))

                texto_continue = fonte_pequena.render(
                    "Clique para proxima pergunta", True, PRETO
                )
                tela.blit(texto_continue, (250, 570))

                contador_mensagem -= 1

        else:
            texto_final = fonte_grande.render("FIM DO JOGO!", True, PRETO)
            tela.blit(texto_final, (300, 150))

            texto_resultado = fonte_grande.render(
                f"Voce fez {pontos} pontos, PARABENS!", True, AZUL
            )
            tela.blit(texto_resultado, (150, 350))

            if pontos > recorde:
                recorde = pontos
                salvar_recorde(CAMINHO_RECORDE, recorde)

            texto_recorde = fonte_pequena.render(f"Recorde: {recorde}", True, PRETO)
            tela.blit(texto_recorde, (400, 450))

        pygame.display.flip()

    pygame.quit()
