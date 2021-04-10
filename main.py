from flask import Flask, render_template, url_for, request, redirect
from classes.Optymalizacja import Optymalizacja

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def my_post_form():
    if request.method == 'POST':
        koszty_trans_p1 = [int(request.form['text0']), int(request.form['text1'])]
        koszty_trans_p2 = [int(request.form['text2']), int(request.form['text3'])]

        podaz = [int(request.form['podaz1']), int(request.form['podaz2'])]
        popyt = [int(request.form['popyt1']), int(request.form['popyt2'])]

        koszty_zakupu = [int(request.form['koszt1']), int(request.form['koszt2'])]
        cena_sprzedazy = [int(request.form['cena1']), int(request.form['cena2'])]

        dane = {"koszty_trans_p1": koszty_trans_p1,
                    "koszty_trans_p2": koszty_trans_p2,
                    "podaz": podaz,
                    "popyt": popyt,
                    "koszty_zakupu": koszty_zakupu,
                    "cena_sprzedazy": cena_sprzedazy}

        """ zakomentowac jesli juz wszystko dziala  """
        # dane = {"koszty_trans_p1": [3, 8],
        #             "koszty_trans_p2": [4, 2],
        #             "podaz": [35, 15],
        #             "popyt": [20, 30],
        #             "koszty_zakupu": [15, 10],
        #             "cena_sprzedazy": [30, 22]}
        """ koniec obszaru do zakomentowania """
        op = Optymalizacja(dane)
        op.set_up()
        op.calc_primary_delivery_plan()
        op.optimize()
        op.calc_all()
        tableData = op.get_balanced_komorki_towar()
        dataForLabels = [op.get_koszt(), op.get_przychod(), op.get_zysk()]
        cost = op.get_komorki_zysk()
        # Musimy przekazac 4 elementowa tablice
        return render_template('results.html', dataForTable=tableData, dataForLabels=dataForLabels, cost=cost)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    


