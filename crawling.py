from selenium import webdriver    # 라이브러리에서 사용하는 모듈만 호출

chromedriver = '\\Users\\shw26\\Chromedriver\\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)

from urllib.parse import quote_plus    # 한글 텍스트를 퍼센트 인코딩으로 변환
from selenium import webdriver    # 라이브러리에서 사용하는 모듈만 호출
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException    # 태그가 없는 예외 처리
import time
import pandas as pd


try :							# 정상 처리
	# element = WebDriverWait(driver, 2).until(
	# EC.presence_of_element_located((By.CLASS_NAME, 'prodName'))
	# )

	options = webdriver.ChromeOptions()
	#options.add_argument('headless')    # 웹 브라우저를 띄우지 않는 headless chrome 옵션 적용
	options.add_argument('disable-gpu')		# GPU 사용 안함
	options.add_argument('lang=ko_KR')		# 언어 설정
	driver = webdriver.Chrome(chromedriver, options=options)

	prodName = []
	prodPrice = []
	prodCategory = []
	prodImg = []

	for sort in range(1, 8):
		url="https://cu.bgfretail.com/product/product.do?category=product&depth2=4&depth3=" + str(sort)		# 1~7 page
		driver.get(url)					# 크롤링할 사이트 호출
		time.sleep(20)

		# Click button
		while True:
			try:
				morebtn = driver.find_element_by_class_name('prodListBtn-w')
				morebtn.click()
				print("Click button...")
				time.sleep(15)
			except:
				break

		# Get data
		# first 4 records are dummy record -> except
		prodName_data = driver.find_elements_by_class_name('prodName')
		prodPrice_data = driver.find_elements_by_class_name('prodPrice')
		prodCategory_data = driver.find_element_by_tag_name('h1')			# not elements
		prodImg_data = driver.find_elements_by_class_name('photo')

		for k in prodName_data:
			if k.text != '':
				prodName.append(k.text)
		print(f"Succeed in getting {prodCategory_data.text} prodName...")

		for k in prodPrice_data:
			if k.text !='':
				prodPrice.append(k.text.rstrip('원'))
				prodCategory.append(prodCategory_data.text)
		print(f"Succeed in getting {prodCategory_data.text} prodPrice...")
		print(f"Succeed in getting {prodCategory_data.text} prodCategory...")

		# IMAGE
		i = 0
		for photo in prodImg_data:
			img = photo.find_element_by_tag_name('img')
			img_src = img.get_attribute("src")
			if i >= 4:
				prodImg.append(img_src)
			i += 1
		print(f"Succeed in getting {prodCategory_data.text} prodImg...")

		# print(prodName, len(prodName))
		# print(prodPrice, len(prodPrice))
		# print(prodCategory, len(prodCategory))
		# print(prodImg, len(prodImg))

	# print(prodName, len(prodName))
	# print(prodPrice, len(prodPrice))
	# print(prodCategory, len(prodCategory))
	# print(prodImg, len(prodImg))

	# CSV file
	prod_df = pd.DataFrame({'prodName': prodName, 'prodPrice': prodPrice, 'prodCategory': prodCategory, 'prodImg':prodImg})
	prod_df.to_csv("./products.csv", mode = 'w', encoding = 'utf-8-sig', header = True)


except TimeoutException:
	print('Time out.')

finally:
	driver.quit()				# 크롬 브라우저 닫기
