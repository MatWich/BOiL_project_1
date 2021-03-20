class Komorka:
    zysk = 0
    koszt_transportu = 0
    towar = 0
    def __init__(self, o, d, koszt):
        self.koszt_transportu = koszt   
        print(o.cena_sprzedazy,"\t",d.koszty_zakupu,"\t",self.koszt_transportu)
        self.zysk = o.cena_sprzedazy - d.koszty_zakupu - self.koszt_transportu 
        self.towar = 0     # ile bd przydzielone (podaz / popyt)



