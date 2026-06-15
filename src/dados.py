def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em arquivo texto."""
    arquivo = open(caminho_arquivo, "w", encoding="utf-8")
    arquivo.write(str(pontuacao))
    arquivo.close()
 
 
def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se não existir valor válido."""
    arquivo = open(caminho_arquivo, "r", encoding="utf-8")
    conteudo = arquivo.read().strip()
    arquivo.close()
 
    if conteudo == "":
        return 0
 
    return int(conteudo)
 
 
def salvar_ranking(caminho_arquivo, nome, pontuacao):
    """Adiciona uma entrada de nome e pontuação no ranking."""
    arquivo = open(caminho_arquivo, "a", encoding="utf-8")
    arquivo.write(nome + ";" + str(pontuacao) + "\n")
    arquivo.close()
 
 
def carregar_ranking(caminho_arquivo):
    """Carrega o ranking e retorna lista de listas [nome, pontuacao] ordenada."""
    arquivo = open(caminho_arquivo, "r", encoding="utf-8")
    linhas = arquivo.readlines()
    arquivo.close()
 
    entradas = []
 
    for linha in linhas:
        linha = linha.strip()
        if ";" in linha:
            partes = linha.split(";")
            nome = partes[0]
            pontuacao = int(partes[1])
            entradas.append([nome, pontuacao])
 
    # Ordenação bolha do maior para o menor
    for i in range(len(entradas)):
        for j in range(i + 1, len(entradas)):
            if entradas[j][1] > entradas[i][1]:
                entradas[i], entradas[j] = entradas[j], entradas[i]
 
    return entradas[:10]