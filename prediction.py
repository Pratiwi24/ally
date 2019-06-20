from flask import Flask,render_template,url_for,request
import pandas as pd
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    con = sqlite3.connect("data/toba.sqlite")
    df = pd.read_sql_query("SELECT * from catalog", con)

    X = df['nama'].values.reshape(-1, 1)
    y = df['harga'].values.reshape(-1, 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    print(regressor.intercept_)
    print(regressor.coef_)

    y_pred = regressor.predict(X_test)

    data = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})

    print(y_pred)

    if request.method == 'POST':
        nama = request.form['nama']
        data = [nama]
        my_prediction = regressor.predict(data)

    return print(my_prediction)


if __name__ == '__main__':
    app.run(debug=True)
