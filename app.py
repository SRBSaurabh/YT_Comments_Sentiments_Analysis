from flask import Flask, render_template, request
from main import get_Sentiments

import nltk
nltk.download('stopwords')

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/catch_URL')
def catch_URL():
    print("Submitted...!!!")
    URL = request.args.get("userURL")
    print('Processing.......', URL)
    answer = get_Sentiments(URL)
    print(answer)
    return f"<html><body><h1>{answer}</h1></body></html>"


if __name__ == '__main__':
    app.run(debug=True)
