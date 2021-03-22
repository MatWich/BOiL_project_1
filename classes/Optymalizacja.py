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
        self.alfa = [0, None, None]
        self.beta = [None, None, None]
        self.wsp_optymalizacji = np.zeros((2, 2))
        self.dane = dane
        self.popyt = 0
        self.podaz = 0

        self.zysk = 0  # zysk

    def set_up(self):
        self.wsp_optymalizacji[0][0] = None
        self.wsp_optymalizacji[0][1] = None
        self.wsp_optymalizacji[1][0] = None
        self.wsp_optymalizacji[1][1] = None
        self.dostawcy = [Dostawca(self.dane["koszty_zakupu"][0], self.dane["podaz"][0]),
                         Dostawca(self.dane["koszty_zakupu"][1], self.dane["podaz"][1])]
        self.odbiorcy = [Odbiorca(self.dane["cena_sprzedazy"][0], self.dane["popyt"][0]),
                         Odbiorca(self.dane["cena_sprzedazy"][1], self.dane["popyt"][1])]

        self.komorki = [[Komorka(self.odbiorcy[0], self.dostawcy[0], self.dane["koszty_trans_p1"][0]),
                         Komorka(self.odbiorcy[1], self.dostawcy[0], self.dane["koszty_trans_p1"][1])],
                        [Komorka(self.odbiorcy[0], self.dostawcy[1], self.dane["koszty_trans_p2"][0]),
                         Komorka(self.odbiorcy[1], self.dostawcy[1], self.dane["koszty_trans_p2"][1])]]
        self.calc_total_supply_and_demand()
        self.tabela = np.array(self.komorki)

    def calc_primary_delivery_plan(self):
        newlist = reduce(lambda x, y: x + y, self.komorki)  # zmienia tablice 2d do 1d
        newlist.sort(key=lambda komorka: komorka.zysk, reverse=True)  # sortuje wedlug zysku
        indexes = []

        for i in range(4):
            indexes.append(np.where(
                self.tabela == newlist[i]))  # zwraca tablice z dwoma zmiennymi np [1, 0] a wiec szukany jest w [1][0]
            # print("x: ",indexes[i][0], "y: ", indexes[i][1])

        if self.is_balanced():
            for i in range(4):
                row, col = indexes[i][0][0], indexes[i][1][0]
                if self.dostawcy[row].podaz <= self.odbiorcy[col].popyt != 0 and self.dostawcy[row].podaz != 0:
                    self.komorki[row][col].towar += self.dostawcy[row].podaz
                    self.odbiorcy[col].popyt -= self.dostawcy[row].podaz
                    self.dostawcy[row].podaz = 0

                elif self.odbiorcy[col].popyt < self.dostawcy[row].podaz != 0 and self.odbiorcy[col].popyt != 0:
                    self.komorki[row][col].towar += self.odbiorcy[col].popyt
                    self.dostawcy[row].podaz -= self.odbiorcy[col].popyt
                    self.odbiorcy[col].popyt = 0
        else:
            print("Work in progress")

        # print(newlist)
        # print()

    # next iterations
    def optimize(self):
        counter = 0
        if self.is_optimized() or counter < 10:
            return self.tabela, self.zysk  # I guess this is what we have to show
        else:
            """If not start optimize"""
            counter += 1

    def calc_bases(self):
        if self.is_balanced():
            for i in range(0, 2, 1):
                for j in range(0, 2, 1):
                    if self.komorki[i][j].towar:
                        self.komorki[i][j].set_bazowa(True)
                        self.komorki[i][j].bazowa = True
                    else:
                        self.komorki[i][j].set_bazowa(False)
                        self.komorki[i][j].bazowa = False

    def calc_alfa_beta(self):
        if self.is_balanced():

            if self.komorki[0][0].bazowa:
                self.beta[0] = self.komorki[0][0].zysk - self.alfa[0]

            if self.komorki[0][1].bazowa:
                self.beta[1] = self.komorki[0][1].zysk - self.alfa[0]

            if self.komorki[1][0].bazowa and self.beta[0] is not None:
                self.alfa[1] = self.komorki[1][0].zysk - self.beta[0]

            if self.komorki[1][1].bazowa and self.beta[1] is not None:
                self.alfa[1] = self.komorki[1][1].zysk - self.beta[1]

    def calc_opt_factors(self):
        for i in range(0, 2, 1):
            for j in range(0, 2, 1):
                if not self.komorki[i][j].bazowa and self.alfa[i] and self.beta[j]:
                    self.komorki[i][j].delta = self.komorki[i][j].zysk - self.alfa[i] - self.beta[j]
                    self.wsp_optymalizacji[i][j] = self.komorki[i][j].delta

    # loops the optCheckGrid if it finds positive number returns true
    def is_optimized(self):
        return True if self.wsp_optymalizacji.min() < 0 else False

    def is_balanced(self):
        return True if self.popyt == self.podaz else False

    def clear_alfa_and_beta(self):
        self.alfa = [0, None, None]
        self.beta = [None, None, None]

    """ HELPERS """

    # return 1d array with towar values
    def return_table(self):
        arrayToReturn = [self.komorki[0][0].towar, self.komorki[0][1].towar, self.komorki[1][0].towar,
                         self.komorki[1][1].towar]

        return arrayToReturn

    def calc_total_supply_and_demand(self):
        self.popyt = self.odbiorcy[0].popyt + self.odbiorcy[1].popyt
        self.podaz = self.dostawcy[0].podaz + self.dostawcy[1].podaz

    def print_table(self):
        str1 = '|' + str(self.komorki[0][0]) + ' |' + str(self.komorki[0][1])
        str2 = '|' + str(self.komorki[1][0]) + ' |' + str(self.komorki[1][1])
        str1L = len(str1)
        str2L = len(str2)
        if str1L > str2L:
            lengthString = str1L
        else:
            lengthString = str2L

        top = "|"
        bot = "|"
        separator = "|"
        for _ in range(lengthString - 1):
            separator += '-'
            top += "¯"
            bot += "_"
        separator += '-|'
        top += "¯|"
        bot += "_|"

        while len(str1) < lengthString:
            str1 += ' '
        str1 += ' |'

        while len(str1) < lengthString - 1:
            str2 += ' '
        str2 += ' |'

        print(top + '\n' + str1 + '\n' + separator + '\n' + str2 + '\n' + bot)

    def print_alfa_and_beta(self):
        print("alfy:")
        print(self.alfa)
        print("beta:")
        print(self.beta)

    def print_opt_factors(self):
        print("Wspolczynniki optymalizacji: ")
        lenghtString = 0
        top, bot, sep = '|', '|', '|'

        str1 = "| " + str(self.wsp_optymalizacji[0][0]).replace(str(np.nan), "x") + " | " + str(
            self.wsp_optymalizacji[0][1]).replace(str(np.nan), "x")
        str2 = "| " + str(self.wsp_optymalizacji[1][0]).replace(str(np.nan), "x") + " | " + str(
            self.wsp_optymalizacji[1][1]).replace(str(np.nan), "x")

        if len(str1) > len(str2):
            lengthString = len(str1)
        else:
            lengthString = len(str2)

        for _ in range(lengthString - 1):
            sep += '-'
            top += "¯"
            bot += "_"
        sep += '-|'
        top += "¯|"
        bot += "_|"

        while len(str1) < lengthString:
            str1 += ' '
        str1 += ' |'

        while len(str1) < lengthString - 1:
            str2 += ' '
        str2 += ' |'

        print(top + '\n' + str1 + '\n' + sep + '\n' + str2 + '\n' + bot)


