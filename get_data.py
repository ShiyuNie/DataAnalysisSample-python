

# -*- coding:utf-8 -*-

import urllib
import urllib.request as urlib2
import requests
from bs4 import BeautifulSoup
import re
import xlwt
from urllib import request
from urllib.parse import urlencode
import urllib.parse
import json
#from lxml import etree
import numpy as np
import pandas as pd
import time
import random
import codecs







# 设定数据数组

job_id = []
job_name = []
job_type = []
job_lables = []
company_shortname = []
company_fullname = []
salary = []
city = []
job_description = []
job_experience = []
education = []
skill_lables = []
approve = []
job_status = []
job_advantagelist = []
release_time = []
industry_field = []
industry_lables = []
company_size = []
work_place = []
finance_phase = []
ref_url=[]






# 读取post列表内容

def readpost(Np):
	# 转换并提交表单
	search0 = {
	'first': True,
	'pn': Np,
	'kd': '数据分析'}
	search = urlencode(search0, encoding='utf-8')
	headers = {
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Host': 'www.lagou.com',
	'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
	}
	url0 = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput='
	url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
	s = requests.Session() # 建立session
	s.get(url=url0, headers=headers, timeout=3)
	cookie = s.cookies # 获取cookie
	response = s.post(url=url, headers=headers, data=search, cookies=cookie, timeout=3)
	#response.encoding = 'utf-8'
	result = response.json()
	#time.sleep(10)	# 暂停防止被判断为robot被禁IP
	#print(response.text)
	#print(result)

	# 打印确认网页内容读取正确
	#file=open("check.txt","w")  
	#file.write()
	#file.write(response.text)
	#file.close()

	return result




# 读取网页html内容

def readcontent(url):
	headers = {
	#'Accept':'text/html,appication/xhtml+xml,appication/xml;q=0.9,*/*;q=0.8',
	#'Accept-Encoding':'gzip, deflate, br',
	#'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	#'Cache-Control':'max-age=0',
	#'Connection':'keep-aive',
	#'Cookie':'SEARCH_ID=f18ed0d91f284a4ba9dc3436b86cb3af; user_trace_token=20190423174133-9438476d-8dfe-4a84-a5bd-41ea56b0efed; _ga=GA1.2.1695238510.1556012496; LGUID=20190423174136-fce58666-65ab-11e9-b0a5-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAFCAAEGB16BD559F11E7BB523E66109AEA19C41; X_HTTP_TOKEN=247ddaf7744eb46c1688606551991aab42a50378b0; LGRID=20190424092102-399231d5-662f-11e9-9c4c-5254005c3644; TG-TRACK-CODE=index_search; X_MIDDLE_TOKEN=92b57399577be6f5b54315dcf1630bb8; ab_test_random_num=0; _putrc=45B8AC8F09A983DE123F89F2B170EADC; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B79813; hasDeiver=0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPubish=1; LG_LOGIN_USER_ID=0fb5cf8e1e2c7d9c19c4bd60cf17d5628e5b55c561d4e862145982b8c922c88d; gate_login_token=cc600482552807aa47e1073af478f11e8da0d36bb371fdb873160d7221a86521; LGSID=20190424090538-12828c4e-662d-11e9-9c4c-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Fist_%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; _gat=1',
	#'Host':'www.lgstatic.com',
	#'Referer':'https://www.lagou.com/jobs/ist_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
	#'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
	}
	request = urlib2.Request(url,headers=headers)
	response = urlib2.urlopen(request)
	print(url,response.code)	# 确认读取成功 200
	pageContent = response.read()
	time.sleep(10)

	# 网页解压缩
	#gzipped = response.headers.get('Content-Encoding')
	#if gzipped:
	#	html = zib.decompress(html, 16+zib.MAX_WBITS)
	#print(html)

	# 打印确认网页内容读取正确
	#file=open("test_url.txt","wb")  
	#file.write(pageContent)
	#file.write(html)
	#file.close()

	return pageContent

	



# 若无数据则填入Null

def add(a,b):
	if isinstance(b,str):
		if len(b):
			a.append(b)
		else:
			a.append('Null')
	else:
		if len(str(b)):
			a.append(b)
		else:
			a.append('Null')
	



# 列表写入文件
def listwri(file,list):
	print(len(list))
	for i in range(len(list)):
		#file.write("<user>\n   <id>"+str(i)+"</id>\n</user>\n")
		s = str(list[i]).replace('[','').replace(']','')    # 去除[],这两行按数据不同，可以选择
		s = s.replace("'",'') + ' '   # 去除单引号，每行末尾追加空格符
		file.write(s)
	file.write('\n')






# 读取post数据

