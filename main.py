import numpy as np
import pandas as pd
import math

class Vacc():       # É criada na geladeira
    def __init__(self, start='Abre'):
        self.vencidas = True    # Vacinas vencidas
        self.ordenada = False   # Vacinas ordenadas por validade
        self.temp = 5.0         # Temperatura

class Bobinas():    # É criada no Freezer
    def __init__(self, start='Abre'):
        self.sujo = False       # Sujo ou não
        self.temp = -10.0       # Temperatura

class Termica():    # É criada na Mesa_Term
    def __init__(self, start='Abre'):
        self.bob = None         # Bobinas
        self.vacc = None        # Vacinas
        #### self.vencidas = None       # Vacinas vencidas  #### como vai possuir objeto vacina, objeto vacina possui parametro vencida
        self.sujo = False       # Sujo ou não

    def take(self, obj):        # Voce pode pegar vacina da caixa, ou bobinas da caixa
        if isinstance(obj, Vacc) and isinstance(self.vacc, Vacc):
            item = self.vacc
            self.vacc = None
            return item
        elif isinstance(obj, Bobinas) and isinstance(self.bob, Bobinas):
            item = self.bob
            self.bob = None
            return item
        return None

    def place(self, obj):       # Voce pode colocar vacinas ou bobinas na caixa
        if isinstance(obj, Vacc) and self.vacc == None:
            self.vacc = obj
            return True
        elif isinstance(obj, Bobinas) and self.bob == None:
            self.bob = obj
            return True
        return False

class Freezer():
    def __init__(self, start='Abre'):
        self.temp = -10.0     # Temperatura
        self.bob = Bobinas(start=start)    # Bobinas

    def take(self, obj):        # Voce pode pegar bobina do freezer
        if isinstance(obj, Bobinas) and isinstance(self.bob, Bobinas):
            item = self.bob
            self.bob = None
            return item
        return None

    def place(self, obj):       # Voce pode colocar bobina no freezer
        if isinstance(obj, Bobinas) and self.bob == None:
            self.bob = obj
            return True
        return False

class Mesa_Amb():
    def __init__(self, start='Abre'):
        self.bob = None       # Bobinas
    
    def take(self, obj):        # Voce pode pegar bobina da mesa
        if isinstance(obj, Bobinas) and isinstance(self.bob, Bobinas):
            item = self.bob
            self.bob = None
            return item
        return None

    def place(self, obj):       # Voce pode colocar bobina na mesa
        if isinstance(obj, Bobinas) and self.bob == None:
            self.bob = obj
            return True
        return False

class Geladeira():
    def __init__(self, start='Abre'):
        self.vacc = Vacc(start=start)

    def take(self, obj):
        if isinstance(obj, Vacc) and isinstance(self.vacc, Vacc):
            item = self.vacc
            self.vacc = None
            return item
        return None

    def place(self, obj):
        if isinstance(obj, Vacc) and self.vacc == None:
            self.vacc = obj
            return True
        return False

    def sort(self):
        self.vacc.ordenada = True

class Mesa_Termica():
    def __init__(self, start='Abre'):
        self.box = Termica(start=start)     # Caixa Termica

    def take(self, obj):    # Take da mesa térmica é diferente, já que apenas na mesa podemos por coisas na caixa térmica,
                            # Então Hal da take bobinas na mesa, mas se a mesa tem a caixa, a mesa da take de bobinas da caixa, e o retorno do item vai para o robo
        if isinstance(obj, Termica) and isinstance(self.box, Termica):
            item = self.box
            self.box = None
            return item
        elif isinstance(obj, Bobinas) and isinstance(self.box, Termica):
            return self.box.take(obj)
        elif isinstance(obj, Vacc) and isinstance(self.box, Termica):
            return self.box.take(obj)
        return None

    def place(self, obj):   # Mesma analogia que take
        if isinstance(obj, Termica) and self.box == None:
            self.box = obj
            return True
        elif isinstance(obj, Bobinas) and isinstance(self.box, Termica):
            self.box.place(obj)
            return True
        elif isinstance(obj, Vacc) and isinstance(self.box, Termica):
            self.box.place(obj)
            return True
        return False

class Lavadora():
    def __init__(self, start='Abre'):
        self.box = False     # Caixa Termica
        self.bob = False   # Bobinas

    def take(self, obj):
        if isinstance(obj, Termica) and isinstance(self.box, Termica):
            item = self.box
            self.box = None
            return item
        elif isinstance(obj, Bobinas) and isinstance(self.bob, Bobinas):
            item = self.bob
            self.bob = None
            return item
        return None
    
    def place(self, obj):       # Voce pode colocar bobinas ou termica na lavadora, ao colocá-las, elas ficarão automaticamente limpas
        if isinstance(obj, Bobinas) and self.bob == None:
            self.bob = obj
            self.bob.sujo = False
            return True
        elif isinstance(obj, Termica) and self.box == None:
            self.box = obj
            self.caixa.sujo = False
            return True
        return False

class Lixo():
    def __init__(self, start='Abre'):
        nothing = 1             # Faz nada

    def take(self, obj):        # Não pode pegar do lixo
        return None

    def place(self, obj):       # Executar place de vacinas no lixo, faz apenas que as vacinas vencidas sejam jogadas
        if isinstance(obj, Vacc):
            obj.vencidas = False
        return False

