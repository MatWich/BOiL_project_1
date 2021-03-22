from flask import Flask, render_template, url_for, request, redirect
from classes.Optymalizacja import Optymalizacja

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def my_post_form():
    if request.method == 'POST':
        dataForTable = [request.form['text0'], request.form['text1'], request.form['text2'], request.form['text3']]
        
        ''' Do uzupelnienia o te cale obliczenia'''
        """totalGain to niby jest cos tam minus cos tam"""
        dane = {"koszty_trans_p1": [3, 8],
                    "koszty_trans_p2": [4, 2],
                    "podaz": [35, 15],
                    "popyt": [20, 30],
                    "koszty_zakupu": [15, 10],
                    "cena_sprzedazy": [30, 22]}

        op = Optymalizacja(dane)
        op.set_up()
        op.calc_primary_delivery_plan()
        tableData = op.return_table()
        cos_tam1 = 10
        cos_tam2 = 20
        totalGain = cos_tam2 - cos_tam1 # i ta zmienna tez trzeba
        dataForLabels = [cos_tam1, cos_tam2, totalGain]


        # Musimy przekazac 4 elementowa tablice
        return render_template('results.html', dataForTable=tableData, dataForLabels=dataForLabels)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    


