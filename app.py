from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


# @app.route('/submit', methods=['GET', 'POST'])
# def submit():
#     print("Submitted...!!!")


if __name__ == '__main__':
    app.run(debug=True)
