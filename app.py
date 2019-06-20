from flask import Flask, flash, render_template, request, redirect
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route('/')
def catalog():
    return render_template('catalog.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)

    if request.method == 'GET':
        result = request.form
        return render_template("result.html", result=result)

@app.route('/show/<filename>')
def uploaded_file(filename):
    return render_template('catalog.html', filename=filename)


if __name__ == '__main__':
    app.debug = True
    app.run()
