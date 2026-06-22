import pygame
import math
import random

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    BRANCO,
    PRETO,
    CINZA,
    CINZA_ESCURO,
    AZUL,
    VERDE,
    VERMELHO,
    VERMELHO_ESCURO,
    AMARELO,
    OURO,
    PRATA,
    BRONZE,
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
)

from src.dados import (
    salvar_recorde,
    carregar_recorde,
    salvar_ranking,
    carregar_ranking,
)

TEMPO_POR_PERGUNTA = 30

# Cores extras para efeitos
VERDE_BRILHO   = (0, 255, 100)
AMARELO_BRILHO = (255, 240, 0)
OURO_BRILHO    = (255, 220, 50)
VERMELHO_BRILHO = (255, 60, 60)
LARANJA         = (255, 140, 0)



def desenhar_texto_centralizado(tela, texto, fonte, cor, y):
    superficie = fonte.render(texto, True, cor)
    x = (LARGURA_TELA - superficie.get_width()) // 2
    tela.blit(superficie, (x, y))


def desenhar_barra_tempo(tela, tempo_restante, tempo_total, x, y, largura, altura):
    """Barra que esvazia da direita para a esquerda conforme o tempo passa."""
    proporcao = max(0, min(1, tempo_restante / tempo_total))

    # Fundo (trilho)
    pygame.draw.rect(tela, CINZA, (x, y, largura, altura), border_radius=altura // 2)

    # Cor muda conforme urgência
    if proporcao > 0.5:
        cor_barra = VERDE
    elif proporcao > 0.2:
        cor_barra = AMARELO
    else:
        cor_barra = VERMELHO

    largura_preenchida = int(largura * proporcao)
    if largura_preenchida > 0:
        pygame.draw.rect(
            tela, cor_barra,
            (x, y, largura_preenchida, altura),
            border_radius=altura // 2,
        )

    # Brilho interno na barra 
    if largura_preenchida > 10:
        s = pygame.Surface((largura_preenchida - 4, altura // 3), pygame.SRCALPHA)
        s.fill((255, 255, 255, 60))
        tela.blit(s, (x + 2, y + 2))

    # Contorno
    pygame.draw.rect(tela, PRETO, (x, y, largura, altura), width=2, border_radius=altura // 2)

    # Texto de segundos centralizado na barra
    fonte_timer = pygame.font.Font(None, 26)
    texto_seg = fonte_timer.render(str(int(tempo_restante)) + "s", True, PRETO)
    tela.blit(texto_seg, (x + (largura - texto_seg.get_width()) // 2, y + (altura - texto_seg.get_height()) // 2))


def _gerar_pontos_boca(centro_x, centro_y, largura, curvatura, triste):
    pontos = []
    metade = largura / 2
    passos = 24
    for i in range(passos + 1):
        t = -1 + (2 * i / passos)
        if triste:
            y_offset = curvatura * (t ** 2)
        else:
            y_offset = curvatura * (1 - t ** 2)
        x = centro_x + t * metade
        y = centro_y + y_offset
        pontos.append((x, y))
    return pontos


def desenhar_rosto(tela, centro_x, centro_y, raio, triste=True):
    cor_rosto   = AMARELO
    cor_contorno = PRETO

    pygame.draw.circle(tela, cor_rosto, (int(centro_x), int(centro_y)), raio)
    pygame.draw.circle(tela, cor_contorno, (int(centro_x), int(centro_y)), raio, 4)

    offset_x = raio * 0.38
    offset_y = raio * 0.25
    raio_olho = max(5, int(raio * 0.09))
    olho_esq = (int(centro_x - offset_x), int(centro_y - offset_y))
    olho_dir = (int(centro_x + offset_x), int(centro_y - offset_y))
    pygame.draw.circle(tela, cor_contorno, olho_esq, raio_olho)
    pygame.draw.circle(tela, cor_contorno, olho_dir, raio_olho)

    if triste:
        sobr_y = int(centro_y - offset_y - raio_olho - 10)
        pygame.draw.line(tela, cor_contorno,
            (olho_esq[0] - 18, sobr_y - 6), (olho_esq[0] + 14, sobr_y + 6), 5)
        pygame.draw.line(tela, cor_contorno,
            (olho_dir[0] + 18, sobr_y - 6), (olho_dir[0] - 14, sobr_y + 6), 5)

        # Lágrima
        lx = olho_esq[0] - raio_olho
        ly = olho_esq[1] + raio_olho + 4
        pygame.draw.polygon(tela, AZUL,
            [(lx, ly), (lx - 7, ly + 16), (lx + 7, ly + 16)])
        pygame.draw.circle(tela, AZUL, (lx, ly + 16), 7)

    boca_y = centro_y + raio * 0.32
    pontos = _gerar_pontos_boca(centro_x, boca_y, raio * 1.1, raio * 0.35, triste)
    pygame.draw.lines(tela, cor_contorno, False, pontos, 6)



class FlashEfeito:

    def __init__(self):
        self.ativo   = False
        self.alpha   = 0
        self.cor     = (255, 255, 255)
        self.duracao = 0
        self.contador = 0

    def iniciar(self, cor, duracao_frames=30, alpha_inicial=180):
        self.ativo    = True
        self.cor      = cor
        self.duracao  = duracao_frames
        self.contador = 0
        self.alpha    = alpha_inicial

    def atualizar_e_desenhar(self, tela):
        if not self.ativo:
            return
        self.contador += 1
        progresso = self.contador / self.duracao
        alpha_atual = int(self.alpha * (1 - progresso))
        if alpha_atual <= 0 or self.contador >= self.duracao:
            self.ativo = False
            return
        s = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        s.fill((*self.cor, alpha_atual))
        tela.blit(s, (0, 0))


# ---------------------------------------------------------------------------
# Efeito de PARTÍCULAS (estrelinhas / confetes no recorde)
# ---------------------------------------------------------------------------

class Particula:
    def __init__(self, x, y, cor):
        angulo = random.uniform(0, 2 * math.pi)
        vel    = random.uniform(3, 9)
        self.x   = x
        self.y   = y
        self.vx  = math.cos(angulo) * vel
        self.vy  = math.sin(angulo) * vel - random.uniform(2, 6)
        self.cor = cor
        self.vida = random.randint(30, 60)
        self.raio = random.randint(3, 7)

    def atualizar(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.3  
        self.vida -= 1

    def desenhar(self, tela):
        if self.vida > 0:
            alpha = min(255, int(255 * self.vida / 40))
            s = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.cor, alpha), (self.raio, self.raio), self.raio)
            tela.blit(s, (int(self.x) - self.raio, int(self.y) - self.raio))


class SistemaParticulas:
    def __init__(self):
        self.particulas = []

    def explodir(self, x, y, quantidade=60):
        cores = [AMARELO_BRILHO, VERDE_BRILHO, OURO_BRILHO, BRANCO, LARANJA, AZUL]
        for _ in range(quantidade):
            cor = random.choice(cores)
            self.particulas.append(Particula(x, y, cor))

    def atualizar_e_desenhar(self, tela):
        vivos = []
        for p in self.particulas:
            p.atualizar()
            p.desenhar(tela)
            if p.vida > 0:
                vivos.append(p)
        self.particulas = vivos

    def limpar(self):
        self.particulas = []


# ---------------------------------------------------------------------------
# Efeito de PULSO no texto
# ---------------------------------------------------------------------------

def texto_pulsante(tela, texto, fonte_base, cor, y, tick, escala_max=1.15, velocidade=4):
    """Renderiza texto com tamanho pulsante usando math.sin."""
    fator = 1.0 + (escala_max - 1.0) * (0.5 + 0.5 * math.sin(tick * velocidade * 0.1))
    tamanho_base = fonte_base.size(texto)[1]
    tamanho_novo = max(10, int(tamanho_base * fator))
    fonte_temp = pygame.font.Font(None, tamanho_novo + 10)
    surf = fonte_temp.render(texto, True, cor)
    x = (LARGURA_TELA - surf.get_width()) // 2
    tela.blit(surf, (x, y))


# ---------------------------------------------------------------------------
# Tela de digitar nome
# ---------------------------------------------------------------------------

def tela_digitar_nome(tela, fonte_grande, fonte_pequena, relogio):
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


# ---------------------------------------------------------------------------
# Tela de RECORDES aprimorada
# ---------------------------------------------------------------------------

def tela_recorde(tela, fonte_grande, fonte_pequena, relogio, recorde):
    entradas = carregar_ranking(CAMINHO_RANKING)
    tick = 0
    particulas = SistemaParticulas()
    # Dispara confete decorativo no topo
    particulas.explodir(LARGURA_TELA // 2, 80, 80)

    rodando = True
    while rodando:
        relogio.tick(FPS)
        tick += 1

        # ---------- Fundo ----------
        tela.fill((10, 20, 60))
        for i in range(ALTURA_TELA):
            fator = i / ALTURA_TELA
            r = int(10  + fator * 10)
            g = int(20  + fator * 30)
            b = int(60  + fator * 80)
            pygame.draw.line(tela, (r, g, b), (0, i), (LARGURA_TELA, i))

        # ---------- Título  ----------
        texto_pulsante(tela, "🏆  HALL DA FAMA  🏆", fonte_grande, OURO_BRILHO, 25, tick, escala_max=1.08)

        # ---------- Melhor pontuação em destaque ----------
        pygame.draw.rect(tela, (0, 60, 150), (220, 90, 560, 58), border_radius=12)
        pygame.draw.rect(tela, OURO_BRILHO,  (220, 90, 560, 58), width=3, border_radius=12)
        desenhar_texto_centralizado(
            tela, "MELHOR PONTUACAO:  " + str(recorde) + " pts",
            fonte_pequena, OURO_BRILHO, 107,
        )

        # ---------- Lista de ranking ----------
        if len(entradas) == 0:
            desenhar_texto_centralizado(tela, "Nenhum jogador ainda!", fonte_pequena, CINZA, 280)
        else:
            cores_posicao = {0: OURO, 1: PRATA, 2: BRONZE}
            medalhas      = {0: "🥇", 1: "🥈", 2: "🥉"}
            for i, (nome, pts) in enumerate(entradas):
                y = 175 + i * 44
                cor_fundo = cores_posicao.get(i, (40, 40, 90))

                # Destaque animado para o 1º lugar
                if i == 0:
                    brilho = int(120 + 80 * math.sin(tick * 0.08))
                    cor_fundo = (min(255, brilho + 80), min(255, brilho + 60), 0)

                pygame.draw.rect(tela, cor_fundo, (120, y, 760, 38), border_radius=8)
                pygame.draw.rect(tela, BRANCO,    (120, y, 760, 38), width=1, border_radius=8)

                medalha = medalhas.get(i, str(i + 1) + ".")
                surf_m  = fonte_pequena.render(medalha, True, PRETO)
                tela.blit(surf_m, (135, y + 5))

                surf_n = fonte_pequena.render(nome, True, PRETO)
                tela.blit(surf_n, (200, y + 5))

                surf_p = fonte_pequena.render(str(pts) + " pts", True, PRETO)
                tela.blit(surf_p, (840 - surf_p.get_width(), y + 5))

        # ---------- Partículas ----------
        particulas.atualizar_e_desenhar(tela)

        # ---------- Rodapé ----------
        desenhar_texto_centralizado(
            tela, "Clique ou pressione uma tecla para voltar",
            fonte_pequena, CINZA, ALTURA_TELA - 45,
        )

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                return

        pygame.display.flip()


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------

def executar_jogo():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio     = pygame.time.Clock()
    fonte_grande  = pygame.font.Font(None, TAMANHO_FONTE_GRANDE)
    fonte_pequena = pygame.font.Font(None, TAMANHO_FONTE_PEQUENA)

    estado = "menu"

    nome_jogador  = ""
    pergunta_atual = 0
    respondida     = False
    pontos         = 0
    recorde        = carregar_recorde(CAMINHO_RECORDE)

    mensagem          = ""
    contador_mensagem = 0

    matriz_opcoes = gerar_matriz_embaralhada()
    rects_botoes  = []

    tempo_restante = TEMPO_POR_PERGUNTA
    ultimo_tick    = pygame.time.get_ticks()

    # Sistemas de efeito
    flash    = FlashEfeito()
    particulas = SistemaParticulas()

    # Variáveis de animação
    tick_global  = 0
    novo_recorde = False  # flag para tela de vitória

    # Estado da tela de derrota / vitória para animação do rosto
    rosto_escala    = 1.0
    rosto_direcao   = 1

    rodando = True
    while rodando:
        relogio.tick(FPS)
        agora = pygame.time.get_ticks()
        tick_global += 1

        # ------------------------------------------------------------------
        # Atualizar contagem regressiva de tempo
        # ------------------------------------------------------------------
        if estado == "jogando" and not respondida:
            if agora - ultimo_tick >= 1000:
                tempo_restante -= 1
                ultimo_tick = agora
                if tempo_restante <= 0:
                    estado         = "derrota"
                    mensagem       = "Tempo esgotado!"
                    flash.iniciar(VERMELHO_BRILHO, duracao_frames=40, alpha_inicial=200)
                elif tempo_restante <= 5:
                    # Flash vermelho suave nos últimos 5 s
                    flash.iniciar((255, 80, 0), duracao_frames=20, alpha_inicial=80)

        # ------------------------------------------------------------------
        # Eventos
        # ------------------------------------------------------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            # ---- Menu ----
            if estado == "menu" and evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if 350 <= mx <= 650 and 380 <= my <= 430:
                    nome_jogador = tela_digitar_nome(tela, fonte_grande, fonte_pequena, relogio)
                    if nome_jogador is None:
                        rodando = False
                    else:
                        pergunta_atual = 0
                        pontos         = 0
                        respondida     = False
                        novo_recorde   = False
                        matriz_opcoes  = gerar_matriz_embaralhada()
                        tempo_restante = TEMPO_POR_PERGUNTA
                        ultimo_tick    = pygame.time.get_ticks()
                        particulas.limpar()
                        estado = "jogando"
                        # Limpa eventos acumulados durante a tela de nome
                        # (o ENTER pressionado não deve ser processado no jogo)
                        pygame.event.clear()

                if 350 <= mx <= 650 and 460 <= my <= 510:
                    tela_recorde(tela, fonte_grande, fonte_pequena, relogio, recorde)

            # ---- Jogando: clicar em opção ----
            if (estado == "jogando"
                    and evento.type == pygame.MOUSEBUTTONDOWN
                    and not respondida
                    and pergunta_atual < len(PERGUNTAS)):
                mx, my = pygame.mouse.get_pos()
                for i, rect in enumerate(rects_botoes):
                    if rect.collidepoint(mx, my):
                        resposta = matriz_opcoes[pergunta_atual][i].lower()
                        respondida = True
                        if verificar_resposta(pergunta_atual, resposta):
                            pontos         = calcular_pontos(pontos, 1)
                            mensagem       = "CORRETO!"
                            contador_mensagem = 90
                            # Flash verde ao acertar
                            flash.iniciar(VERDE_BRILHO, duracao_frames=25, alpha_inicial=140)
                            # Pequena explosão de confete na área da resposta
                            particulas.explodir(rect.centerx, rect.centery, 30)
                        else:
                            estado   = "derrota"
                            mensagem = "Resposta errada!"
                            flash.iniciar(VERMELHO_BRILHO, duracao_frames=40, alpha_inicial=200)
                        break

            # ---- Jogando: avançar para próxima pergunta ----
            if (estado == "jogando"
                    and evento.type == pygame.MOUSEBUTTONDOWN
                    and respondida):
                pergunta_atual    += 1
                respondida         = False
                mensagem           = ""
                contador_mensagem  = 0
                tempo_restante     = TEMPO_POR_PERGUNTA
                ultimo_tick        = pygame.time.get_ticks()
                particulas.limpar()
                if pergunta_atual >= len(PERGUNTAS):
                    estado = "vitoria"
                    novo_recorde = pontos > recorde
                    if novo_recorde:
                        # Flash dourado épico para novo recorde
                        flash.iniciar(OURO_BRILHO, duracao_frames=60, alpha_inicial=220)
                        particulas.explodir(LARGURA_TELA // 2, ALTURA_TELA // 2, 120)
                    else:
                        flash.iniciar(VERDE_BRILHO, duracao_frames=40, alpha_inicial=160)
                        particulas.explodir(LARGURA_TELA // 2, 200, 60)

            # ---- Derrota: voltar ao menu ----
            if estado == "derrota" and evento.type == pygame.MOUSEBUTTONDOWN:
                salvar_ranking(CAMINHO_RANKING, nome_jogador, pontos)
                if pontos > recorde:
                    recorde = pontos
                    salvar_recorde(CAMINHO_RECORDE, recorde)
                estado = "menu"
                particulas.limpar()

            # ---- Vitória: voltar ao menu ----
            if estado == "vitoria" and evento.type == pygame.MOUSEBUTTONDOWN:
                salvar_ranking(CAMINHO_RANKING, nome_jogador, pontos)
                if pontos > recorde:
                    recorde = pontos
                    salvar_recorde(CAMINHO_RECORDE, recorde)
                estado = "menu"
                particulas.limpar()

        # ==================================================================
        # DESENHO
        # ==================================================================

        # ---- MENU ----
        if estado == "menu":
            tela.fill(BRANCO)
            desenhar_texto_centralizado(
                tela, "QUEM QUER SER ENGENHEIRO(A) DE SOFTWARE?",
                fonte_grande, PRETO, 200,
            )
            desenhar_texto_centralizado(
                tela, "Acerte todas as perguntas para se tornar Engenheiro!",
                fonte_pequena, CINZA_ESCURO, 270,
            )
            desenhar_texto_centralizado(
                tela, "Recorde atual: " + str(recorde) + " pts",
                fonte_pequena, AZUL, 320,
            )
            pygame.draw.rect(tela, VERDE, (350, 380, 300, 50), border_radius=8)
            desenhar_texto_centralizado(tela, "JOGAR", fonte_grande, BRANCO, 390)
            pygame.draw.rect(tela, AZUL, (350, 460, 300, 50), border_radius=8)
            desenhar_texto_centralizado(tela, "RECORDES", fonte_grande, BRANCO, 470)

        # ---- JOGANDO ----
        elif estado == "jogando" and pergunta_atual < len(PERGUNTAS):
            tela.fill(BRANCO)

            # Cabeçalho
            texto_j = fonte_pequena.render("Jogador: " + nome_jogador, True, PRETO)
            tela.blit(texto_j, (50, 15))
            texto_p = fonte_pequena.render("Pontos: " + str(pontos), True, PRETO)
            tela.blit(texto_p, (LARGURA_TELA - 200, 15))

            # Barra de tempo
            desenhar_barra_tempo(tela, tempo_restante, TEMPO_POR_PERGUNTA, 50, 52, 900, 28)

            # Pergunta
            pergunta = obter_pergunta(pergunta_atual)
            surf_q   = fonte_pequena.render(pergunta, True, PRETO)
            tela.blit(surf_q, (50, 110))

            # Botões de opção
            rects_botoes = []
            for i, opcao in enumerate(matriz_opcoes[pergunta_atual]):
                y    = 210 + i * 90
                cor  = CINZA
                # Realça o botão se já foi respondido e esta é a resposta certa
                if respondida:
                    if opcao.lower() == PERGUNTAS[pergunta_atual]["resposta"].lower():
                        cor = VERDE
                rect = pygame.draw.rect(tela, cor, (100, y, 800, 70), border_radius=8)
                rects_botoes.append(rect)
                surf_o = fonte_pequena.render(opcao, True, PRETO)
                tela.blit(surf_o, (120, y + 22))

            # Mensagem de acerto
            if respondida and contador_mensagem > 0:
                desenhar_texto_centralizado(tela, mensagem, fonte_grande, VERDE, 585)
                desenhar_texto_centralizado(
                    tela, "Clique para proxima pergunta", fonte_pequena, PRETO, 635,
                )
                contador_mensagem -= 1

            # Partículas de confete de acerto
            particulas.atualizar_e_desenhar(tela)

        # ---- DERROTA ----
        elif estado == "derrota":
            # Fundo vermelho pulsante
            pulso = int(30 * math.sin(tick_global * 0.08))
            r = min(255, 180 + pulso)
            tela.fill((r, 0, 0))
            pygame.draw.rect(tela, VERMELHO, (60, 60, LARGURA_TELA - 120, ALTURA_TELA - 120), border_radius=20)
            pygame.draw.rect(tela, BRANCO,   (60, 60, LARGURA_TELA - 120, ALTURA_TELA - 120), width=4, border_radius=20)

            # Título tremendo (shake rápido)
            shake_x = random.randint(-3, 3) if tick_global % 4 < 2 else 0
            surf_go = pygame.font.Font(None, 72).render("GAME OVER!", True, BRANCO)
            tela.blit(surf_go, (LARGURA_TELA // 2 - surf_go.get_width() // 2 + shake_x, 80))

            # Carinha triste com escala pulsante
            rosto_r = int(90 + 8 * math.sin(tick_global * 0.06))
            desenhar_rosto(tela, LARGURA_TELA // 2, 255, rosto_r, triste=True)

            desenhar_texto_centralizado(tela, mensagem, fonte_pequena, BRANCO, 368)
            desenhar_texto_centralizado(tela, "Voce fez " + str(pontos) + " ponto(s)", fonte_grande, BRANCO, 415)
            desenhar_texto_centralizado(tela, "Recorde: " + str(recorde) + " pts", fonte_pequena, BRANCO, 462)
            desenhar_texto_centralizado(tela, "Clique para voltar ao menu", fonte_pequena, BRANCO, 560)

        # ---- VITÓRIA ----
        elif estado == "vitoria":
            # Fundo verde gradiente animado
            onda = int(20 * math.sin(tick_global * 0.05))
            for i in range(ALTURA_TELA):
                fator = i / ALTURA_TELA
                g = int(100 + fator * 80 + onda)
                tela.set_at_mapped if False else None
                pygame.draw.line(tela, (0, min(255, g), 40), (0, i), (LARGURA_TELA, i))

            # Painel central
            pygame.draw.rect(tela, (0, 100, 30, 200), (80, 80, 840, 500), border_radius=20)
            s_painel = pygame.Surface((840, 500), pygame.SRCALPHA)
            s_painel.fill((0, 0, 0, 80))
            tela.blit(s_painel, (80, 80))
            pygame.draw.rect(tela, VERDE_BRILHO, (80, 80, 840, 500), width=3, border_radius=20)

            # Título
            texto_pulsante(tela, "PARABENS, ENGENHEIRO(A)!", fonte_grande, BRANCO, 105, tick_global)

            # Carinha feliz
            desenhar_rosto(tela, LARGURA_TELA // 2, 280, 80, triste=False)

            desenhar_texto_centralizado(tela, "Voce acertou todas as perguntas!", fonte_pequena, BRANCO, 385)
            desenhar_texto_centralizado(tela, "Pontuacao: " + str(pontos) + " pts", fonte_grande, BRANCO, 425)

            if novo_recorde:
                texto_pulsante(tela, "★  NOVO RECORDE!  ★", fonte_grande, AMARELO_BRILHO, 472, tick_global, escala_max=1.2, velocidade=6)
            else:
                desenhar_texto_centralizado(tela, "Recorde: " + str(recorde) + " pts", fonte_pequena, BRANCO, 480)

            desenhar_texto_centralizado(tela, "Clique para voltar ao menu", fonte_pequena, BRANCO, 545)

            # Confetes caindo
            if tick_global % 8 == 0:
                particulas.explodir(
                    random.randint(100, LARGURA_TELA - 100),
                    random.randint(50, 200),
                    10,
                )
            particulas.atualizar_e_desenhar(tela)

        # ------------------------------------------------------------------
        # Flash global (sempre por cima de tudo)
        # ------------------------------------------------------------------
        flash.atualizar_e_desenhar(tela)

        pygame.display.flip()

    pygame.quit()