def getpostData(Np):
	# 读取列表所需内容
	result = readpost(Np)
	job_info = result['content']['positionResult']['result']

	# 所需内容赋予数组
	for i in job_info:
		positionName = i['positionName']  # 职位名称
		firstType = i['firstType']  # 职位大分类，如产品或技术
		secondType = i['secondType']  # 职位中分类，如数据分析
		thirdType = i['thirdType']  # 职位细分类，如大数据
		companyShortName = i['companyShortName']	# 公司简称
		companyFullName = i['companyFullName']  # 公司全称
		industryField = i['industryField']	# 行业领域
		industryLables = i['industryLables']  # 行业标签，列表
		positionLables = i['positionLables']  # 职位标签，列表
		jobNature = i['jobNature']  # 全职兼职
		dist = i['city']  # 城市
		sal = i['salary']  # 薪资
		edu = i['education']  # 学历要求
		workYear = i['workYear']  # 工作经验
		skillLables = i['skillLables']  # 技能标签,列表
		appNo = i['approve']	# 招聘人数
		positionAdvantage = i['positionAdvantage']  # 工作优势
		companyLabelList = i['companyLabelList']  # 福利待遇，列表
		companySize = i['companySize']  # 公司规模人数
		financeStage = i['financeStage']  # 上市融资
		positionId = i['positionId']  # 招聘ID
		createTime = i['createTime']  # 发布时间

		detail_url = 'https://www.lagou.com/jobs/{}.html'.format(positionId)	# 职位链接
        #print('%s 拉勾网链接:-> %s' % (companyShortName, detail_url))
		positiontype = firstType + '-' + secondType + '-' + thirdType	# 职位类型
		joblbs = ''		# 职位标签
		for j in positionLables:
			joblbs += j + ' '
		skilllbs = ''	# 技能标签
		for j in skillLables:
			skilllbs += j + ' '
		indulbs = ''	# 行业标签
		for j in industryLables:
			indulbs += j + ' '
		advlbs = positionAdvantage	# 福利列表
		for j in companyLabelList:
			advlbs += j + ' '

		add(job_id, positionId)
		add(job_name, positionName)
		add(job_type, positiontype)
		add(job_lables, joblbs)
		add(company_shortname, companyShortName)
		add(company_fullname, companyFullName)
		add(salary, sal)
		add(city, dist)
		add(job_experience, workYear)
		add(education, edu)
		add(skill_lables, skilllbs)
		add(approve, appNo)
		add(job_status, jobNature)
		add(job_advantagelist, advlbs)
		add(release_time, createTime)
		add(industry_field, industryField)
		add(industry_lables, indulbs)
		add(company_size, companySize)
		add(finance_phase, financeStage)

		add(ref_url, detail_url)






# 得到网页中数据

def getdetData(newurl):
	# 读取解析网页内容
	#newurl = 'https://www.lagou.com/jobs/5545028.html'
	pageContent=readcontent(newurl)
	soup = BeautifulSoup(pageContent, "html.parser")

	# 读取职位描述
	result1 = soup.findAll('dd', attrs = {"class" : "job_bt"})
	for i in result1:
		temp1 = i.findAll('div', attrs = {"class" : "job-detail"})
		s1 = temp1[0].get_text()
		add(job_description, s1)

	# 读取工作地点
	result2 = soup.findAll('dd', attrs = {"class" : "job-address clearfix"})
	for i in result2:
		temp2 = i.findAll('div', attrs = {"class" : "work_addr"})
		s2 = temp2[0].get_text()
		add(work_place, s2)










if __name__ == '__main__':
	# 共30页网页，循环读取，每个网页另有有15个链接读取
	for i in range(0,30):
		Np=i+1
		getpostData(Np)
		for j in range(i*15,(i+1)*15):
			#newurl = ref_url[i]
			getdetData(ref_url[j])
			#print(j,len(work_place),len(job_description))	
		time.sleep(10)	# 间隔一段时间以免被封IP

		# 写入dataframe表格，存入csv
		data = pd.DataFrame({
			"job_id":job_id,
			"job_name":job_name,
			"job_type":job_type,
			"job_lables":job_lables,
			"company_shortname":company_shortname,
			"company_fullname":company_fullname,
			"city":city,
			"salary":salary,
			"job_experience":job_experience,
			"education":education,
			"skill_lables":skill_lables,
			"approve":approve,
			"job_status":job_status,
			"work_place":work_place,
			"job_description":job_description,
			"job_advantagelist":job_advantagelist,
			"industry_field":industry_field,
			"industry_lables":industry_lables,
			"company_size":company_size,
			"finance_phase":finance_phase,
			"release_time":release_time
			})
		output = 'data_analysis2' + str(i)+ '.csv'
		data.to_csv(output, index=True, header=True, encoding='utf_8_sig')

	# 打印确认网页内容读取正确
	#file = codecs.open("check_list.txt",'a','utf-8-sig')
	#listwri(file,job_id)
	#listwri(file,job_name)
	#listwri(file,job_type)
	#listwri(file,job_lables)
	#listwri(file,company_shortname)
	#listwri(file,company_fullname)
	#listwri(file,salary)
	#listwri(file,city)
	#listwri(file,job_description)	
	#listwri(file,job_experience)
	#listwri(file,education)
	#listwri(file,skill_lables)
	#listwri(file,approve)
	#listwri(file,job_status)
	#listwri(file,job_advantagelist)
	#listwri(file,release_time)
	#listwri(file,industry_field)
	#listwri(file,industry_lables)
	#listwri(file,company_size)
	#listwri(file,work_place)	
	#listwri(file,finance_phase)
	#istwri(file,ref_url)
	#file.close()

# 	检查读取
#	newurl = ref_url[10]
#	getdetData(newurl)
#	checkdata = pd.DataFrame({
#		'work_place': work_place,
#		'job_description': job_description
#		})
#	checkdata.to_csv('checkdata.csv', index=True, header=True, encoding='utf_8_sig')
	

