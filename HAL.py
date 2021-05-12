from pprint import pprint
import json
# Ações
VAI_PARA_FREEZER = 'VAI_PARA_FREEZER'
VAI_PARA_MESA_AMB = 'VAI_PARA_MESA_AMB'
VAI_PARA_MESA_TER = 'VAI_PARA_MESA_TER'
VAI_PARA_GELADEIRA = 'VAI_PARA_GELADEIRA'
PEGA = 'PEGA'
COLOCA = 'COLOCA'
ESPERA = 'ESPERA'
ORDENA = 'ORDENA'

ACOES = [VAI_PARA_FREEZER, VAI_PARA_MESA_AMB,
         VAI_PARA_MESA_TER, VAI_PARA_GELADEIRA,
         PEGA, COLOCA, ESPERA, ORDENA]

# Constantes
COMBUSTIVEL_INICIAL = 10
PASSO_TEMPERATURA = 1
TEMPERATURA_INICIAL = -10
PROFUNDIDADE_BUSCA = 5


class HAL():
    def __init__(self, definicao={'posicao': '', 'segurando': '', 'combustivel': COMBUSTIVEL_INICIAL}):
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
        elif acao == VAI_PARA_MESA_TER and self.posicao != 'mesa_ter':
            proximo['posicao'] = 'mesa_ter'
            proximo['combustivel'] -= 1
            proximo_estado_existe = True
        elif acao == VAI_PARA_GELADEIRA and self.posicao != 'geladeira':
            proximo['posicao'] = 'geladeira'
            proximo['combustivel'] -= 1
            proximo_estado_existe = True
        elif acao == PEGA:
            if self.posicao == 'freezer' and estado.freezer.bobinas and self.segurando == '':
                proximo['segurando'] = 'bobinas'
                proximo_estado_existe = True
            elif self.posicao == 'geladeira' and estado.geladeira.vacinas and self.segurando == '':
                proximo['segurando'] = 'vacinas'
                proximo_estado_existe = True
            elif self.posicao == 'mesa_amb' and estado.mesa_amb.bobinas and self.segurando == '':
                proximo['segurando'] = 'bobinas'
                proximo_estado_existe = True
            elif self.posicao == 'mesa_ter' and estado.caixa.bobinas and self.segurando == '':
                proximo['segurando'] = 'bobinas'
                proximo_estado_existe = True
            elif self.posicao == 'mesa_ter' and estado.caixa.vacinas and self.segurando == '':
                proximo['segurando'] = 'vacinas'
                proximo_estado_existe = True

        elif acao == COLOCA:
            if self.posicao == 'mesa_amb' and self.segurando == 'bobinas':
                proximo['segurando'] = ''
                proximo_estado_existe = True
            elif self.posicao == 'freezer' and self.segurando == 'bobinas':
                proximo['segurando'] = ''
                proximo_estado_existe = True
            elif self.posicao == 'geladeira' and self.segurando == 'vacinas':
                proximo['segurando'] = ''
                proximo_estado_existe = True
            elif self.posicao == 'mesa_ter' and self.segurando == 'bobinas':
                proximo['segurando'] = ''
                proximo_estado_existe = True
            elif self.posicao == 'mesa_ter' and self.segurando == 'vacinas':
                proximo['segurando'] = ''
                proximo_estado_existe = True

        elif acao == ORDENA and self.posicao == 'geladeira' and estado.geladeira.vacinas and not estado.vacinas.ordenadas:
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


class Vacinas:
    def __init__(self, definicao={'vencidas': False, 'ordenadas': False}):
        # self.vencidas = definicao['vencidas']
        self.ordenadas = definicao['ordenadas']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if acao == ORDENA and estado.hal.posicao == 'geladeira' and estado.geladeira.vacinas:
            proximo['ordenadas'] = True
        return proximo

    def log(self, estado):
        if estado.hal.segurando == 'vacinas':
            localizacao = 'hal'
        elif estado.geladeira.vacinas:
            localizacao = 'geladeira'
        elif estado.caixa.vacinas:
            localizacao = 'caixa'
        print(
            # f'As vacinas estão no(a) {localizacao} {self.vencidas} e {self.ordenadas}')
            f'As vacinas estão no(a) {localizacao} e {self.ordenadas}')


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
            localizacao = 'mesa_amb'
        elif estado.caixa.bobinas:
            localizacao = 'mesa_ter'
        print('As bobinas estão no(a) {} na temperatura {} graus celcius'.format(
            localizacao, self.temp
        ))


