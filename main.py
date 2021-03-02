from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

'''
@app.route('/get', methods=['GET'])
def index():
    return render_template('index.html')
'''

@app.route('/', methods=['GET', 'POST'])
def my_post_form():
    if request.method == 'POST':
        data = [request.form['text0'], request.form['text1'], request.form['text2'], request.form['text3']]
        

        return render_template('results.html', data=data)
    else:
        return render_template('index.html')



@app.route('/hi/<username>')
def greet(username):
    return f"Hi there, {username}"


if __name__ == '__main__':
    app.run(debug=True)
