from HAL import busca_caminho, Estado, printa_caminho, COMBUSTIVEL_INICIAL, TEMPERATURA_INICIAL

estado_inicial_caso_abre = {
    'hal': {
        'segurando': '',
        'posicao': '',
        'combustivel': COMBUSTIVEL_INICIAL
    },
    'bobinas': {
        'temp': TEMPERATURA_INICIAL,
        'sujo': False
    },
    'vacinas': {'ordenadas': False},
    'freezer': {'bobinas': True},
    'geladeira': {'vacinas': True},
    'caixa': {
        'bobinas': False,
        'vacinas': False
    }
}


estado_inicial_caso_fecha = {
    'hal': {
        'segurando': '',
        'posicao': '',
        'combustivel': COMBUSTIVEL_INICIAL
    },
    'bobinas': {
        'temp': TEMPERATURA_INICIAL,
        'sujo': False
    },
    'vacinas': {'ordenadas': False},
    'freezer': {'bobinas': False},
    'geladeira': {'vacinas': False},
    'caixa': {
        'bobinas': True,
        'vacinas': True
    }
}

destino_bobinas_abre = {
    'caixa': {
        'bobinas': True
    },
    'bobinas': {
        'temp': -2
    }
}

destino_vacinas_abre = {
    'caixa': {
        'vacinas': True
    },
    'vacinas': {
        'ordenadas': True
    }
}

destino_fecha = {
    'freezer': {
        'bobinas': True
    },
    'geladeira': {
        'vacinas': True
    }
}

destino_vacinas_fecha = {
    'geladeira': {
        'vacinas': True
    },
}

# Pega e coloca bobinas na caixa termica
# estado = Estado(estado_inicial_caso_abre)
# caminho = busca_caminho(estado, destino_bobinas_abre)
# printa_caminho(caminho)

# Pega e coloca vacinas na caixa termica
# estado = Estado(estado_inicial_caso_abre)
# caminho = busca_caminho(estado, destino_vacinas_abre)
# printa_caminho(caminho)

# Pega e coloca bobinas na caixa termica
estado = Estado(estado_inicial_caso_fecha)
caminho = busca_caminho(estado, destino_fecha)
printa_caminho(caminho)

"""
Resultados: foi alcançado o resultado esperado, ou seja, foi possível gerar uma sequência de ações que o robo poderia tomar para resolver o problema proposto, que é chegar em um estado final a partir de um estado inicial. Apesar que é possível que o robo não tome o caminho ótimo, devido a dificuldade já comentada da criação da função heurística, ele sempre conseguiu alcançar uma solução razoavel dado os problemas esquematizados.
"""
