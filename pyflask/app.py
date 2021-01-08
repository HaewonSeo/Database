from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)
conn = pymysql.connect(host='localhost', user='root', password='####', db='convenience_store', charset='utf8')
curs = conn.cursor()

# main page
@app.route('/')
def index():
	return render_template('index.html')

# store list
@app.route('/store_list',  methods=['GET'])
def store_list():
	user_latitude = request.args["latitude"]
	user_longitude = request.args["longitude"]

	sql_stores =	"select * \
					from stores\
					where (latitude between %s-0.01 and %s+0.01) and (longitude between %s-0.1 and %s+0.1)"\
						% (user_latitude, user_latitude, user_longitude, user_longitude)

	curs.execute(sql_stores)
	stores = curs.fetchall()



	sql_products =	"select *\
					from contains natural join products\
					where Stockid in (\
						select stockid\
						from stores\
						where (latitude between %s-0.01 and %s+0.01) \
							and (longitude between %s-0.1 and %s+0.1));"\
							% (user_latitude, user_latitude, user_longitude, user_longitude)

	curs.execute(sql_products)
	products = curs.fetchall()

	conn.commit()
	return render_template('store_list.html', store_list = stores, product_list = products)

# login
@app.route('/login', methods=['POST'])
def login():
	user_Bid = request.form['Bid']
	user_pwd = request.form['pwd']

	sql_login =	"select *\
				from stores\
				where Bid='%s' and pwd='%s';" %(user_Bid, user_pwd)

	sql_products =	"select *\
					from contains natural join products\
					where Stockid = (\
						select Stockid\
						from stores\
						where Bid=%s and pwd=%s);" %(user_Bid, user_pwd)

	curs.execute(sql_login)
	login_user = curs.fetchone()

	# fail to login
	if login_user == None:
		print("fail to login")
		return render_template('index.html')

	curs.execute(sql_products)
	products = curs.fetchall()
	print("login..")

	conn.commit()
	return render_template('store_manage.html', user=login_user, product_list = products)


@app.route('/update', methods=['GET', 'POST'])
def update():
	# delete
	if request.method == "GET":
		delete_Stockid = request.args['Stockid']
		delete_Pid  = request.args['Pid']

		# select * -> delete
		sql_delete = "delete\
					from contains\
					where Stockid='%s' and Pid='%s';" %(delete_Stockid, delete_Pid)

		sql_login =	"select *\
					from stores\
					where Stockid='%s';" %(delete_Stockid)

		sql_products =	"select *\
						from contains natural join products\
						where Stockid='%s';" %(delete_Stockid)

		curs.execute(sql_delete)
		print("deleted..")

		curs.execute(sql_login)
		login_user = curs.fetchone()

		curs.execute(sql_products)
		products = curs.fetchall()

		conn.commit()
		return render_template('store_manage.html', user=login_user, product_list = products)

	# update
	elif request.method == "POST":
		update_Stockid = request.form['Stockid']
		update_Pid  = request.form['Pid']
		update_quantity = request.form['quantity']

		sql_update = "update contains\
					set quantity=%s\
					where Stockid='%s' and Pid='%s';" %(update_quantity, update_Stockid, update_Pid)

		sql_login =	"select *\
					from stores\
					where Stockid='%s';" %(update_Stockid)

		sql_products =	"select *\
						from contains natural join products\
						where Stockid='%s';" %(update_Stockid)

		curs.execute(sql_update)
		print("updated..")

		curs.execute(sql_login)
		login_user = curs.fetchone()

		curs.execute(sql_products)
		products = curs.fetchall()

		conn.commit()
		return render_template('store_manage.html', user=login_user, product_list = products)

# insert
@app.route("/insert", methods=['GET'])
def insert():
	if request.method == "GET":
		insert_Stockid = request.args['Stockid']
		insert_Pname  = request.args['Pname']
		insert_quantity = request.args['quantity']

	try:
		sql_select_Pid = ("select Pid\
							from products\
								where Pname like '%{}%';").format(insert_Pname)

		curs.execute(sql_select_Pid)
		insert_Pid = curs.fetchone()[0]

		sql_insert = "insert into contains(Stockid, Pid, quantity)\
					values('%s','%s','%s');" %(insert_Stockid, insert_Pid, insert_quantity)

		curs.execute(sql_insert)
		conn.commit()
		print("inserted..")


	# error value of Pid
	except:
		print("error value of Pid")

	sql_login =	"select *\
				from stores\
				where Stockid='%s';" %(insert_Stockid)

	curs.execute(sql_login)
	login_user = curs.fetchone()

	sql_products =	"select *\
					from contains natural join products\
					where Stockid='%s';" %(insert_Stockid)

	curs.execute(sql_products)
	products = curs.fetchall()
	conn.commit()

	return render_template('store_manage.html', user=login_user, product_list = products)

if __name__ == '__main__':
	app.run()


conn.close()
