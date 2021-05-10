from pprint import pprint
import json
# Ações
VAI_PARA_FREEZER = 'VAI_PARA_FREEZER'
VAI_PARA_MESA_AMB = 'VAI_PARA_MESA_AMB'
PEGA = 'PEGA'
COLOCA = 'COLOCA'
ESPERA = 'ESPERA'

ACOES = [VAI_PARA_FREEZER, VAI_PARA_MESA_AMB, PEGA, COLOCA, ESPERA]

# Constantes
COMBUSTIVEL_INICIAL = 10
PASSO_TEMPERATURA = 1
TEMPERATURA_INICIAL = -10
PONTO = 1


class HAL():
    def __init__(self, definicao={'posicao': '', 'segurando': None, 'combustivel': COMBUSTIVEL_INICIAL}):
        self.posicao = definicao['posicao']
        self.segurando = definicao['segurando']
        self.combustivel = definicao['combustivel']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        proximo_estado_existe = False
        if acao == VAI_PARA_FREEZER and self.posicao != 'freezer':
            proximo['posicao'] = 'freezer'
            proximo['combustivel'] -= 1
            proximo_estado_existe = True
        elif acao == VAI_PARA_MESA_AMB and self.posicao != 'mesa_amb':
            proximo['posicao'] = 'mesa_amb'
            proximo['combustivel'] -= 1
            proximo_estado_existe = True
        elif acao == PEGA:
            if self.posicao == 'freezer' and estado.freezer.bobinas:
                proximo['segurando'] = 'bobinas'
                proximo_estado_existe = True
        elif acao == COLOCA:
            if self.posicao == 'mesa_amb' and self.segurando == 'bobinas':
                proximo['segurando'] = ''
                proximo_estado_existe = True
        elif acao == ESPERA:
            proximo_estado_existe = True

        if proximo_estado_existe:
            return proximo
        return None

    def log(self):
        print('HAL esta {} segurando {} com combustivel faltando {}'.format(
            self.posicao if self.posicao else 'na posicao inicial', self.segurando if self.segurando else 'nada', self.combustivel
        ))


class Bobinas():
    def __init__(self, definicao={'sujo': False, 'temp': TEMPERATURA_INICIAL}):
        self.sujo = definicao['sujo']
        self.temp = definicao['temp']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if estado.mesa_amb.bobinas:
            proximo['temp'] = self.temp + PASSO_TEMPERATURA
        return proximo

    def log(self, estado):
        if estado.hal.segurando == 'bobinas':
            localizacao = 'hal'
        elif estado.freezer.bobinas:
            localizacao = 'freezer'
        elif estado.mesa_amb.bobinas:
            localizacao = 'freezer'
        print('As bobinas estão {} no(a) {} na temperatura {} graus celcius'.format(
            'sujas' if self.sujo else 'limpas', localizacao, self.temp
        ))


class Freezer():
    def __init__(self, definicao={'bobinas': True}):
        self.bobinas = definicao['bobinas']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if acao == PEGA and self.bobinas and estado.hal.posicao == 'freezer':
            proximo['bobinas'] = False
        return proximo


class MesaAmb():
    def __init__(self, definicao={'bobinas': False}):
        self.bobinas = definicao['bobinas']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if acao == COLOCA and not self.bobinas and estado.hal.posicao == 'mesa_amb' and estado.hal.segurando == 'bobinas':
            proximo['bobinas'] = True
        return proximo


def pontuacao_do_estado(estado, destino):
    pontuacao = 0
    distancia_maxima_temp = destino['bobinas']['temp'] - \
        TEMPERATURA_INICIAL
    if estado.mesa_amb.bobinas == destino['mesa_amb']['bobinas']:
        pontuacao += PONTO
    if estado.freezer.bobinas == destino['freezer']['bobinas']:
        pontuacao += PONTO
    if estado.bobinas.temp < destino['bobinas']['temp']:
        pontuacao += distancia_maxima_temp - \
            (destino['bobinas']['temp'] - estado.bobinas.temp)
    if estado.bobinas.temp == destino['bobinas']['temp']:
        pontuacao += distancia_maxima_temp + PONTO
    if estado.bobinas.temp > destino['bobinas']['temp']:
        pontuacao -= 1000 * PONTO
    pontuacao += estado.hal.combustivel / 2.0
    return pontuacao


