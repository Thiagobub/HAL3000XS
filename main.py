import numpy as np
import pandas as pd
import math

class Vacc():
    def __init__(self):
        self.vencidas = True          # Vacinas vencidas
        self.ordenada = False       # Vacinas ordenadas por validade
        self.temp = 5.0            # Temperatura

class Bobinas():
    def __init__(self):
        self.sujo = False           # Sujo ou não
        self.temp = -10.0            # Temperatura

class Termica():
    def __init__(self):
        self.bob = None               # Bobinas
        self.vacc = None              # Vacinas
        self.vencidas = None          # Vacinas vencidas
        self.sujo = False           # Sujo ou não

class Freezer():
    def __init__(self):
        self.temp = -10.0     # Temperatura
        self.bob = True        # Bobinas

class Mesa_Amb():
    def __init__(self):
        self.bob = False       # Bobinas

class Geladeira():
    def __init__(self):
        self.vacc = True      # Vacinas

class Mesa_Termica():
    def __init__(self):
        self.caixa = True     # Caixa Termica

class Lavadora():
    def __init__(self):
        self.caixa = False     # Caixa Termica
        self.bobinas = False   # Bobinas

class Lixo():
    def __init__(self):
        self.vacc = None      # Vacinas

class State():
    def __init__(self):
        self.freezer = Freezer()
        self.mesa_amb = Mesa_amb()
        self.geladeira = Geladeira()
        self.mesa_caixa =  Mesa_Amb()
        self.lavadora = Lavadora()
        self.lixo = Lixo()

class HAL():
    def __init__(self):
        self.pos = 'Freezer'
        self.segurando = None
        self.temp = -10.0

    def go_to(self):
        x = 1   # todo

    def take(self):
        x = 1   # todo

    def place(self):
        x = 1   # todo

    def wait(self):
        x = 1   # todo

    def sort_vax(self):
        x = 1   # todo
