grafo_nao_direcionado = {1: {2, 3, 5},
                         2: {1, 3, 5},
                         3: {1, 2, 4},
                         4: {3, 5},
                         5: {1, 2, 4}}

grafo_direcionado = {1: {2},
                     2: {1, 3, 4},
                     3: {1, 4, 5},
                     4: {5, 6},
                     5: set(),
                     6: {4}}

grafo_ponderado = {'A': {'B': 12, 'C': 4},
                   'B': {'C': 6, 'D': 6},
                   'C': {'B': 10, 'D': 2, 'E': 2},
                   'D': {'C': 8, 'F': 6},
                   'E': {'B': 2, 'F': 6},
                   'F': {}
                   }

percurso_valido = [1, 5, 2, 3, 1, 3]
percurso_invalido = [1, 5, 2, 3, 5, 3]


def check_percurso(grafo, percurso):
    for indice in range(len(percurso) - 1):
        vertice_atual = percurso[indice]
        adjacente = grafo[vertice_atual]
        vertice_proximo = percurso[indice + 1]

        if vertice_proximo not in adjacente:
            return False
        else:
            pass
    return True


def is_vizinho(g, vertice1, vertice2):
    adj = g[vertice1]
    if vertice2 in adj:
        return True
    return False


def check_is_subgraph(grafo1, grafo2) -> bool:
    for vertice in grafo2:
        if vertice not in grafo1:
            return False
        else:
            adjacentes_grafo1 = grafo1[vertice]
            adjacentes_grafo2 = grafo2[vertice]
            for vizinho in adjacentes_grafo2:
                if vizinho not in adjacentes_grafo1:
                    return False
    return True


def get_subgrafo_induzido(grafo1, lista_de_vertices):
    subgrafo_induzido = {}
    for vertice in lista_de_vertices:
        adjacentes = grafo1[vertice]
        subgrafo_induzido[vertice] = []
        for vizinho in adjacentes:
            if vizinho in lista_de_vertices:
                subgrafo_induzido[vertice].append(vizinho)
    return subgrafo_induzido


def get_complementar(grafo) -> dict:
    complementar = {}
    lista_de_vertices = set(grafo)
    for vertice in grafo:
        adjacentes = set(grafo[vertice])
        vertices_ausentes = lista_de_vertices - adjacentes
        complementar[vertice] = list(vertices_ausentes.difference([vertice]))

    return complementar


def get_vizinho_antecessor(grafo: dict, grupo: tuple | list | set | int) -> set:
    grupo = set(grupo)
    vizinhanca = set()
    for vertice in grupo:
        for v, adjacentes in grafo.items():
            if vertice in adjacentes:
                vizinhanca.update([v])
    vizinhanca -= grupo
    return vizinhanca


def get_vizinho_sucessor(grafo, grupo: tuple | list | set | int) -> set:
    grupo = set(grupo)
    vizinhanca = set()
    for vertice in grupo:
        vizinhanca.update(grafo[vertice])
    vizinhanca -= grupo
    return vizinhanca


def get_fecho_transitivo_direto(grafo, vertice: int) -> set:
    fecho = {vertice}
    w = set()

    while True:
        fecho.update(get_vizinho_sucessor(grafo, fecho))
        if fecho == w:
            break
        w = fecho
    return fecho


def get_fecho_transitivo_indireto(grafo, vertice: int) -> set:
    fecho = {vertice}
    w = set()

    while True:
        fecho.update(get_vizinho_antecessor(grafo, fecho))
        if fecho == w:
            break
        w = fecho
    return fecho


def malgrange(grafo):
    y = set(grafo)
    i = 0
    componente = {}

    while len(y) > 0:
        i += 1
        vertice = y.pop()

        r_plus = get_fecho_transitivo_direto(grafo, vertice)
        r_minus = get_fecho_transitivo_indireto(grafo, vertice)

        componente[i] = r_plus.intersection(r_minus)
        y -= componente[i]
    return componente


def remove_direction(grafo):
    saida = {}
    for vertice, adjacentes in grafo.items():
        saida[vertice] = set()
        for vizinho in adjacentes:
            saida[vertice].update([vizinho])
            saida[vizinho].update([vertice])
    return saida


def is_conexo(grafo):
    fecho_transitivo_direto = get_fecho_transitivo_direto(grafo, 1)
    fecho_transitivo_indireto = get_fecho_transitivo_indireto(grafo, 1)
    resultado = fecho_transitivo_direto.intersection(fecho_transitivo_indireto)

    return resultado == set(grafo)


def is_conexo2(grafo):
    new_grafo = remove_direction(grafo)
    componentes = malgrange(new_grafo)
    n_componentes = len(componentes)
    if n_componentes > 1:
        return False
    return True


def dijkstra(grafo, vertice_inicial):
    # Inicializa as distâncias mínimas com infinito para todos os vértices, exceto o de origem
    vertices_nao_visitados = set(grafo)
    anterior = {}
    distancias = {}
    for vertice in vertices_nao_visitados:
        distancias[vertice] = float('inf')
    distancias[vertice_inicial] = 0

    while len(vertices_nao_visitados) > 0:
        # Seleciona o vértice que será visitado que tenha a menor distância registrada
        vertice_visitado = None
        distancia_do_visitado = float('inf')
        for vertice_candidato in vertices_nao_visitados:
            if distancias[vertice_candidato] < distancia_do_visitado:
                vertice_visitado = vertice_candidato
                distancia_do_visitado = distancias[vertice_visitado]

        # Saia se não há mais vértices para visitar (há vertices inatingíveis)
        if not vertice_visitado: break

        # Marca o vértice como visitado
        vertices_nao_visitados -= {vertice_visitado}

        # Atualiza as distâncias no array de distâncias
        for vizinho in grafo[vertice_visitado]:
            if vizinho not in vertices_nao_visitados: continue  # Considere apenas vizinhos não visitados
            custo_do_vizinho = grafo[vertice_visitado][vizinho]
            nova_distancia = distancia_do_visitado + custo_do_vizinho
            # Se a distancia até este vizinho for menor do que a que já foi registrada, atualize o registro
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anterior[vizinho] = vertice_visitado

    return distancias, anterior
