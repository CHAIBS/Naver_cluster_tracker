# 네이버 클러스터 추적기
# 셀레늄, 리퀘스트, 뷰티풀수프가 설치되어 있어야 합니다.

from selenium import webdriver
import datetime
import requests
import bs4
import re
import csv
import threading

driver = webdriver.Chrome('C:/Users/chaib/Downloads/chromedriver_win32/chromedriver') # 크롬드라이버 위치
count = 0

def write_Data(keyword, time=60, repeat=3):
	global count
	count += 1
	timer = threading.Timer(time, write_Data) # 반복할 시간입력. 단위는 초

	url = 'https://www.naver.com'
	driver.get(url)
	driver.find_element_by_id("query").send_keys(keyword)
	driver.find_element_by_id("search_btn").click()
	driver.find_element_by_link_text('뉴스 더보기').click()
	driver.implicitly_wait(3)

	html = driver.page_source
	soup = bs4.BeautifulSoup(html,'html.parser')
	cluster_all = soup.findAll('li', id=re.compile('^sp_nws'))

	now = datetime.datetime.now()

	f = open('{0}_{1}_cluster_data.csv'.format(str(now.strftime('%Y%m%d%H%M')), keyword), 'w', newline='')
	wr = csv.writer(f)

	for cluster in cluster_all:
		cluster_title = cluster.find('a', class_='_sp_each_title').text
		cluster_link = cluster.find('a', class_='_sp_each_title').get('href')
		cluster_press = cluster.find('span', class_='_sp_each_source').text
		crawrling_time = now.strftime('%Y-%m-%d %H:%M')
		cluster_time = cluster.find('span', class_='bar').next_sibling

		wr.writerow([cluster_title, cluster_link, cluster_press, crawrling_time, cluster_time,'클러스터 타이틀'])

		if cluster.find('ul', class_='relation_lst') != None:
			cluster_relation = cluster.find('ul', class_='relation_lst')
			relation_all = cluster_relation.findAll('li')
			for relations in relation_all:
				relation_title = relations.find('a').get('title')
				relation_link = relations.find('a').get('href')
				relation_press = relations.find('span', class_='press').text
				relation_time = relations.find('span', class_='bar').next_sibling
				wr.writerow([relation_title, relation_link, relation_press, crawrling_time, relation_time, '관련기사'])

	f.close()

	timer.start()

	if count == repeat: # 반복 주기 설정
		timer.cancel()

if __name__ == '__main__':
	write_Data('삼성')
