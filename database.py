import psycopg2

#connect to database

conn = psycopg2.connect(host="localhost",dbname="myduka_db",user="postgres",password="mubby",port=5432)
cur = conn.cursor()
# def get_products():
   
#     cur.execute("SELECT * FROM products")
#     prods= cur.fetchall()
#     for prod in prods:
#         print(prod)
   

# get_products()    

# TO GET SALES
# def get_sales():
    
#     cur.execute("SELECT * FROM  sales")
#     sales=cur.fetchall()
#     for sale in sales:
#         print(sale)

# get_sales() 

def get_data(table_name):
    select =f"select * from {table_name}"
  
    cur.execute(select)
    data=cur.fetchall()
    return data

# get_data('sales')
# get_data('products')

#insert data
def insert_products(values):
    products="insert into products(name,buying_price,\
         selling_price,stock_quantity)values(%s,%s,%s,%s);"
    cur.execute(products,values)
    conn.commit()



def register_users(values):
      users="insert into users (full_name,email,password)\
        values(%s,%s,%s)" 
      cur.execute(users,values)
      conn.commit() 

# product_value=("potato",600,1000,10) 
# insert_products(product_value)
# get_data('sales')
# get_data('products') 

#connect sales
def  insert_sales(values):
         sales= "insert into sales(pid,\
            quantity,created_at)values(%s,%s,now())"
         cur.execute(sales,values)
         conn.commit()
sale_value=(2,500)
insert_sales(sale_value)
get_data('sales')  

def sales_product():
      display='select pr.name,sum(pr.selling_price*sl.quantity)\
          as res from products as pr join sales as sl on pr.id=sl.pid group by pr.name;'
      cur.execute(display)
      data=cur.fetchall()
      return data
def profit_product():
      display ='select p.name,sum(((selling_price-buying_price)*quantity))\
          as profit from products as p join sales as s on s.pid=p.id group by p.name;' 
      cur.execute(display)
      data=cur.fetchall()
      return data  

def sales_day():
      display='select date(created_at) as day ,sum (selling_price *quantity)as slp\
          from products as p join sales as s on s.pid=p.id group by day order by day'
      cur.execute(display)
      data=cur.fetchall()
      return data


def profit_day():
     display= 'select date(created_at) as day ,sum(((selling_price-buying_price)*quantity)) as profit \
        from products as p join sales as s on s.pid=p.id group by day order by day;'
     cur.execute(display)
     data=cur.fetchall()
     return data