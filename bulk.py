import pymysql
import csv
from random import randint

conn = pymysql.connect(host='localhost', user='root', password='####', db='convenience_store', charset='utf8')
curs = conn.cursor()
sql = "insert into products (Pid, Pname, price, category, img) values (%s, %s, %s, %s, %s)"
sql_insert_stores = "insert into stores (Bid, Sname, Sowner, address, tel, latitude, longitude, Stockid) values (%s, %s, %s, %s, %s, %s, %s, %s)"
sql_insert_stock = "insert into stock(Stockid) value(%s)"
sql_insert_contains = "insert into contains(Stockid, Pid, quantity) values (%s, %s, %s)"

# f = open('./products.csv', 'r', encoding='utf-8')
# f_stores = open('./stores.csv', 'r', encoding='utf-8')
# f_stock = open('./stock.csv', 'r', encoding='utf-8')

# rd = csv.reader(f_stores)

# for line in rd:
	# curs.execute(sql, (line[0], line[1], line[2], line[3], line[4]))
	# curs.execute(sql_insert_stores, (int(line[0]), line[1], line[2], line[3], line[5], line[7], line[8], line[9]))
	# curs.execute(sql_insert_stock, line[0])

	# print(line)

# insert contain

i = 0
for stock_id in range(1, 5942):
# # 간편식사 : p1~p179(179)
# 	for prod_id in range(1, 31):
# 		curs.execute(sql_insert_contains, (("stock"+str(stock_id)), ("P"+str(prod_id)), randint(0, 300)))
# 		print(i)
# 		i +=1
# # 즉석조리 : p180~p296(117)
# 	for prod_id in range(180, 211):
# 		curs.execute(sql_insert_contains, (("stock"+str(stock_id)), ("P"+str(prod_id)), randint(0, 300)))
# 		print(i)
# 		i +=1
# # 과자류: p297~p1555(1259)
# 	for prod_id in range(297, 328):
# 		curs.execute(sql_insert_contains, (("stock"+str(stock_id)), ("P"+str(prod_id)), randint(0, 300)))
# 		print(i)
# 		i +=1
# # 아이스크림: p1556~p1893(338)
# 	for prod_id in range(1556, 1587):
# 		curs.execute(sql_insert_contains, (("stock"+str(stock_id)), ("P"+str(prod_id)), randint(0, 300)))
# 		print(i)
# 		i +=1
# # 식품: p1894~p3793(1900)
# 	for prod_id in range(1894, 1925):
# 		curs.execute(sql_insert_contains, (("stock"+str(stock_id)), ("P"+str(prod_id)), randint(0, 300)))
# 		print(i)
# 		i +=1
# # 생활용품 : p4976~p6485(1510)
# 	for prod_id in range(4976, 5007):
# 		curs.execute(sql_insert_contains, (("stock"+str(stock_id)), ("P"+str(prod_id)), randint(0, 300)))
# 		print(i)
# 		i +=1
# 음료 : p3794~p4975(1183)
	for prod_id in range(3794, 3825):
		curs.execute(sql_insert_contains, (("stock"+str(stock_id)), ("P"+str(prod_id)), randint(0, 300)))
		print(i)
		i +=1
	conn.commit()

conn.commit()
conn.close()

# f_stores.close()

