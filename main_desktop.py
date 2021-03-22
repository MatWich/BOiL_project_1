from classes.Optymalizacja import Optymalizacja


def main():
    dane = [[3, 8],  # koszty transportu p1
            [4, 2],  # koszty transportu p2
            [35, 15],  # podaz
            [20, 30],  # popyt
            [15, 10],  # koszty zakupu
            [30, 22]  # cena sprzedazy
            ]

    daneDict = {"koszty_trans_p1": [3, 8],
                "koszty_trans_p2": [4, 2],
                "podaz": [35, 15],
                "popyt": [20, 30],
                "koszty_zakupu": [15, 10],
                "cena_sprzedazy": [30, 22]}

    tab_pocz = Optymalizacja(daneDict)
    tab_pocz.set_up()
    tab_pocz.calc_primary_delivery_plan()
    tab_pocz.calc_bases()
    tab_pocz.calc_alfa_beta()
    tab_pocz.calc_opt_factors()
    print('Zooptymalizane: ', tab_pocz.is_optimized())
    tab_pocz.print_opt_factors()
    print("Before")
    tab_pocz.print_table()
    tab_pocz.optimize()
    # cos_tam1 = 10
    # cos_tam2 = 20
    # totalGain = cos_tam2 - cos_tam1  # i ta zmienna tez trzeba
    # dataForLabels = [cos_tam1, cos_tam2, totalGain]

    tab_pocz.print_alfa_and_beta()
    tab_pocz.print_table()


if __name__ == "__main__":
    main()
