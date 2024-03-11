from flask import Flask,render_template
from database import get_data

# Create a flask instance.
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template("Home Page")

@app.route('/product')
def product():
    data=get_data("products") # Get the products table data.
    return  render_template("product.html",prod=data)
@app.route('/sales')
def sales():
    data=get_data("sales")
    return render_template("sales.html",sal=data)
app.run(debug=True)