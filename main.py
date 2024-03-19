from flask import Flask,render_template,request,redirect,url_for,flash
from database import get_data,insert_products,insert_sales,sales_product,profit_product,sales_day,profit_day,register_users

# Create a flask instance.
app = Flask(__name__)
app.secret_key="kssjdnvdvd"
@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/product')
def product():
    data=get_data("products") # Get the products table data.
    return  render_template("product.html",prod=data)

#route to add product
@app.route('/add_product',methods=['post'])
def add_product():
    product_name=request.form["product_name"]
    buying_price=request.form ["buying_price"]
    selling_price=request.form ["selling_price"]
    stock_quantity=request.form["stock_quantity"]
    values=(product_name,buying_price,selling_price,stock_quantity)
    insert_products(values) # Insert
    return redirect(url_for("product"))

@app.route('/sales')
def sales():
    data=get_data("sales")
    products=get_data("products")
    return render_template("sales.html",sal=data,prods=products)
@app.route('/make_sale', methods=['post'])
def make_sale():
    pid=request.form['product_id']
    quantity=request.form['quantity']
    val=(pid,quantity)
    insert_sales(val)
    return redirect(url_for('sales'))
@app.route('/dashboard')
def dashboard():
    sp=sales_product()
    pp=profit_product()
    sd=sales_day()
    pd=profit_day()
    pl=[]
    days=[]
    for m in pd:
        pl.append(float(m[1]))
        days.append(str(m[0]))


    sl=[]
    day=[]
    for p in sd:
        sl.append(float(p[1]))
        day.append(str(p[0]))


    name=[]
    pr=[]
    for i in pp:
        name.append(str(i[0]))
        pr.append(float(i[1]))
    names=[]
    values=[]
    for i in sp:
         names.append(str(i[0]))
         values.append(float(i[1]))
 
    return render_template( 'dashboard.html',names=names,val=values,pr=pr,name=name,sale=sl,day=day,days=days,profit=pl)

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        f_name=request.form['full_name']
        email=request.form['email']
        password=request.form['password']
        val=(f_name,email,password)
        register_users(val)
        flash("you were successfully logged in")
    return render_template( 'reg.html' )



# @app.route('/login',method=['post','get'])
# def login():
#     return render_template('login.html')


app.run(debug=True)