class Estado():
    def __init__(self, estado_base):
        self.hal = HAL(estado_base['hal']) if 'hal' in estado_base else HAL()
        self.bobinas = Bobinas(
            estado_base['bobinas']) if 'bobinas' in estado_base else Bobinas()
        self.freezer = Freezer(
            estado_base['freezer']) if 'freezer' in estado_base else Freezer()
        self.mesa_amb = MesaAmb(
            estado_base['mesa_amb']) if 'mesa_amb' in estado_base else MesaAmb()

    def estado_a_partir_da_acao(self, acao):
        hal = self.hal.estado_a_partir_da_acao(acao, self)
        if hal:
            return Estado({
                'hal': hal,
                'bobinas': self.bobinas.estado_a_partir_da_acao(acao, self),
                'freezer': self.freezer.estado_a_partir_da_acao(acao, self),
                'mesa_amb': self.mesa_amb.estado_a_partir_da_acao(acao, self),
            })
        return None

    def __repr__(self):
        return json.dumps({
            'hal': vars(self.hal),
            'bobinas': vars(self.bobinas),
            'freezer': vars(self.freezer),
            'mesa_amb': vars(self.mesa_amb)
        })

    def eh_melhor_que(self, outro, destino):
        pontuacao0 = pontuacao_do_estado(self, destino)
        pontuacao1 = pontuacao_do_estado(outro, destino)
        return pontuacao0 >= pontuacao1

    def eh_igual(self, destino):
        pontuacao0 = pontuacao_do_estado(self, destino)
        pontuacao1 = pontuacao_do_estado(destino, destino)
        return pontuacao0 == pontuacao1


def gera_possiveis_caminhos(estado):

    caminhos = []
    for acao in ACOES:
        proximo = estado.estado_a_partir_da_acao(acao)
        if proximo:
            caminhos.append({'acao': acao, 'estado': proximo})
    return caminhos


def seleciona_melhor_caminho(caminhos, destino):
    melhor = 0
    for index, caminho in enumerate(caminhos):
        melhor_estado = caminhos[melhor][-1]['estado']
        atual = caminho[-1]['estado']
        if atual.eh_melhor_que(melhor_estado, destino):
            melhor = index
    return caminhos[melhor]


def busca_caminho(inicio, destino):
    terminado = False
    caminho = [{'acao': '', 'estado': inicio}]

    steps = 6
    while steps:
        steps -= 1
        caminhos_possiveis = []
        caminhos_profundidade1 = gera_possiveis_caminhos(caminho[-1]['estado'])
        for caminho_p1 in caminhos_profundidade1:
            caminhos_profundidade2 = gera_possiveis_caminhos(
                caminho_p1['estado'])
            caminhos_possiveis.extend(
                [[caminho_p1, caminho_p2] for caminho_p2 in caminhos_profundidade2])
        melhor_caminho = seleciona_melhor_caminho(caminhos_possiveis, destino)
        caminho.extend(melhor_caminho)
        # if steps == 0:
        #     # pprint(caminhos_possiveis)
        #     pprint([[cam, pontuacao_do_estado(cam[-1]['estado'], destino)]
        #             for cam in caminhos_possiveis])
        # if (caminho[-1]['estado'].eh_igual(destino)):
        #     terminado = True
    printa_caminho(caminho)


def printa_caminho(caminho):
    for item in caminho:
        acao = item['acao']
        estado = item['estado']
        if acao:
            print('\nA acao tomada foi:', acao)
        estado.hal.log()
        estado.bobinas.log(estado)


destino = {
    'freezer': {
        'bobinas': False,
    },
    'mesa_amb': {
        'bobinas': True,
    },
    'bobinas': {
        'temp': -2
    }
}

estado = Estado({})
caminho = busca_caminho(estado, destino)
