try:
    import numpy as np
    from classes.Komorka import Komorka
    from classes.Dostawca import Dostawca
    from classes.Odbiorca import Odbiorca

    from functools import reduce
except ImportError as err:
    raise ImportError(err)


class Optymalizacja:
    tabela = np.zeros((2, 2))

    def __init__(self, dane):  # data user provides
        self.dostawcy = np.zeros(2)  # Provider stuff
        self.odbiorcy = np.zeros(2)  # Supplier stuff
        self.tabela = np.zeros((2, 2))  # later filled up with Nodes
        self.komorki = [[], []]
        self.alfa = [0, 0, 0, 0]
        self.beta = [0, 0, 0, 0]
        self.wsp_optymalizacji = np.zeros((2, 2))
        self.dane = dane

        self.zysk = 0  # zysk


    def set_up(self):
        self.wsp_optymalizacji[0] = -1
        self.dostawcy = [Dostawca(self.dane["koszty_zakupu"][0], self.dane["podaz"][0]), Dostawca(self.dane["koszty_zakupu"][1], self.dane["podaz"][1])]
        self.odbiorcy = [Odbiorca(self.dane["cena_sprzedazy"][0], self.dane["popyt"][0]), Odbiorca(self.dane["cena_sprzedazy"][1], self.dane["popyt"][1])]

        self.komorki = [[Komorka(self.odbiorcy[0], self.dostawcy[0], self.dane["koszty_trans_p1"][0]),
                    Komorka(self.odbiorcy[1], self.dostawcy[0], self.dane["koszty_trans_p1"][1])],
                   [Komorka(self.odbiorcy[0], self.dostawcy[1], self.dane["koszty_trans_p2"][0]),
                    Komorka(self.odbiorcy[1], self.dostawcy[1], self.dane["koszty_trans_p2"][1])]]

        self.tabela = np.array(self.komorki)


    def calc_primary_delivery_plan(self):
        newlist = reduce(lambda x, y: x + y, self.komorki)          # zmienia tablice 2d do 1d
        newlist.sort(key=lambda komorka: komorka.zysk, reverse=True)        # sortuje wedlug zysku
        indexes = []

        for i in range(4):
            indexes.append(np.where(self.tabela == newlist[i] )) # zwraca tablice z dwoma zmiennymi np [1, 0] a wiec szukany jest w [1][0]
            # print("x: ",indexes[i][0], "y: ", indexes[i][1])

        if self.is_balanced():
            indexPointer = 0
            for i in range(0, 2, 1):
                if i == 1:
                    indexPointer += 1

                for j in range(0, 2, 1):
                    if self.dostawcy[i].podaz <= self.odbiorcy[j].popyt != 0 and self.dostawcy[i].podaz != 0:
                        self.komorki[indexes[i + indexPointer][0][0]][indexes[j + indexPointer][1][0]].towar += self.dostawcy[i].podaz
                        self.odbiorcy[j].popyt -= self.dostawcy[0].podaz
                        self.dostawcy[i].podaz = 0

                    elif self.odbiorcy[j].popyt < self.dostawcy[i].podaz != 0 and self.odbiorcy[j].popyt != 0:
                        self.komorki[indexes[i + indexPointer][0][0]][indexes[j + indexPointer][1][0]].towar += self.odbiorcy[j].popyt
                        self.dostawcy[i].podaz -= self.odbiorcy[j].popyt
                        self.odbiorcy[j].popyt = 0
        else:
            print("Work in progress")

        # print(newlist)
        # print()

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

    def is_balanced(self):
        popyt = self.odbiorcy[0].popyt + self.odbiorcy[1].popyt
        podaz = self.dostawcy[0].podaz + self.dostawcy[1].podaz

        return True if popyt == podaz else False

    """ HELPERS """
    def print_table(self):
        str1 = '|' + str(self.tabela[0][0]) + ' |' + str(self.tabela[0][1])
        str2 = '|' + str(self.tabela[1][0]) + ' |' + str(self.tabela[1][1])
        str1L = len(str1)
        str2L = len(str2)
        if str1L > str2L:
            lengthString = str1L
        else:
            lengthString = str2L

        separator = "|"
        for _ in range(lengthString-1):
            separator += '-'
        separator += '|'

        while len(str1) < lengthString:
            str1 += ' '
        str1 += '|'

        while len(str1) < lengthString -1:
            str2 += ' '
        str2 += '|'

        print(str1)
        print(separator)
        print(str2)