class HAL():
    def __init__(self, start='Abre', place=None):
        self.pos = place
        self.segurando = None
        self.temp = -10.0

    def go_to(self, to):
        self.pos = to

    def take(self, obj):
        if self.segurando == None:
            item = self.pos.take(obj)
            if item != None:    # Se a função retornou nada, quer dizer que não tem nada para pegar
                self.segurando = item

    def place(self):
        '''
            Para a função place devemos pensar, o robo deve saber o que pode ser posto aonde? tipo, implementar tratamentos por if aqui mesmo?
            OOOUUU o robo tenta dar place no local, e o local "recusa" o objeto (retornando false), e não entraria no if, e então o robo não colocaria o item no local
            OOUU alguma outra coisa ai, por enquanto está da segunda maneira, ele tenta colocar, mas o local não tem "local apropriado" para o objeto em questão, então retorna False
        '''
        if self.pos.place(self.segurando):    # coloca o que estiver segurando no lugar
            self.segurando = None

    def wait(self):
        '''
            STILL NEED IMPLEMENTATION
        '''
        x = 1

    def sort_vacc(self):
        if isinstance(self.pos, Geladeira):
            self.pos.sort()

def abreSala():
    start = 'Abre' 
    
    # instanciando os lugares
    freezer   = Freezer(start)
    mesa_amb  = Mesa_Amb(start)
    geladeira = Geladeira(start)
    mesa_term = Mesa_Termica(start)
    lavadora  = Lavadora(start)
    lixo      = Lixo(start)
    
    # Lista com os lugares possíveis (Instancias dos lugares)
    places = [freezer, mesa_amb, geladeira, mesa_term, lavadora, lixo]  

    # instanciando o robo no lugar da mesa térmica
    robo = HAL(place=mesa_term)  

    # retornando os itens
    vac = geladeira.vacc
    bob = freezer.bob
    box = mesa_term.box

    # Lista de itens disponíveis (instancias dos itens criados)
    items = [vac, bob, box]     

    return places, items, robo


# Initializing first problem    ##### Still need to implement the second problem, this will be done through start variable at constructor, to set starting
#                               ##### parameters regarding the initial state of the Fechamento da sala

places, items, r = abreSala()


## Example of possible actions to solve first problem

print(r.pos)        # show us HAL's starting position
r.go_to(places[0])  # send hal to freezer
r.take(items[1])    # tell hal to take bobinas
r.go_to(places[1])  # send hal to mesa de ambientação
r.place()           # tell hal to place what he is holding where he is at           

r.take(items[0])    # tell hal to take vacinas      ### ele ta na mesa de ambientação, e lá não tem vacinas     #### Teste de erro
r.take(items[1])    # tell hal to take bobinas      ### caso ele tente pegar algo em um lugar que não tem este algo, simplesmente não pegaria nada

r.go_to(places[3])  # send hal to Mesa Termica
r.place()           # tell hal to place bobnias no lugar atual
r.place()           # tell hal to place what he's holding (nothing now) at the actual place                     #### Teste de erro

r.sort_vacc()       # tell hal to sort vaccines     ### he's not at Geladeira                                   #### Teste de erro
r.go_to(places[2])  # send hal to Geladeira
r.sort_vacc()       # tell hal to sort vaccines     ### now he's at Geladeira

r.take(items[0])    # tell hal to take vacinas
r.go_to(places[5])  # send hal to lixo
r.place()           # tell hal to place vacinas (vencidas only) no lixo (deve continuar segurando obj vacinas, mas agr vom vencidas = False)

r.go_to(places[3])  # send hal to mesa termica
r.place()           # tell hal to place (vacinas na caixa termica que ta na mesa termica)

r.take(items[1])    # tell hal to take bobinas
r.take(items[0])    # tell hal to take vacinas  (but he's already holding something)
r.place()           # tell hal to place bobinas in the box again

r.take(items[2])    # tell hal to take Termica      ### Checking if the box on slef.segurando will be everything in there (vacinas e bobinas)

print(r.segurando)  # algo no final pra eu checar o debuger antes do programa quitar



'''
######### A IMPLEMENTAR #########
função fechaSala, e as varíaveis nas construtoras para setar o problema inicial de abreSala e fechaSala
como representar e comparar se o estado atual do sistema representa o estado final que a gente quer? talvez uma função checa as variáveis necessárias
função de perder temperatura com wait()
checar função de limpar na lavadora, que será usada no segundo problema
'''




##########  ANOTAÇÕES DE IDEIAS ANTIGAS (não necessariamente foram utilizadas)   ##################
# Fazer classe template -> se o hal quiser pegar o item do local atual, chama classe.getItem(), podemos ter lista de items

# Como fazer a função de ele poder escolher qual item pegar?
# take(1) 
# take(2)  } para todas as classes?, e se tiver 1 objeto então não importa qual ação, vai pegar aquele objeto?
# take(3) /
#

# como fazer função para ele se deslocar
# ele tem q se deslocar para "acessar" as opções de take, place, etc.. daquele local