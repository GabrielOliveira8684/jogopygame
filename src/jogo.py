try:
    import pygame
except ImportError as e:
    raise ImportError("The 'pygame' package is required to run this game. Install it with: pip install pygame") from e
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
    CAMINHO_RANKING,
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
    salvar_ranking,
    carregar_ranking,
)
 
TEMPO_POR_PERGUNTA = 30  # segundos
 
 
def desenhar_texto_centralizado(tela, texto, fonte, cor, y):
    """Renderiza texto centralizado horizontalmente na tela."""
    superficie = fonte.render(texto, True, cor)
    x = (LARGURA_TELA - superficie.get_width()) // 2
    tela.blit(superficie, (x, y))
 
 
def tela_digitar_nome(tela, fonte_grande, fonte_pequena, relogio):
    """Exibe uma tela para o jogador digitar o nome antes de começar."""
    nome = ""
    rodando = True
    while rodando:
        relogio.tick(FPS)
        tela.fill(BRANCO)
        desenhar_texto_centralizado(tela, "Digite seu nome:", fonte_grande, PRETO, 250)
        desenhar_texto_centralizado(tela, nome + "|", fonte_grande, AZUL, 330)
        desenhar_texto_centralizado(tela, "Pressione ENTER para confirmar", fonte_pequena, CINZA, 430)
 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome.strip():
                    return nome.strip()
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif len(nome) < 20 and evento.unicode.isprintable():
                    nome += evento.unicode
 
        pygame.display.flip()
    return None
 
 
def tela_ranking(tela, fonte_grande, fonte_pequena, relogio):
    """Exibe o ranking dos melhores jogadores."""
    entradas = carregar_ranking(CAMINHO_RANKING)
    rodando = True
    while rodando:
        relogio.tick(FPS)
        tela.fill(BRANCO)
        desenhar_texto_centralizado(tela, "🏆  RANKING  🏆", fonte_grande, AZUL, 60)
 
        if not entradas:
            desenhar_texto_centralizado(tela, "Nenhum jogador ainda!", fonte_pequena, CINZA, 200)
        else:
            for i, (nome, pts) in enumerate(entradas):
                texto = f"{i + 1}. {nome}  —  {pts} pts"
                cor = AZUL if i == 0 else PRETO
                y = 140 + i * 45
                desenhar_texto_centralizado(tela, texto, fonte_pequena, cor, y)
 
        desenhar_texto_centralizado(tela, "Clique para voltar ao menu", fonte_pequena, CINZA, 620)
 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.MOUSEBUTTONDOWN or evento.type == pygame.KEYDOWN:
                return
 
        pygame.display.flip()
 
 
