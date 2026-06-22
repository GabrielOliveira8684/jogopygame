import os

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_resposta,
    gerar_matriz_embaralhada,
    obter_pergunta,
    PERGUNTAS,
)
from src.dados import (
    salvar_recorde,
    carregar_recorde,
    salvar_ranking,
    carregar_ranking,
)


# ---------------------------------------------------------------------------
# Regras de pontuação e vidas
# ---------------------------------------------------------------------------

def test_calcular_pontos():
    """Deve somar corretamente os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_jogador_perdeu_com_zero_vidas():
    """Deve indicar derrota quando o total de vidas chega a zero."""
    assert jogador_perdeu(0) is True


def test_jogador_nao_perdeu_com_vidas():
    """Nao deve indicar derrota quando o jogador ainda tem vidas."""
    assert jogador_perdeu(3) is False


def test_limitar_valor_abaixo_do_minimo():
    """Deve retornar o limite minimo quando o valor informado for menor."""
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    """Deve retornar o limite maximo quando o valor informado for maior."""
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    """Deve manter o valor original quando ele ja estiver no intervalo."""
    assert limitar_valor(50, 0, 100) == 50


# ---------------------------------------------------------------------------
# Regras do quiz (perguntas e respostas)
# ---------------------------------------------------------------------------

def test_verificar_resposta_correta():
    """Deve considerar correta a resposta certa, ignorando maiusculas/minusculas."""
    assert verificar_resposta(0, "INT") is True
    assert verificar_resposta(0, "int") is True


def test_verificar_resposta_incorreta():
    """Deve considerar incorreta uma resposta diferente da esperada."""
    assert verificar_resposta(0, "float") is False


def test_obter_pergunta_formata_numero_e_texto():
    """O texto da pergunta deve conter o numero (1-indexado) e a pergunta original."""
    texto = obter_pergunta(0)
    assert "PERGUNTA NÚMERO 1" in texto
    assert PERGUNTAS[0]["pergunta"] in texto


def test_gerar_matriz_embaralhada_mantem_mesmas_opcoes():
    """As opcoes embaralhadas devem ser as mesmas da pergunta original, apenas em outra ordem."""
    matriz = gerar_matriz_embaralhada()
    assert len(matriz) == len(PERGUNTAS)
    for indice, opcoes_embaralhadas in enumerate(matriz):
        assert sorted(opcoes_embaralhadas) == sorted(PERGUNTAS[indice]["opcoes"])


# ---------------------------------------------------------------------------
# Persistencia de dados (recorde e ranking)
# ---------------------------------------------------------------------------

def test_carregar_recorde_sem_arquivo_retorna_zero(tmp_path):
    """Em uma maquina nova, sem arquivo de recorde ainda, deve retornar 0 (sem travar o jogo)."""
    caminho = tmp_path / "recorde.txt"
    assert carregar_recorde(str(caminho)) == 0


def test_salvar_e_carregar_recorde(tmp_path):
    """Deve salvar e recuperar corretamente a pontuacao recorde."""
    caminho = tmp_path / "recorde.txt"
    salvar_recorde(str(caminho), 7)
    assert carregar_recorde(str(caminho)) == 7


def test_carregar_ranking_sem_arquivo_retorna_lista_vazia(tmp_path):
    """Em uma maquina nova, sem arquivo de ranking ainda, deve retornar lista vazia."""
    caminho = tmp_path / "ranking.txt"
    assert carregar_ranking(str(caminho)) == []


def test_salvar_e_carregar_ranking_ordenado_do_maior_para_menor(tmp_path):
    """O ranking deve ser carregado ordenado da maior para a menor pontuacao."""
    caminho = tmp_path / "ranking.txt"
    salvar_ranking(str(caminho), "Ana", 3)
    salvar_ranking(str(caminho), "Bruno", 8)
    salvar_ranking(str(caminho), "Carla", 5)

    ranking = carregar_ranking(str(caminho))

    assert ranking == [["Bruno", 8], ["Carla", 5], ["Ana", 3]]


def test_carregar_ranking_limita_aos_10_primeiros(tmp_path):
    """O ranking carregado nao deve ter mais do que 10 entradas."""
    caminho = tmp_path / "ranking.txt"
    for i in range(15):
        salvar_ranking(str(caminho), "Jogador" + str(i), i)

    ranking = carregar_ranking(str(caminho))

    assert len(ranking) == 10
    assert ranking[0][1] == 14  # maior pontuacao deve vir primeiro