class Caixa():
    def __init__(self, definicao={'bobinas': False, 'vacinas': False}):
        self.bobinas = definicao['bobinas']
        self.vacinas = definicao['vacinas']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if acao == PEGA and self.bobinas and estado.hal.posicao == 'mesa_ter' and estado.hal.segurando == '':
            proximo['bobinas'] = False
        elif acao == PEGA and self.vacinas and estado.hal.posicao == 'mesa_ter' and estado.hal.segurando == '':
            proximo['vacinas'] = False

        elif acao == COLOCA and not self.bobinas and estado.hal.posicao == 'mesa_ter' and estado.hal.segurando == 'bobinas':
            proximo['bobinas'] = True
        elif acao == COLOCA and not self.vacinas and estado.hal.posicao == 'mesa_ter' and estado.hal.segurando == 'vacinas':
            proximo['vacinas'] = True
        return proximo

    def log(self, estado):
        if estado.hal.segurando == 'caixa':
            localizacao = 'hal'
        elif estado.mesa_ter.caixa:
            localizacao = 'mesa termica'
        print('A caixa termica esta no(a) {}, {} e {}'.format(
            localizacao,
            'com bobinas' if self.bobinas else 'sem bobinas',
            'com vacinas' if self.vacinas else 'sem vacinas'
        ))


class Freezer():
    def __init__(self, definicao={'bobinas': True}):
        self.bobinas = definicao['bobinas']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if acao == PEGA and self.bobinas and estado.hal.posicao == 'freezer' and estado.hal.segurando == '':
            proximo['bobinas'] = False
        if acao == COLOCA and not self.bobinas and estado.hal.posicao == 'freezer' and estado.hal.segurando == 'bobinas':
            proximo['bobinas'] = True
        return proximo


class MesaAmb():
    def __init__(self, definicao={'bobinas': False}):
        self.bobinas = definicao['bobinas']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if acao == COLOCA and not self.bobinas and estado.hal.posicao == 'mesa_amb' and estado.hal.segurando == 'bobinas':
            proximo['bobinas'] = True
        elif acao == PEGA and self.bobinas and estado.hal.posicao == 'mesa_amb' and estado.hal.segurando == '':
            proximo['bobinas'] = False
        return proximo


class Geladeira():
    def __init__(self, definicao={'vacinas': True}):
        self.vacinas = definicao['vacinas']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if acao == PEGA and self.vacinas and estado.hal.posicao == 'geladeira' and estado.hal.segurando == '':
            proximo['vacinas'] = False
        if acao == COLOCA and not self.vacinas and estado.hal.posicao == 'geladeira' and estado.hal.segurando == 'vacinas':
            proximo['vacinas'] = True
        return proximo


def pega_localizacao_bobinas(estado):
    if estado.hal.segurando == 'bobinas':
        return estado.hal.posicao
    elif estado.freezer.bobinas:
        return 'freezer'
    elif estado.mesa_amb.bobinas:
        return 'mesa_amb'
    return 'mesa_ter'


def pega_localizacao_bobinas_destino(destino):
    if 'freezer' in destino and destino['freezer']['bobinas']:
        return 'freezer'
    elif 'mesa_amb' in destino and destino['mesa_amb']['bobinas']:
        return 'mesa_amb'
    return 'mesa_ter'


def pega_localizacao_vacinas(estado):
    if estado.hal.segurando == 'vacinas':
        return estado.hal.posicao
    elif estado.geladeira.vacinas:
        return 'geladeira'
    return 'mesa_ter'


def pega_localizacao_vacinas_destino(destino):
    if 'geladeira' in destino and destino['geladeira']['vacinas']:
        return 'geladeira'
    return 'mesa_ter'


