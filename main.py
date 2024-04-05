from flask import Flask,render_template,request,redirect,url_for,flash,session
from database import get_data,insert_products,insert_sales,sales_product,profit_product,sales_day,profit_day,\
    register_users,check_email,check_logins,sales_per_day,total_sales, todays_profit,total_profit,product_name

# Create a flask instance.
app = Flask(__name__)
app.secret_key="kssjdnvdvd"
@app.route('/')
def hello():
    return render_template('home.html')

@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/product')
def product():
     if 'email' not in session:
        flash("login  to access this page ")
        return redirect(url_for("login"))
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
     if 'email' not in session:
        flash("login  to access this page ")
        return redirect(url_for("login"))
     
     data=get_data("sales")
     products=get_data("products")
     return render_template("sales.html",sal=data,prods=products)


@app.route('/make_sale', methods=['post'])
def make_sale():
    pid=request.form['product_id']
    quantity=request.form['quantity']
    val=(pid,quantity)
    insert_sales(val)
    data=product_name(pid) # get the name of the product using its id
    for i in data:
        product=i
        flash(f'sales made successfully for {quantity} {product}',"success") 
    return redirect(url_for('sales'))
@app.route('/dashboard')
def dashboard():
    if 'email'not in session:
        flash("login to access this page")
        return redirect(url_for("login"))
    spp=sales_per_day()
    ts=total_sales()
    tp= todays_profit()
    total=total_profit()
    print(total)


    
    
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
 
    return render_template( 'dashboard.html',names=names,val=values,pr=pr,name=name,sale=sl,day=day,days=days,profit=pl,spp=spp,ts=ts,tp=tp,total=total)

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        f_name=request.form['full_name']
        email=request.form['email']
        password=request.form['password']
        val=(f_name,email,password)
        if check_email(email):
            
            flash("email already exist use a different email ,","success")
        else:   
             register_users(val)
             flash("you were successfully logged in danger")
    return render_template( 'register.html' )



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        if check_logins(email,password):
            session['email'] = email
            flash("access granted","success")
            return redirect(url_for('home'))
        else:
            flash("wrong password or email try again","danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email',None) # remove the email from
    return redirect(url_for('home'))


app.run(debug=True)
