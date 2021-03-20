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
    tab_pocz.calc_primary_delivery_plan()
    cos_tam1 = 10
    cos_tam2 = 20
    totalGain = cos_tam2 - cos_tam1  # i ta zmienna tez trzeba
    dataForLabels = [cos_tam1, cos_tam2, totalGain]


if __name__ == "__main__":
    main()