def pontuacao_do_estado(estado, destino):
    pontuacao = 0

    # Temperatura da bobina
    if 'bobinas' in destino and 'temp' in destino['bobinas']:
        if estado.mesa_amb.bobinas and estado.bobinas.temp != destino['bobinas']['temp']:
            pontuacao += 2.0

        localizacao_bobinas_atual = pega_localizacao_bobinas(estado)
        localizacao_bobinas_destino = pega_localizacao_bobinas_destino(destino)

        if localizacao_bobinas_atual == 'mesa_amb':
            pontuacao += 0.5
        if localizacao_bobinas_atual == localizacao_bobinas_destino and estado.bobinas.temp != destino['bobinas']['temp']:
            pontuacao -= 1

        distancia_maxima_temp = destino['bobinas']['temp'] - \
            TEMPERATURA_INICIAL

        if estado.bobinas.temp < destino['bobinas']['temp']:
            pontuacao += estado.bobinas.temp - TEMPERATURA_INICIAL
        if estado.bobinas.temp == destino['bobinas']['temp']:
            pontuacao += distancia_maxima_temp + 2

        if estado.bobinas.temp > destino['bobinas']['temp']:
            pontuacao -= 1000

        if (estado.bobinas.temp == destino['bobinas']['temp']
                and localizacao_bobinas_atual == localizacao_bobinas_destino):
            pontuacao += 5

        if (estado.bobinas.temp == destino['bobinas']['temp']
            and localizacao_bobinas_atual == localizacao_bobinas_destino
                and estado.caixa.bobinas == destino['caixa']['bobinas']):
            pontuacao += 10

    if 'freezer' in destino and 'bobinas' in destino['freezer']:
        localizacao_bobinas_atual = pega_localizacao_bobinas(estado)
        localizacao_bobinas_destino = pega_localizacao_bobinas_destino(destino)

        if localizacao_bobinas_atual == localizacao_bobinas_destino:
            pontuacao += 10
        if estado.freezer.bobinas == destino['freezer']['bobinas']:
            pontuacao += 7

    # Pontos relacionados a vacina
    if 'vacinas' in destino:
        if 'vacinas' in destino and estado.vacinas.ordenadas == destino['vacinas']['ordenadas']:
            pontuacao += 5

        localizacao_vacinas_atual = pega_localizacao_vacinas(estado)
        localizacao_vacinas_destino = pega_localizacao_vacinas_destino(destino)

        if localizacao_vacinas_atual == localizacao_vacinas_destino:
            pontuacao += 3

        if 'caixa' in destino and 'vacinas' in destino['caixa'] and estado.caixa.vacinas == destino['caixa']['vacinas']:
            pontuacao += 1
        elif 'geladeira' in destino and estado.geladeira.vacinas == destino['geladeira']['vacinas']:
            pontuacao += 1

    if 'geladeira' in destino and 'vacinas' in destino['geladeira']:
        localizacao_vacinas_atual = pega_localizacao_vacinas(estado)
        localizacao_vacinas_destino = pega_localizacao_vacinas_destino(destino)

        if localizacao_vacinas_atual == localizacao_vacinas_destino:
            pontuacao += 5
        if estado.geladeira.vacinas == destino['geladeira']['vacinas']:
            pontuacao += 3
    # Combustivel
    pontuacao += estado.hal.combustivel
    return pontuacao


