class Komorka:
    zysk = 0
    koszt_transportu = 0
    towar = 0
    bazowa: bool
    delta = None

    def __init__(self, o, d, koszt):
        self.koszt_transportu = koszt
        print(o.cena_sprzedazy, "\t", d.koszty_zakupu, "\t", self.koszt_transportu)
        self.zysk = o.cena_sprzedazy - d.koszty_zakupu - self.koszt_transportu
        self.towar = 0  # ile bd przydzielone (podaz / popyt)
        self.bazowa = False    # czy bazowa czy nie bazowa
        self.delta = None

    def __repr__(self):
        return f" ZYSK: {self.zysk} KOSZT_TRANS: {self.koszt_transportu} TOWAR: {self.towar} BAZOWA: {self.bazowa}"

    def set_bazowa(self, boolean):
        self.bazowa = boolean