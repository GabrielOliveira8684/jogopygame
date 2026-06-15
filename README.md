# Nome do Jogo

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório é um template para os grupos da disciplina. A proposta é começar com uma base funcional e evoluir o jogo ao longo do semestre.

## Integrantes do grupo

Fabricio Felix Gomes
Gabriel Oliveira
Gabriel Oliveira Gonzaga Araujo
Italo Alves Machado

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

Jogo de perguntas e respostas sobre Python. O jogador responde a uma série de perguntas de múltipla escolha e deve acertar todas para se tornar Engenheiro(a) de Software. Cada pergunta tem um cronômetro de 30 segundos — errar ou deixar o tempo acabar encerra a partida.

## Objetivo do jogador

Acertar todas as perguntas dentro do tempo limite. Ao final, o jogador recebe o título de Engenheiro(a) de Software e sua pontuação é registrada no ranking.

## Regras do jogo

O jogador digita seu nome antes de começar.
Cada pergunta tem 30 segundos para ser respondida.
Acertar a pergunta avança para a próxima e soma 1 ponto.
Errar ou deixar o tempo acabar encerra a partida imediatamente.
Ao final (vitória ou derrota), a pontuação é salva no ranking.
O recorde geral é salvo entre sessões.

## Controles

Mouse (clique): selecionar a resposta desejada
Mouse (clique): avançar para a próxima pergunta após acerto
Teclado: digitar o nome na tela inicial

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/GabrielOliveira8684/jogopygame.git
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest tests/ -v
```

## Funcionalidades implementadas

Tela de menu com botões Jogar e Ranking
Digitação do nome do jogador antes da partida
Perguntas com opções embaralhadas a cada partida
Cronômetro de 30 segundos por pergunta (fica vermelho nos últimos 10s)
Sistema de pontuação (1 ponto por acerto)
Tela de derrota (resposta errada ou tempo esgotado)
Tela de vitória com destaque de novo recorde
Ranking dos 10 melhores jogadores (salvo em arquivo)
Recorde persistente entre sessões (salvo em arquivo)