try:
    import numpy as np
    from classes.Komorka import Komorka
    from classes.Dostawca import Dostawca
    from classes.Odbiorca import Odbiorca
except ImportError as err:
    raise ImportError(err)


class Optymalizacja:
    tabela = np.zeros((2, 2))

    def __init__(self, dane):  # data user provides
        self.dostawcy = np.zeros(2)  # Provider stuff
        self.odbiorcy = np.zeros(2)  # Supplier stuff
        self.tabela = np.zeros((2, 2))  # later filled up with Nodes
        self.alfa = [0, 0, 0, 0]
        self.beta = [0, 0, 0, 0]
        self.wsp_optymalizacji = np.zeros((2, 2))
        self.dane = dane

        self.zysk = 0  # zysk

        self.set_up()

    def set_up(self):
        self.wsp_optymalizacji[0] = -1
        self.dostawcy = [Dostawca(self.dane["koszty_zakupu"][0], self.dane["podaz"][0]), Dostawca(self.dane["koszty_zakupu"][1], self.dane["podaz"][1])]
        self.odbiorcy = [Odbiorca(self.dane["cena_sprzedazy"][0], self.dane["popyt"][0]), Odbiorca(self.dane["cena_sprzedazy"][1], self.dane["popyt"][1])]

        komorki = [[Komorka(self.odbiorcy[0], self.dostawcy[0], self.dane["koszty_trans_p1"][0]),
                    Komorka(self.odbiorcy[1], self.dostawcy[0], self.dane["koszty_trans_p1"][1])],
                   [Komorka(self.odbiorcy[0], self.dostawcy[1], self.dane["koszty_trans_p2"][0]),
                    Komorka(self.odbiorcy[1], self.dostawcy[1], self.dane["koszty_trans_p2"][1])]]
        self.tabela = np.array(komorki)

        for i in range(2):
            for j in range(2):
                print(self.tabela[i][j].zysk)

    def calc_primary_delivery_plan(self):
        pass

    # next iterations
    def optimize(self):
        if self.is_optimized():
            return self.tabela, self.zysk  # I guess this is what we have to show
        else:
            pass
        """If not start optimize"""

    # loops the optCheckGrid if it finds positive number returns true
    def is_optimized(self):
        return True if self.wsp_optymalizacji.min() < 0 else False
