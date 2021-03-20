import numpy as np
from classes import Komórka, Odbiorca, Dostawca

class Optymalizacja:
    tabela = np.zeros((2,2))
    def __init__(self, dane):           # data user provides
        self.dostawcy = np.zeros(2)            # Provider stuff
        self.odbiorcy = np.zeros(2)            # Supplier stuff
        self.tabela = np.zeros((2, 2))            # later filled up with Nodes
        self.alfa = [0, 0, 0, 0]
        self.beta = [0, 0, 0, 0]
        self.wsp_optymalizacji = np.zeros((2, 2))
        self.dane = dane

        self.zysk = 0                           # zysk

        self.set_up()

    def set_up(self):
        self.wsp_optymalizacji[0] = -1
        self.dostawcy = [Dostawca.Dostawca(self.dane[4][0],self.dane[2][0]),Dostawca.Dostawca(self.dane[4][1],self.dane[2][1])]
        self.odbiorcy = [Odbiorca.Odbiorca(self.dane[5][0],self.dane[3][0]),Odbiorca.Odbiorca(self.dane[5][1],self.dane[3][1])]
        
        komorki = [[Komórka.Komorka(self.odbiorcy[0],self.dostawcy[0],self.dane[0][0]),Komórka.Komorka(self.odbiorcy[1],self.dostawcy[0],self.dane[0][1])],
                    [Komórka.Komorka(self.odbiorcy[0],self.dostawcy[1],self.dane[1][0]),Komórka.Komorka(self.odbiorcy[1],self.dostawcy[1],self.dane[1][1])]]
        self.tabela = np.array(komorki)
        for i in range(2):
            for j in range(2):
                print(self.tabela[i][j].zysk)

    def calc_primary_delivery_plan(self):
        pass
        

    # next iterations
    def optimize(self):
        if self.is_optimized():
            return self.tabela, self.zysk            # I guess this is what we have to show
        else:
            pass
        """If not start optimize"""

    # loops the optCheckGrid if it finds positive number returns true
    def is_optimized(self):
        return True if self.wsp_optymalizacji.min() < 0 else False

