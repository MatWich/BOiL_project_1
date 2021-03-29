try:
    import numpy as np
    from classes.Komorka import Komorka
    from classes.Dostawca import Dostawca
    from classes.Odbiorca import Odbiorca

    from functools import reduce
except ImportError as err:
    raise ImportError(err)


class Optymalizacja:
    def __init__(self, dane):
        self.dane = dane
        self.dostawcy = np.zeros(2)  # Provider stuff
        self.odbiorcy = np.zeros(2)  # Supplier stuff
        self.komorki = [[], []]
        self.tabela = np.zeros((2, 2))  # potrzebne do znajdowania najmniejszych wartosci
        self.alfa = [0, None, None]
        self.beta = [None, None, None]
        self.wsp_optymalizacji = np.zeros((2, 2))  # np.zeros((3, 3)) jesli niezbilansowany
        self.popyt = 0
        self.podaz = 0
        self.run = True
        self.zysk = 0
        self.koszt = 0
        self.przychod = 0

    def set_up(self):
        self.calc_total_supply_and_demand()  # calkowita podaz i popyt
        self.clear()  # ustawia kilka rzeczy

        if self.is_balanced():
            self.balanced_set_up()  # DO STUFF IF BALACED
        else:
            self.not_balanced_set_up()  # DO STUFF IF NOT BALANCED

        self.tabela = np.array(self.komorki)

    def calc_primary_delivery_plan(self):
        if self.is_balanced():
            self.balanced_calc_primary_delivery_plan()  # DO STUFF IF BALANCED
        else:
            self.not_balanced_calc_primary_delivery_plan()  # DO STUFF IF NOT BALANCED

    def optimize(self):
        if self.is_balanced():
            self.balanced_optimize()  # DO STUFF IF BALANCED
        else:
            self.not_balanced_optimize()  # DO STUFF IF NOT BALANCED

    def calc_bases(self):
        for i in range(0, len(self.komorki), 1):
            for j in range(0, len(self.komorki[0]), 1):
                if self.komorki[i][j].towar:
                    self.komorki[i][j].bazowa = True
                else:
                    self.komorki[i][j].bazowa = False

    def calc_alfa_beta(self):
        if self.is_balanced():
            self.balanced_calc_alfa_beta()  # DO STUFF IF BALANCED
        else:
            self.not_balanced_calc_alfa_beta()  # DO STUFF IF NOT BALANC

    def calc_opt_factors(self):
        for i in range(0, len(self.komorki), 1):
            for j in range(0, len(self.komorki[0]), 1):
                if not self.komorki[i][j].bazowa and self.alfa[i] and self.beta[j]:
                    self.komorki[i][j].delta = self.komorki[i][j].zysk - self.alfa[i] - self.beta[j]
                    self.wsp_optymalizacji[i][j] = self.komorki[i][j].delta

    def clear(self):
        # FOR BOTH
        for i in range(0, len(self.komorki), 1):
            for j in range(0, len(self.komorki[0]), 1):
                self.komorki[i][j].delta = None
                self.komorki[i][j].bazowa = False
                self.wsp_optymalizacji[i][j] = None

        self.zysk = 0
        self.koszt = 0
        self.przychod = 0

        if self.is_balanced():
            self.balanced_clear()  # DO STUFF IF BALANCED
        else:
            self.not_balanced_clear()  # DO STUFF IF NOT BALANC

    """ ACTUAL FUNCTIONS """

    ''' SET UP'''

    def balanced_set_up(self):
        self.dostawcy = [Dostawca(self.dane["koszty_zakupu"][0], self.dane["podaz"][0]),
                         Dostawca(self.dane["koszty_zakupu"][1], self.dane["podaz"][1])]

        self.odbiorcy = [Odbiorca(self.dane["cena_sprzedazy"][0], self.dane["popyt"][0]),
                         Odbiorca(self.dane["cena_sprzedazy"][1], self.dane["popyt"][1])]

        self.komorki = [[Komorka(self.odbiorcy[0], self.dostawcy[0], self.dane["koszty_trans_p1"][0]),
                         Komorka(self.odbiorcy[1], self.dostawcy[0], self.dane["koszty_trans_p1"][1])],
                        [Komorka(self.odbiorcy[0], self.dostawcy[1], self.dane["koszty_trans_p2"][0]),
                         Komorka(self.odbiorcy[1], self.dostawcy[1], self.dane["koszty_trans_p2"][1])]]

    def not_balanced_set_up(self):
        pass

    ''' CALC PRIMARY DELIVERY PLAN '''

    def balanced_calc_primary_delivery_plan(self):
        newlist = reduce(lambda x, y: x + y, self.komorki)  # zmienia tablice 2d do 1d
        newlist.sort(key=lambda komorka: komorka.zysk, reverse=True)  # sortuje wedlug zysku
        indexes = []

        for i in range(4):
            indexes.append(np.where(
                self.tabela == newlist[i]))  # zwraca tablice z dwoma zmiennymi np [1, 0] a wiec szukany jest w [1][0]
            # print("x: ",indexes[i][0], "y: ", indexes[i][1])

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

    def not_balanced_calc_primary_delivery_plan(self):
        pass

    ''' OPTIMIZE '''

    def balanced_optimize(self):
        counter = 0
        while self.run:
            self.calc_bases()
            self.calc_alfa_beta()
            self.calc_opt_factors()
            flag, highest_X, highest_Y = self.is_optimized()
            if flag or counter >= 10:
                print("Nie ma co optymalizowac")
                self.run = False
                break
            else:
                """If not start optimize"""
                counter += 1
                self.get_cycle(highest_X, highest_Y)

                print(f"After iteration {counter} ")
                self.print_table()
                self.calc_all()
                self.clear()

    def not_balanced_optimize(self):
        pass

    def get_cycle(self, x, y): 
        if x > 0:
            column = 0
        
            for i in range(len(self.wsp_optymalizacji[x])):
                if self.wsp_optymalizacji[x-1][i] == None and self.wsp_optymalizacji[x][i] == None:
                    column = i
                    break
            
            tmp = 0
            if self.komorki[x-1][y].towar < self.komorki[x][column].towar:
                tmp = self.komorki[x-1][y].towar
            else:
                tmp = self.komorki[x][column].towar
            
            self.komorki[x][y].towar += tmp
            self.komorki[x-1][column].towar += tmp
            self.komorki[x-1][y].towar -= tmp
            self.komorki[x][column].towar -= tmp
        else:
            column = 0
        
            for i in range(len(self.wsp_optymalizacji[x])):
                if self.wsp_optymalizacji[x+1][i] == None and self.wsp_optymalizacji[x][i] == None:
                    column = i
                    break
            
            tmp = 0
            if self.komorki[x+1][y].towar < self.komorki[x][column].towar:
                tmp = self.komorki[x+1][y].towar
            else:
                tmp = self.komorki[x][column].towar
            
            self.komorki[x][y].towar += tmp
            self.komorki[x+1][column].towar += tmp
            self.komorki[x+1][y].towar -= tmp
            self.komorki[x][column].towar -= tmp


    ''' CALC ALFA BETA '''

    def balanced_calc_alfa_beta(self):
        if self.komorki[0][0].bazowa:
            self.beta[0] = self.komorki[0][0].zysk - self.alfa[0]

        if self.komorki[0][1].bazowa:
            self.beta[1] = self.komorki[0][1].zysk - self.alfa[0]

        if self.komorki[1][0].bazowa and self.beta[0] is not None:
            self.alfa[1] = self.komorki[1][0].zysk - self.beta[0]

        if self.komorki[1][1].bazowa and self.beta[1] is not None:
            self.alfa[1] = self.komorki[1][1].zysk - self.beta[1]

    def not_balanced_calc_alfa_beta(self):
        pass

    ''' CALC OPT FACTORS '''

    def balanced_calc_opt_factors(self):
        pass

    def not_balanced_calc_opt_factors(self):
        pass

    def balanced_clear(self):
        self.alfa = [0, None]
        self.beta = [None, None]

    def not_balanced_clear(self):
        self.alfa = [0, None, None]
        self.beta = [None, None, None]

    """ GETTERS AND SETTERS """

    def get_koszt(self):
        return self.koszt

    def get_zysk(self):
        return self.zysk

    def get_przychod(self):
        return self.przychod

    def get_komorki(self):
        return self.komorki

    def get_komorki_zysk(self):
        tabToReturn = []
        for i in range(0, len(self.komorki)):
            for j in range(0, len(self.komorki[0])):
                tabToReturn.append(self.komorki[i][j].zysk)

        return tabToReturn


    ##################################### NWM DLACZEGO NIE DZIALA###########################
    def get_komorki_towar(self):
        if self.is_balanced():
            self.get_balanced_komorki_towar()  # DO STUFF IF BALANCED
        else:
            self.get_not_balanced_komorki_towar()  # DO STUFF IF NOT BALANC

    def get_balanced_komorki_towar(self):
        return [self.komorki[0][0].towar, self.komorki[0][1].towar, 0, self.komorki[1][0].towar,
                self.komorki[1][1].towar, 0, 0, 0, 0]

    def get_not_balanced_komorki_towar(self):
        return [self.komorki[0][0].towar, self.komorki[0][1].towar, self.komorki[0][2].towar, self.komorki[1][0].towar,
                self.komorki[1][1].towar, self.komorki[1][2].towar, self.komorki[2][0].towar, self.komorki[2][1].towar,
                self.komorki[2][2].towar]



    """ UTILITIES """

    def is_balanced(self):
        return True if self.popyt == self.podaz else False

    def calc_total_supply_and_demand(self):
        self.podaz = self.dane["podaz"][0] + self.dane["podaz"][1]
        self.popyt = self.dane["popyt"][0] + self.dane["popyt"][1]


    # loops the optCheckGrid if it finds positive number returns true
    def is_optimized(self):
        highest = -999999
        for i in range(len(self.wsp_optymalizacji)):
            for j in range(len(self.wsp_optymalizacji[0])):
                if highest < self.wsp_optymalizacji[i][j]:
                    highest = self.wsp_optymalizacji[i][j]
                    highest_X = i
                    highest_Y = j

        return True if highest < 0 else False, highest_X, highest_Y

    def calc_all(self):
        self.calc_total_cost()
        self.calc_total_income()
        self.calc_benefit()

    def calc_total_cost(self):
        for i in range(len(self.komorki)):
            for j in range(len(self.komorki[0])):
                self.koszt += self.komorki[i][j].towar * (
                        self.komorki[i][j].koszt_transportu + self.dostawcy[i].koszty_zakupu)
        print("Calkowity koszt:\t", self.koszt)

    def calc_total_income(self):
        for i in range(2):
            for j in range(2):
                self.przychod += self.komorki[i][j].towar * self.odbiorcy[j].cena_sprzedazy
        print("Calkowity przychod:\t", self.przychod)

    def calc_benefit(self):
        self.zysk = self.przychod - self.koszt
        print("Zysk pośrednika:\t", self.zysk)

    """ HELPERS """

    def print_table(self):
        if self.is_balanced():
            self._balanced_print_table()  # DO STUFF IF BALACED
        else:
            self._not_balanced_print_table()  # DO STUFF IF NOT BALANCED

    def _balanced_print_table(self):
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

        while len(str2) < lengthString:
            str2 += ' '
        str2 += ' |'
        str1 += ' |'

        print(top + '\n' + str1 + '\n' + separator + '\n' + str2 + '\n' + bot)

    def _not_balanced_print_table(self):
        str1 = '|' + str(self.komorki[0][0]) + ' |' + str(self.komorki[0][1]) + ' |' + str(self.komorki[0][2])
        str2 = '|' + str(self.komorki[1][0]) + ' |' + str(self.komorki[1][1]) + ' |' + str(self.komorki[1][2])
        str3 = '|' + str(self.komorki[2][0]) + ' |' + str(self.komorki[2][1]) + ' |' + str(self.komorki[2][2])

        lengthArr = [len(str1), len(str2), len(str3)]
        lengthString = max(lengthArr)

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

        while len(str2) < lengthString:
            str2 += ' '
        str2 += ' |'
        str1 += ' |'

        print(top + '\n' + str1 + '\n' + separator + '\n' + str2 + '\n' + str3 + '\n' + bot)

    def print_alfa_and_beta(self):
        print("alfy:")
        print(self.alfa)
        print("beta:")
        print(self.beta)

    def print_opt_factors(self):
        print("Wspolczynniki optymalizacji: ")
        if self.is_balanced():
            self._balanced_print_opt_factors()  # DO STUFF IF BALACED
        else:
            self._not_balanced_print_opt_factors()  # DO STUFF IF NOT BALANCED

    def _balanced_print_opt_factors(self):
        lenghtString = 0
        top, bot, sep = '|', '|', '|'
        str1 = "| " + str(self.wsp_optymalizacji[0][0]).replace(str(np.nan), "x") + " | " + str(
            self.wsp_optymalizacji[0][1]).replace(str(np.nan), "x")
        str2 = "| " + str(self.wsp_optymalizacji[1][0]).replace(str(np.nan), "x") + " | " + str(
            self.wsp_optymalizacji[1][1]).replace(str(np.nan), "x")

        lengthArr = [len(str1), len(str2)]
        maxLength = max(lengthArr)

        for _ in range(maxLength - 1):
            sep += '-'
            top += "¯"
            bot += "_"
        sep += '-|'
        top += "¯|"
        bot += "_|"

        while len(str1) < maxLength:
            str1 += ' '

        while len(str2) < maxLength:
            str2 += ' '

        str1 += ' |'
        str2 += ' |'

        print(top + '\n' + str1 + '\n' + sep + '\n' + str2 + '\n' + bot)

    def _not_balanced_print_opt_factors(self):
        lenghtString = 0
        top, bot, sep = '|', '|', '|'
        str1 = "| " + str(self.wsp_optymalizacji[0][0]).replace(str(np.nan), "x") + " | " + str(
            self.wsp_optymalizacji[0][1]).replace(str(np.nan), "x") + " | " + str(self.wsp_optymalizacji[0][2]).replace(
            str(np.nan), "x")
        str2 = "| " + str(self.wsp_optymalizacji[1][0]).replace(str(np.nan), "x") + " | " + str(
            self.wsp_optymalizacji[1][1]).replace(str(np.nan), "x") + " | " + str(self.wsp_optymalizacji[1][2]).replace(
            str(np.nan), "x")
        str3 = "| " + str(self.wsp_optymalizacji[2][0]).replace(str(np.nan), "x") + " | " + str(
            self.wsp_optymalizacji[2][1]).replace(str(np.nan), "x") + " | " + str(self.wsp_optymalizacji[2][2]).replace(
            str(np.nan), "x")

        lengthArr = [len(str1), len(str2), len(str3)]
        maxLength = max(lengthArr)

        for _ in range(maxLength - 1):
            sep += '-'
            top += "¯"
            bot += "_"
        sep += '-|'
        top += "¯|"
        bot += "_|"

        while len(str1) < maxLength:
            str1 += ' '

        while len(str2) < maxLength:
            str2 += ' '

        while len(str3) < maxLength:
            str3 += ' '

        str1 += ' |'
        str2 += ' |'
        str3 += ' |'

        print(top + '\n' + str1 + '\n' + sep + '\n' + str2 + '\n' + sep + '\n' + str3 + '\n' + bot)