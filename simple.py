from pprint import pprint
import json
# Ações
VAI_PARA_LIXO = 'VAI_PARA_LIXO'
VAI_PARA_FREEZER = 'VAI_PARA_FREEZER'
VAI_PARA_MESA_AMB = 'VAI_PARA_MESA_AMB'
VAI_PARA_MESA_TER = 'VAI_PARA_MESA_TER'
VAI_PARA_GELADEIRA = 'VAI_PARA_GELADEIRA'
VAI_PARA_LAVADORA = 'VAI_PARA_LAVADORA'
PEGA = 'PEGA'
COLOCA = 'COLOCA'
ESPERA = 'ESPERA'
ORDENA = 'ORDENA'

ACOES = [VAI_PARA_LIXO, VAI_PARA_FREEZER, VAI_PARA_MESA_AMB, 
         VAI_PARA_MESA_TER, VAI_PARA_GELADEIRA, VAI_PARA_LAVADORA, 
         PEGA, COLOCA, ESPERA, ORDENA]

# Constantes
COMBUSTIVEL_INICIAL = 10
PASSO_TEMPERATURA = 1
TEMPERATURA_INICIAL = -10
PONTO = 1


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
        elif acao == VAI_PARA_LAVADORA and self.posicao != 'lavadora':
            proximo['posicao'] = 'lavadora'
            proximo['combustivel'] -= 1
            proximo_estado_existe = True
        elif acao == VAI_PARA_LIXO and self.posicao != 'lixo':
            proximo['posicao'] = 'lixo'
            proximo['combustivel'] -= 1
            proximo_estado_existe = True

        elif acao == PEGA:
            if self.posicao == 'freezer' and estado.freezer.bobinas:
                proximo['segurando'] = 'bobinas'
                proximo_estado_existe = True
            elif self.posicao == 'geladeira' and estado.geladeira.vacinas:
                proximo['segurando'] = 'vacinas'
                proximo_estado_existe = True
            elif self.posicao == 'mesa_amb' and estado.mesa_amb.bobinas:
                proximo['segurando'] = 'bobinas'
                proximo_estado_existe = True
            elif self.posicao == 'mesa_ter' and estado.mesa_ter.caixa:  ## Conflito, como sabe se pega caixa ou pega vacina ou bobina da caixa?
                proximo['segurando'] = 'caixa'
                proximo_estado_existe = True

        elif acao == COLOCA:
            if self.posicao == 'mesa_amb' and self.segurando == 'bobinas':
                proximo['segurando'] = ''
                proximo_estado_existe = True
            elif self.posicao == 'mesa_ter' and self.segurando == 'bobinas':
                proximo['segurando'] = ''
                proximo_estado_existe = True
            elif self.posicao == 'mesa_ter' and self.segurando == 'vacinas':
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

class Vacinas:
    def __init__(self, definicao={'temp': 5, 'vencidas': True, 'ordenadas': False}):
        self.temp = definicao['temp']
        self.vencidas = definicao['vencidas']
        self.ordenadas = definicao['ordenadas']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if acao == ORDENA and estado.hal.posicao == 'geladeira':
            proximo[ordenadas] = 'True'
        ### Conferir se tem mais coisas ###
        return proximo

    def log(self, estado):
        if estado.hal.segurando == 'vacinas':
            localizacao = 'hal'
        #elif estado.geladeira.vacinas:
        #    localizacao = 'geladeira'
        #elif estado.caixa.vacinas:
        #    localizacao = 'caixa'
        print(f'As vacinas estão no(a) {localizacao} {self.vencidas} e {self.ordenadas}')

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

class Caixa():
    def __init__(self, definicao={'sujo': False, 'bobinas': False, 'vacinas': True}):
        self.sujo = definicao['sujo']
        self.bobinas = definicao['bobinas']
        self.vacinas = definicao['vacinas']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if acao == PEGA and self.bobinas and estado.hal.posicao == 'mesa_ter' and estado.hal.segurando == '':
            proximo['bobinas'] = False
        elif acao == PEGA and self.vacinas and estado.hal.posicao == 'mesa_ter' and estado.hal.segurando == '':
            proximo['vacinas'] = False
        
        elif acao == COLOCA and self.bobinas and estado.hal.posicao == 'mesa_ter':
            proximo['bobinas'] = True
        elif acao == COLOCA and self.vacinas and estado.hal.posicao == 'mesa_ter':
            proximo['vacinas'] = True
        return proximo

    def log(self, estado):
        if estado.hal.segurando == 'caixa':
            localizacao = 'hal'
        elif estado.mesa_ter.caixa:
            localizacao = 'mesa termica'
        print('A caixa termica esta {} no(a) {}, {} e {}'.format(
            'suja' if self.sujo else 'limpas',
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
        return proximo

class MesaTer():
    def __init__(self, definicao={'caixa': True}):
        self.caixa = definicao['caixa']

    def estado_a_partir_da_acao(self, acao, estado):
        proximo = vars(self).copy()
        if acao == PEGA and self.caixa and estado.hal.posicao == 'mesa_ter' and estado.hal.segurando == '':
            proximo['caixa'] = False
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
        return proximo

class Lavadora():
    def __init__(self, definicao={}):
        x=1 # TODO

    def estado_a_partir_da_acao(self, acao, estado):
        x=1 # TODO

class Lixo():
    def __init__(self, definicao={}):
        x=1 # TODO

    def estado_a_partir_da_acao(self, acao, estado):
        x=1 # TODO


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
        self.mesa_ter = MesaTer(
            estado_base['mesa_ter']) if 'mesa_ter' in estado_base else MesaTer()
        self.geladeira = Geladeira(
            estado_base['vacinas']) if 'geladeira' in estado_base else Geladeira()
        self.lixo = Lixo()
        self.lavadora = Lavadora()
        

    def estado_a_partir_da_acao(self, acao):
        hal = self.hal.estado_a_partir_da_acao(acao, self)
        if hal:
            return Estado({
                'hal': hal,
                #'vacinas': self.bobinas.estado_a_partir_da_acao(acao, self),
                'bobinas': self.bobinas.estado_a_partir_da_acao(acao, self),
                'caixa'  : self.caixa.estado_a_partir_da_acao(acao, self),
                'freezer': self.freezer.estado_a_partir_da_acao(acao, self),
                'mesa_amb': self.mesa_amb.estado_a_partir_da_acao(acao, self),
                'mesa_ter': self.mesa_ter.estado_a_partir_da_acao(acao, self),
                #'geladeira': self.geladeira.estado_a_partir_da_acao(acao, self),
                #'lavadora': self.lavadora.estado_a_partir_da_acao(acao, self),
                #'lixo' : self.lixo.estado_a_partir_da_acao(acao, self)
            })
        return None

    def __repr__(self):
        return json.dumps({
            'hal': vars(self.hal),
            'vacinas': vars(self.vacinas),
            'bobinas': vars(self.bobinas),
            'caixa'  : vars(self.caixa),
            'freezer': vars(self.freezer),
            'mesa_amb': vars(self.mesa_amb),
            'mesa_ter': vars(self.mesa_term),
            'geladeira': vars(self.geladeira),
            'lavadora': vars(self.geladeira),
            'lixo': vars(self.lixo)
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



'''
####### TO DO #########
Fazer o hal colocar bobinas e vacinas na caixa térmica quando estiver na mesa térmica


'''