def executar_jogo():
    """Executa o loop principal do jogo de perguntas."""
    pygame.init()
 
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
 
    relogio = pygame.time.Clock()
    fonte_grande = pygame.font.Font(None, TAMANHO_FONTE_GRANDE)
    fonte_pequena = pygame.font.Font(None, TAMANHO_FONTE_PEQUENA)
 
    # ── Estados possíveis ──────────────────────────────────────────────────
    # "menu"    → tela inicial
    # "nome"    → digitar nome
    # "jogando" → partida em andamento
    # "derrota" → errou uma pergunta
    # "vitoria" → acertou todas
    # "ranking" → exibe ranking
    estado = "menu"
 
    nome_jogador = ""
    pergunta_atual = 0
    respondida = False
    pontos = 0
    recorde = carregar_recorde(CAMINHO_RECORDE)
 
    mensagem = ""
    contador_mensagem = 0
 
    matriz_opcoes = gerar_matriz_embaralhada()
    rects_botoes = []
 
    # Cronômetro
    tempo_restante = TEMPO_POR_PERGUNTA
    ultimo_tick = pygame.time.get_ticks()
 
    # Elemento decorativo animado
    elemento_x = 0
    elemento_velocidade = 5
 
    rodando = True
    while rodando:
        relogio.tick(FPS)
        agora = pygame.time.get_ticks()
 
        # ── Cronômetro (só conta durante a partida, antes de responder) ────
        if estado == "jogando" and not respondida:
            if agora - ultimo_tick >= 1000:
                tempo_restante -= 1
                ultimo_tick = agora
                if tempo_restante <= 0:
                    estado = "derrota"
                    mensagem = "Tempo esgotado!"
 
        # ── Eventos ────────────────────────────────────────────────────────
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
 
            # Menu
            if estado == "menu" and evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Botão Jogar  (rect aproximado)
                if 350 <= mouse_x <= 650 and 380 <= mouse_y <= 430:
                    nome_jogador = tela_digitar_nome(tela, fonte_grande, fonte_pequena, relogio)
                    if nome_jogador is None:
                        rodando = False
                    else:
                        # Reinicia partida
                        pergunta_atual = 0
                        pontos = 0
                        respondida = False
                        matriz_opcoes = gerar_matriz_embaralhada()
                        tempo_restante = TEMPO_POR_PERGUNTA
                        ultimo_tick = pygame.time.get_ticks()
                        estado = "jogando"
 
                # Botão Ranking
                if 350 <= mouse_x <= 650 and 460 <= mouse_y <= 510:
                    tela_ranking(tela, fonte_grande, fonte_pequena, relogio)
 
            # Jogando — clicar em opção
            if (
                estado == "jogando"
                and evento.type == pygame.MOUSEBUTTONDOWN
                and not respondida
                and pergunta_atual < len(PERGUNTAS)
            ):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, botao in enumerate(rects_botoes):
                    if botao.collidepoint(mouse_x, mouse_y):
                        resposta_usuario = matriz_opcoes[pergunta_atual][i].lower()
                        respondida = True
 
                        if verificar_resposta(pergunta_atual, resposta_usuario, matriz_opcoes[pergunta_atual]):
                            pontos = calcular_pontos(pontos, 1)
                            mensagem = "CORRETO!"
                            contador_mensagem = 90
                        else:
                            estado = "derrota"
                            mensagem = "Resposta errada!"
 
            # Jogando — avançar pergunta após resposta correta
            if estado == "jogando" and evento.type == pygame.MOUSEBUTTONDOWN and respondida:
                pergunta_atual += 1
                respondida = False
                mensagem = ""
                contador_mensagem = 0
                tempo_restante = TEMPO_POR_PERGUNTA
                ultimo_tick = pygame.time.get_ticks()
 
                if pergunta_atual >= len(PERGUNTAS):
                    estado = "vitoria"
 
            # Telas de fim — clicar volta ao menu
            if estado in ("derrota", "vitoria") and evento.type == pygame.MOUSEBUTTONDOWN:
                # Salva ranking e recorde
                if nome_jogador:
                    salvar_ranking(CAMINHO_RANKING, nome_jogador, pontos)
                if pontos > recorde:
                    recorde = pontos
                    salvar_recorde(CAMINHO_RECORDE, recorde)
                estado = "menu"
 
        # ── Desenho ────────────────────────────────────────────────────────
        tela.fill(BRANCO)
 
        # Elemento decorativo
        elemento_x += elemento_velocidade
        if elemento_x > LARGURA_TELA:
            elemento_x = -20
        pygame.draw.circle(tela, AZUL, (elemento_x, 50), 10)
 
        # ── MENU ───────────────────────────────────────────────────────────
        if estado == "menu":
            desenhar_texto_centralizado(tela, "BEM-VINDO AO JOGO DE PERGUNTAS PYTHON!", fonte_grande, PRETO, 200)
            desenhar_texto_centralizado(tela, "Acerte todas as perguntas para se tornar Engenheiro!", fonte_pequena, CINZA, 270)
            desenhar_texto_centralizado(tela, f"Recorde atual: {recorde} pts", fonte_pequena, AZUL, 320)
 
            # Botão Jogar
            pygame.draw.rect(tela, VERDE, (350, 380, 300, 50), border_radius=8)
            desenhar_texto_centralizado(tela, "JOGAR", fonte_grande, BRANCO, 390)
 
            # Botão Ranking
            pygame.draw.rect(tela, AZUL, (350, 460, 300, 50), border_radius=8)
            desenhar_texto_centralizado(tela, "RANKING", fonte_grande, BRANCO, 470)
 
        # ── JOGANDO ────────────────────────────────────────────────────────
        elif estado == "jogando" and pergunta_atual < len(PERGUNTAS):
            # Cabeçalho
            texto_jogador = fonte_pequena.render(f"Jogador: {nome_jogador}", True, PRETO)
            tela.blit(texto_jogador, (50, 15))
 
            texto_pontos = fonte_pequena.render(f"Pontos: {pontos}", True, PRETO)
            tela.blit(texto_pontos, (LARGURA_TELA - 200, 15))
 
            # Cronômetro com cor de alerta
            cor_tempo = VERMELHO if tempo_restante <= 10 else PRETO
            texto_tempo = fonte_grande.render(f"⏱ {tempo_restante}s", True, cor_tempo)
            tela.blit(texto_tempo, (LARGURA_TELA // 2 - 40, 10))
 
            # Pergunta
            pergunta = obter_pergunta(pergunta_atual)
            texto_pergunta = fonte_pequena.render(pergunta, True, PRETO)
            tela.blit(texto_pergunta, (50, 85))
 
            # Botões de opção
            rects_botoes = []
            for i, opcao in enumerate(matriz_opcoes[pergunta_atual]):
                y = 220 + i * 90
                cor_botao = CINZA
                if respondida:
                    cor_botao = VERDE if opcao.lower() in [r.lower() for r in [opcao] if verificar_resposta(pergunta_atual, opcao.lower(), matriz_opcoes[pergunta_atual])] else CINZA
                rect = pygame.draw.rect(tela, cor_botao, (100, y, 800, 70), border_radius=8)
                rects_botoes.append(rect)
                texto_opcao = fonte_pequena.render(opcao, True, PRETO)
                tela.blit(texto_opcao, (120, y + 22))
 
            # Mensagem de acerto
            if respondida and contador_mensagem > 0:
                desenhar_texto_centralizado(tela, mensagem, fonte_grande, VERDE, 590)
                desenhar_texto_centralizado(tela, "Clique para próxima pergunta", fonte_pequena, PRETO, 640)
                contador_mensagem -= 1
 
        # ── DERROTA ────────────────────────────────────────────────────────
        elif estado == "derrota":
            pygame.draw.rect(tela, VERMELHO, (100, 150, 800, 400), border_radius=16)
            desenhar_texto_centralizado(tela, "GAME OVER!", fonte_grande, BRANCO, 200)
            desenhar_texto_centralizado(tela, mensagem, fonte_pequena, BRANCO, 270)
            desenhar_texto_centralizado(tela, f"Você fez {pontos} ponto(s)", fonte_grande, BRANCO, 340)
            desenhar_texto_centralizado(tela, f"Recorde: {recorde} pts", fonte_pequena, BRANCO, 410)
            desenhar_texto_centralizado(tela, "Clique para voltar ao menu", fonte_pequena, BRANCO, 490)
 
        # ── VITÓRIA ────────────────────────────────────────────────────────
        elif estado == "vitoria":
            pygame.draw.rect(tela, VERDE, (100, 150, 800, 400), border_radius=16)
            desenhar_texto_centralizado(tela, "PARABÉNS, ENGENHEIRO(A)!", fonte_grande, BRANCO, 200)
            desenhar_texto_centralizado(tela, f"Você acertou todas as perguntas!", fonte_pequena, BRANCO, 270)
            desenhar_texto_centralizado(tela, f"Pontuação: {pontos} pts", fonte_grande, BRANCO, 340)
            if pontos > recorde:
                desenhar_texto_centralizado(tela, "🏆 NOVO RECORDE!", fonte_grande, PRETO, 410)
            else:
                desenhar_texto_centralizado(tela, f"Recorde: {recorde} pts", fonte_pequena, BRANCO, 410)
            desenhar_texto_centralizado(tela, "Clique para voltar ao menu", fonte_pequena, BRANCO, 490)
 
        pygame.display.flip()
 
    pygame.quit()