class Estado():
    def __init__(self, estado_base):
        self.hal = HAL(estado_base['hal']) if 'hal' in estado_base else HAL()
        self.vacinas = Vacinas(
            estado_base['vacinas']) if 'vacinas' in estado_base else Vacinas()
        self.bobinas = Bobinas(
            estado_base['bobinas']) if 'bobinas' in estado_base else Bobinas()
        self.caixa = Caixa(
            estado_base['caixa']) if 'caixa' in estado_base else Caixa()
        self.freezer = Freezer(
            estado_base['freezer']) if 'freezer' in estado_base else Freezer()
        self.mesa_amb = MesaAmb(
            estado_base['mesa_amb']) if 'mesa_amb' in estado_base else MesaAmb()
        self.geladeira = Geladeira(
            estado_base['geladeira']) if 'geladeira' in estado_base else Geladeira()

    def estado_a_partir_da_acao(self, acao):
        hal = self.hal.estado_a_partir_da_acao(acao, self)
        if hal:
            return Estado({
                'hal': hal,
                'vacinas': self.vacinas.estado_a_partir_da_acao(acao, self),
                'bobinas': self.bobinas.estado_a_partir_da_acao(acao, self),
                'caixa': self.caixa.estado_a_partir_da_acao(acao, self),
                'freezer': self.freezer.estado_a_partir_da_acao(acao, self),
                'mesa_amb': self.mesa_amb.estado_a_partir_da_acao(acao, self),
                'geladeira': self.geladeira.estado_a_partir_da_acao(acao, self),
            })
        return None

    def __repr__(self):
        return json.dumps({
            'hal': vars(self.hal),
            'vacinas': vars(self.vacinas),
            'bobinas': vars(self.bobinas),
            'caixa': vars(self.caixa),
            'freezer': vars(self.freezer),
            'mesa_amb': vars(self.mesa_amb),
            'geladeira': vars(self.geladeira),
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


def seleciona_melhor_estado(estados, destino):
    melhor = 0
    for index, estado in enumerate(estados):
        atual = estados[melhor]
        if estado.eh_melhor_que(atual, destino):
            melhor = index
    return melhor


def estado_eh_destino(estado, destino):
    achou = True
    if 'bobinas' in destino and estado.bobinas.temp != destino['bobinas']['temp']:
        achou = False
    if 'vacinas' in destino and estado.vacinas.ordenadas != destino['vacinas']['ordenadas']:
        achou = False
    if 'caixa' in destino and 'vacinas' in destino['caixa'] and estado.caixa.vacinas != destino['caixa']['vacinas']:
        achou = False
    if 'caixa' in destino and 'bobinas' in destino['caixa'] and estado.caixa.bobinas != destino['caixa']['bobinas']:
        achou = False
    if 'geladeira' in destino and estado.geladeira.vacinas != destino['geladeira']['vacinas']:
        achou = False
    if 'freezer' in destino and estado.freezer.bobinas != destino['freezer']['bobinas']:
        achou = False
    return achou


def seleciona_melhor_caminho(antigo, novos, destino):
    indice_melhor_caminho = 0
    pontuação_melhor_caminho = 0
    achou_solucao = False
    indice_solucao = None
    indice_melhor_estado_solucao = None
    for index, caminho in enumerate([antigo + n for n in novos]):
        if not achou_solucao:
            lista_solucao = [estado_eh_destino(
                c['estado'], destino) for c in caminho]
            achou = sum(lista_solucao) > 0

            if achou:
                achou_solucao = True
                indice_solucao = index
                indice_melhor_estado_solucao = lista_solucao.index(True)
                break
        else:
            lista_solucao = [estado_eh_destino(
                c['estado'], destino) for c in caminho]
            achou = sum(lista_solucao) > 0
            if achou:
                indice_estado_solucao = lista_solucao.index(True)
                if indice_estado_solucao < indice_melhor_estado_solucao:
                    indice_melhor_estado_solucao = indice_estado_solucao
                    indice_solucao = index
            continue

        pontuacoes = [pontuacao_do_estado(
            c['estado'], destino) for c in caminho]

        if sum(p < 0 for p in pontuacoes):
            continue
        pontuacao_caminho_maior = sum(pontuacoes[1:])
        pontuacao_caminho_menor = sum(pontuacoes[:-1])
        pontuacao_caminho = pontuacao_caminho_maior - pontuacao_caminho_menor
        if pontuacao_caminho > pontuação_melhor_caminho:
            indice_melhor_caminho = index
            pontuação_melhor_caminho = pontuacao_caminho
    if achou_solucao:
        return (novos[indice_solucao], True)
    return (novos[indice_melhor_caminho], False)


def busca_caminho(inicio, destino):
    terminado = False
    caminho = [{'acao': '', 'estado': inicio}]

    finished = False
    while not finished:
        caminhos_possiveis = []
        for index in range(PROFUNDIDADE_BUSCA):
            if index == 0:
                caminhos_possiveis.extend(
                    [[c] for c in gera_possiveis_caminhos(caminho[-1]['estado'])])
            else:
                novos_caminhos = []
                for antigos in caminhos_possiveis:
                    novos_caminhos.extend(
                        [antigos + [novo] for novo in gera_possiveis_caminhos(antigos[-1]['estado'])])
                caminhos_possiveis = novos_caminhos

        melhor_caminho, achou_solucao = seleciona_melhor_caminho(
            caminho, caminhos_possiveis, destino)
        caminho.extend(melhor_caminho)

        if achou_solucao:
            lista_solucao = [estado_eh_destino(
                c['estado'], destino) for c in caminho]
            caminho = caminho[:lista_solucao.index(True) + 1]

            finished = True
    return caminho


def printa_caminho(caminho):
    for item in caminho:
        acao = item['acao']
        estado = item['estado']
        if acao:
            print('\nA acao tomada foi:', acao)
        estado.hal.log()
        estado.bobinas.log(estado)
        estado.vacinas.log(estado)
