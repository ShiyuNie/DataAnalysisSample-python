
import numpy as np
import math
import pandas as pd

import scipy as sc
import random

import jieba
import jieba.analyse

import matplotlib as mpl
import matplotlib.pyplot as plt
#from matplotlib.font_manager import fontproperties
import seaborn as sn
from wordcloud import WordCloud
# matplotlib inline
plt.rcParams['figure.figsize'] = (10, 6)
#plt.style.use('ggplot')
import pprint
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签




# 读数据
data = pd.read_csv("LaGou_DataAnalyst.csv",encoding='utf_8_sig')
print(data.dtypes.value_counts()) # 查看每列数据类型
print(data.shape)  # 查看数据的行列大小
data.info()
#test = data.head(30)  # 查看前30行
#print(test)


# 备份data1
data1 = data.copy()


# 查看有缺失值的列 
nan_lie = data1.isnull().any(axis=0)
print(nan_lie) # 无缺失值，但与csv中数据不符，可能是Null当做了字符
# 含有空值的列的数目
#data1.isnull().any(axis=0).sum()
# 以 Null、None或NULL、NONE 字符确定缺失值
nan_lie = data1.groupby(['industry_lables']).size()['Null']
print(nan_lie) # output 219
# industry_lables 缺失太多且不重要，去除该列
data1 = data1.drop(['industry_lables'], axis=1)


# 去重
data1.duplicated()
data1.drop_duplicates()	
#data1.drop_duplicates(['job_id'])

# 去除不需要的列
data1 = data1.drop(['company_shortname','job_advantagelist','work_place','finance_phase','release_time'], axis=1)
# 去除兼职和实习
print(data1.loc[:,'job_status'].value_counts()) # 实习 8 兼职 1
data1=data1[~data1['job_status'].isin(['实习','兼职'])]
data1.info()
# 分析approve 录取人数
print(data1.loc[:,'approve'].value_counts()) # 1 436; 0 5 	【 0 可能是已招满或误输，做1人处理 】
data_clean = data1.drop(['approve'],axis=1)
data_clean.info()
#data_clean.to_csv('cleandata.csv', index=True, header=True, encoding='utf_8_sig') # Chinese 'utf_8_sig'



# ================================================================================================

# 读取薪资
salary = data_clean["salary"].tolist()	
ave_salary = []
for i in range(len(salary)):			# 薪酬区间取中间值
	if (salary[i].find('-')!=-1):
		a_split = salary[i].split('-')
		a_min = int(a_split[0].strip('kK'))
		a_max = int(a_split[1].strip('kK'))
		a_ave = float((a_min+a_max)/2)
	else:
		a_ave = float(salary[i].strip('kK'))
	ave_salary.append(a_ave)
print(len(salary),len(ave_salary))
#print(np.max(ave_salary),np.min(ave_salary))	# 最大月薪 60.0 k，最小月薪 3.5 k
#print(np.mean(ave_salary))	 	# 平均薪酬18.21 k
#print(np.median(ave_salary))	# 中位薪酬17.5 k

# 薪酬分布 - 薪酬数量 - 柱状图
fig1 = plt.figure(figsize=(10,6))
ax1 = plt.subplot(111)
ax1.hist(ave_salary, bins=20, color='blue', alpha=0.6)
ran = range(0,60,5)
ax1.set_title(u'月薪分布')
plt.xlabel(u'月薪（k/月）',fontsize=20)
plt.ylabel(u'数量',fontsize=20)
plt.xticks(ran)
fig1.savefig("salary_count.jpg")
fig1.clf()



# 地域分布 - 城市数量 - 柱状图
city_count = data_clean.groupby(['city'])['job_name'].count().sort_values(ascending=False)
#print(city_count)

ax2 = plt.subplot(111)
cifig = ax2.bar(np.arange(len(city_count)), city_count.values, width=0.5)

def cityticks(barn,xticks):		# x轴城市
	x = []
	for i in barn:
		x.append(i.get_x() + i.get_width()/2)
	x = tuple(x)
	plt.xticks(x, xticks)

def numtag(barn, data=None, offset=[0,0]):		# 数据标签
	for i in barn:
		try:
			height = i.get_height()
			plt.text(i.get_x() + i.get_width()/2.4, 1.01*height, '%s' % int(height))
		except AttributeError:
			x = range(len(data))
			y = data.values
			for i in range(len(x)):
				plt.text(x[i]+offset[0], y[i]+0.05+offset[1], y[i])

cityticks(cifig, city_count.index)
ax2.set_xticklabels(city_count.index)
numtag(cifig,offset=[-1,0])

ax2.set_title(u'城市分布')
plt.xlabel(u'城市',fontsize=20)
plt.ylabel(u'数量',fontsize=20)
fig1.savefig("city_count.jpg")
fig1.clf()



# 地域分布 - 城市百分比 - 饼状图
n_job = data_clean['job_name'].count()
c_name = []
c_per = []
other = 0.0
for i in range(len(city_count)):
	if city_count.values[i] >= 5:
		c_name.append(city_count.index[i])
		c_per.append(city_count.values[i]/n_job)
	else:
		other = other + city_count.values[i]/n_job

c_name.append(u'其他')
c_per.append(other)
colors = ['dimgray', 'silver', 'tomato', 'sandybrown', 'gold', 'greenyellow', 'violet', 'deepskyblue', 'pink']

ax3 = plt.subplot(111)
piefig = ax3.pie(c_per, labels=c_name, autopct="%3.1f%%", startangle=60, colors=colors)
ax3.set_title(u'城市百分比分布')
fig1.savefig("city_percent.jpg")
fig1.clf()



# 薪酬城市分布 - 北上广深杭薪酬分布 - 折线图
def a_salary(s):
	if (s.find('-')!=-1):
		a_split = s.split('-')
		a_min = int(a_split[0].strip('kK'))
		a_max = int(a_split[1].strip('kK'))
		a_ave = float((a_min+a_max)/2)
	else:
		a_ave = float(s.strip('kK'))
	return a_ave
data_clean['avg_salary'] = data_clean['salary'].apply(a_salary)
city_salary = data_clean.groupby(['city'])['avg_salary']
get_city = city_count[0:5]		# 只取职位数前五的城市

ax4 = plt.subplot(111)
for i in range(5):
	y = []
	s = city_salary.get_group(get_city.index[i]).values
	for j in range(11):
		y.append(((s>ran[j])&(s<ran[j+1])).sum())
	ax4.plot(np.arange(2.5,55,5), y, c=colors[i], linestyle='--', marker='o', label=get_city.index[i])

ax4.set_title(u'各城市月薪分布')
plt.xlabel(u'月薪（k/月）',fontsize=20)
plt.ylabel(u'数量',fontsize=20)
plt.xticks(ran)
plt.legend(loc='upper right')
fig1.savefig("citysalary_count.jpg")
fig1.clf()

# 薪酬城市分布 - 北上广深杭薪酬分布 - 箱线图
sbox = []
for i in range(5):
	s = city_salary.get_group(get_city.index[i]).values
	sbox.append(s)

ax5 = plt.subplot(111)
ax5.boxplot(sbox)
ax5.set_title(u'各城市月薪分布')
ax5.set_xticklabels(get_city.index)
plt.ylabel(u'月薪（k/月）',fontsize=20)
fig1.savefig("citysalary_box.jpg")
fig1.clf()



# 工作经验要求分布 - 经验数量 - 柱状图
experience_count = data_clean.groupby(['job_experience'])['job_name'].count()
experience_matrix = pd.DataFrame([experience_count.index,experience_count.values]).T
experience_matrix.columns = ['exp', 'count']
experience_map = {u'应届毕业生' : 0, u'1年以下' : 1, u'1-3年' : 2, u'3-5年' : 3, u'5-10年' : 4, u'10年以上' : 5, u'不限' : 6}
experience_matrix['expnum'] = experience_matrix['exp'].map(experience_map)
experience_matrix.sort_values('expnum', inplace=True)

ax6 = plt.subplot(111)
expfig = ax6.bar(np.arange(len(experience_matrix)), experience_matrix['count'], width=0.8)
cityticks(expfig, experience_matrix['exp'])
ax1.set_xticklabels(experience_matrix['exp'])
numtag(expfig,offset=[-1,0])

ax6.set_title(u'工作经验分布')
plt.xlabel(u'经验要求',fontsize=20)
plt.ylabel(u'数量',fontsize=20)
fig1.savefig("experience_count.jpg")
fig1.clf()



# 工作经验月薪分布 - 月薪数量 - 折线图、箱线图
experience_salary = data_clean.groupby(['job_experience'])['avg_salary']
get_exp = experience_matrix['exp'].tolist()

ax7 = plt.subplot(111)
sbox = []
for i in range(6):
	y = []
	s = experience_salary.get_group(get_exp[i]).values
	sbox.append(s)
	for j in range(11):
		y.append(((s>ran[j])&(s<ran[j+1])).sum())
	ax7.plot(np.arange(2.5,55,5), y, c=colors[i], linestyle='--', marker='o', label=get_exp[i])

ax7.set_title(u'经验要求的月薪分布')
plt.xlabel(u'月薪（k/月）',fontsize=20)
plt.ylabel(u'数量',fontsize=20)
plt.xticks(ran)
plt.legend(loc='upper right')
fig1.savefig("expsalary_count.jpg")
fig1.clf()

ax8 = plt.subplot(111)
ax8.boxplot(sbox)
ax8.set_title(u'经验要求的月薪分布')
ax8.set_xticklabels(get_exp)
plt.ylabel(u'月薪（k/月）',fontsize=20)
fig1.savefig("expsalary_box.jpg")
fig1.clf()



# 学历要求分布 - 学历数量 - 柱状图、饼状图
edu_count = data_clean.groupby(['education'])['job_name'].count().sort_values(ascending=False)
edu_matrix = pd.DataFrame([edu_count.index,edu_count.values]).T
edu_matrix.columns = ['edu', 'count']
edu_map = {u'不限' : 0, u'大专' : 1, u'本科' : 2, u'硕士' : 3, u'博士' : 4}
edu_matrix['edunum'] = edu_matrix['edu'].map(edu_map)
edu_matrix.sort_values('edunum', inplace=True)

ax9 = plt.subplot(111)
edufig = ax9.bar(np.arange(len(edu_matrix)), edu_matrix['count'], width=0.8)

cityticks(edufig, edu_matrix['edu'])
ax9.set_xticklabels(edu_matrix['edu'])
numtag(edufig,offset=[-1,0])

ax9.set_title(u'学历分布')
plt.xlabel(u'学历',fontsize=20)
plt.ylabel(u'数量',fontsize=20)
fig1.savefig("edu_count.jpg")
fig1.clf()

e_name = []
e_per = []
for i in range(len(edu_count)):
	e_name.append(edu_count.index[i])
	e_per.append(edu_count.values[i]/n_job)

colors = ['blue', 'sandybrown', 'gold', 'greenyellow', 'violet', 'deepskyblue', 'pink']
ax10 = plt.subplot(111)
piefig = ax10.pie(e_per, labels=e_name, autopct="%3.1f%%", startangle=60, colors=colors)
ax10.set_title(u'学历百分比分布')
fig1.savefig("edu_percent.jpg")
fig1.clf()



# 学历月薪分布 - 月薪数量 - 折线图、箱线图
edu_salary = data_clean.groupby(['education'])['avg_salary']
get_edu = edu_matrix['edu'].tolist()

ax11 = plt.subplot(111)
sbox = []
for i in range(4):
	y = []
	s = edu_salary.get_group(get_edu[i]).values
	sbox.append(s)
	for j in range(11):
		y.append(((s>ran[j])&(s<ran[j+1])).sum())
	ax11.plot(np.arange(2.5,55,5), y, c=colors[i], linestyle='--', marker='o', label=get_edu[i])

ax11.set_title(u'学历要求的月薪分布')
plt.xlabel(u'月薪（k/月）',fontsize=20)
plt.ylabel(u'数量',fontsize=20)
plt.xticks(ran)
plt.legend(loc='upper right')
fig1.savefig("edusalary_count.jpg")
fig1.clf()

ax12 = plt.subplot(111)
ax12.boxplot(sbox)
ax12.set_title(u'学历要求的月薪分布')
ax12.set_xticklabels(get_edu)
plt.ylabel(u'月薪（k/月）',fontsize=20)
fig1.savefig("edusalary_box.jpg")
fig1.clf()



# 企业规模分布 - 企业规模数量 - 柱状图、饼状图
ComSize_count = data_clean.groupby(['company_size'])['job_name'].count().sort_values(ascending=False)
size_matrix = pd.DataFrame([ComSize_count.index,ComSize_count.values]).T
size_matrix.columns = ['size', 'count']
size_map = {u'15-50人' : 0, u'50-150人' : 1, u'150-500人' : 2, u'500-2000人' : 3, u'2000人以上' : 4}
size_matrix['sizenum'] = size_matrix['size'].map(size_map)
size_matrix.sort_values('sizenum', inplace=True)

ax13 = plt.subplot(111)
sizefig = ax13.bar(np.arange(len(size_matrix)), size_matrix['count'], width=0.5)
cityticks(sizefig, size_matrix['size'])
ax13.set_xticklabels(size_matrix['size'])
numtag(sizefig,offset=[-1,0])

ax13.set_title(u'企业规模分布')
plt.xlabel(u'企业规模',fontsize=20)
plt.ylabel(u'数量',fontsize=20)
fig1.savefig("ComSize_count.jpg")
fig1.clf()

comsize_name = []
comsize_per = []
for i in range(len(ComSize_count)):
	comsize_name.append(ComSize_count.index[i])
	comsize_per.append(ComSize_count.values[i]/n_job)

ax14 = plt.subplot(111)
piefig = ax14.pie(comsize_per, labels=comsize_name, autopct="%3.1f%%", startangle=60, colors=colors)
ax14.set_title(u'企业规模百分比分布')
fig1.savefig("ComSize_percent.jpg")
fig1.clf()



# 企业月薪分布 - 月薪数量 - 折线图、箱线图
com_salary = data_clean.groupby(['company_size'])['avg_salary']
get_com = size_matrix['size'].tolist()

ax15 = plt.subplot(111)
sbox = []
for i in range(5):
	y = []
	s = com_salary.get_group(get_com[i]).values
	sbox.append(s)
	for j in range(11):
		y.append(((s>ran[j])&(s<ran[j+1])).sum())
	ax15.plot(np.arange(2.5,55,5), y, c=colors[i], linestyle='--', marker='o', label=get_com[i])

ax15.set_title(u'不同企业规模的月薪分布')
plt.xlabel(u'月薪（k/月）',fontsize=20)
plt.ylabel(u'数量',fontsize=20)
plt.xticks(ran)
plt.legend(loc='upper right')
fig1.savefig("comsalary_count.jpg")
fig1.clf()

ax16 = plt.subplot(111)
ax16.boxplot(sbox)
ax16.set_title(u'不同企业规模的月薪分布')
ax16.set_xticklabels(get_com)
plt.ylabel(u'月薪（k/月）',fontsize=20)
fig1.savefig("comsalary_box.jpg")
fig1.clf()




# 企业规模需求 - 企业规模各经验需求比例、各学历需求比例 - 柱状图
com_exp = data_clean.groupby(['company_size'])['job_experience']

ax17 = plt.subplot(111)
y = [1.0 for i in range(5)]
m = [0 for i in range(5)]
n_comjob = size_matrix['count'].tolist()
x = np.arange(len(size_matrix)-1)

for i in range(6):
	comexp_bar=ax17.bar(x, y, color=colors[i], label=get_exp[i], width=0.5)
	cityticks(comexp_bar, size_matrix['size'])
	ax17.set_xticklabels(size_matrix['size'])
	for j in range(5):
		s = list(com_exp.get_group(get_com[j])).count(get_exp[i])
		m[j] = 100*s/n_comjob[j]
		if i>=2:
			plt.text(x[j], y[j]-0.05, '%.2f %%' % m[j], ha='center', va='bottom', fontsize=15)
		y[j] = y[j] - s/n_comjob[j]

ax17.set_title(u'不同企业规模的经验需求比例')
plt.xlabel(u'企业规模',fontsize=20)
box = ax17.get_position()
ax17.set_position([box.x0, box.y0, box.width*0.8 , box.height])
plt.legend(loc = 'center left', bbox_to_anchor=(1.0, 0.8), ncol=1)
fig1.savefig("comexp_percent.jpg")
fig1.clf()


com_edu = data_clean.groupby(['company_size'])['education']
ax18 = plt.subplot(111)
y = [1.0 for i in range(5)]
m = [0 for i in range(5)]

for i in range(4):
	comedu_bar=ax18.bar(x, y, color=colors[i], label=get_edu[i], width=0.5)
	cityticks(comedu_bar, size_matrix['size'])
	ax18.set_xticklabels(size_matrix['size'])
	for j in range(5):
		s = list(com_edu.get_group(get_com[j])).count(get_edu[i])
		m[j] = 100*s/n_comjob[j]
		if m[j]>=1.00:
			plt.text(x[j], y[j]-0.05, '%.2f %%' % m[j], ha='center', va='bottom', fontsize=15)
		y[j] = y[j] - s/n_comjob[j]

ax18.set_title(u'不同企业规模的学历需求比例')
plt.xlabel(u'企业规模',fontsize=20)
box = ax18.get_position()
ax18.set_position([box.x0, box.y0, box.width*0.8 , box.height])
plt.legend(loc = 'center left', bbox_to_anchor=(1.0, 0.8), ncol=1)
fig1.savefig("comedu_percent.jpg")
fig1.clf()




# 技能需求占比

# 提取岗位标签和描述部分，每个职位取关键词，计算出现次数
n_job = data_clean['job_id'].count()
skill = data_clean["skill_lables"].tolist()
desc = data_clean["job_description"].tolist()
skills_match = [u'sql', u'mysql', u'python', u'r', u'excel', u'office', u'ppt', u'linux', u'shell', u'hive', u'hadoop', u'bi', u'tableau', u'oracle', u'sas', u'spss', u'java', u'spark', u'matlab']
for i in range(19):
	skills_match[i] = skills_match[i].encode(encoding='utf8')  
skills_num = [0] * 19	# skill出现次数

for i in range(n_job):
	if (skill[i] != 'Null') and (skill[i] != 'null') and (skill[i] != 'None') and (skill[i] != 'none') and (skill[i] != ''):
		text = skill[i]+desc[i]
	else:
		text = desc[i]
	text = text.encode(encoding='utf8')
	text = text.lower()
	k = -1
	for j in skills_match:
		k = k + 1
		if (text.find(j)!=-1):
			skills_num[k] = skills_num[k] + 1
#print(skills_num)	#[329, 73, 225, 287, 162, 19, 68, 10, 10, 75, 53, 103, 49, 35, 111, 111, 22, 46, 20]

skill_count = pd.DataFrame({ 'skills':skills_match, 'number': skills_num})
#print(df)
skill_count = skill_count.sort_values(by='number', ascending=False)
skill_count = skill_count.reset_index(drop=True)
#print(skill_count)
for i in range(19):
	skills_match[i] = str(skill_count['skills'][i],encoding='utf8')  

fig2 = plt.figure(figsize=(15,6))
ax19 = plt.subplot(111)
skillfig = ax19.bar(np.arange(len(skill_count)), skill_count['number'], width=0.5)
cityticks(skillfig, skills_match)
ax19.set_xticklabels(skills_match)
#numtag(skillfig,offset=[-1,0])
percentage = [i*100/n_job for i in skill_count['number']]
for x, y in enumerate(skill_count['number']):
	plt.text(x, y + 5, str(round(percentage[x], 1))+'%', ha='center')

ax19.set_title(u'技能占比')
#plt.xlabel(u'技能',fontsize=20)
plt.ylabel(u'数量',fontsize=20)
fig2.savefig("skilldist.jpg")
fig2.clf()




# 城市和工作经验关系
city_exp = data_clean.groupby(['city'])['job_experience']

ax20 = plt.subplot(111)
y = [1.0 for i in range(5)]
m = [0 for i in range(5)]
n_cityjob = get_city.values.tolist()
x = np.arange(len(get_city))

for i in range(6):
	cityexp_bar=ax20.bar(x, y, color=colors[i], label=get_exp[i], width=0.6)
	cityticks(cityexp_bar, get_city.index)
	ax20.set_xticklabels(get_city.index)
	for j in range(5):
		s = list(city_exp.get_group(get_city.index[j])).count(get_exp[i])
		m[j] = 100*s/n_cityjob[j]
		if i>=2:
			plt.text(x[j], y[j]-0.05, '%.2f %%' % m[j], ha='center', va='bottom', fontsize=15)
		y[j] = y[j] - s/n_cityjob[j]

ax20.set_title(u'各城市的经验需求比例')
#plt.xlabel(u'城市',fontsize=20)
box = ax20.get_position()
ax20.set_position([box.x0, box.y0, box.width*0.8 , box.height])
plt.legend(loc = 'center left', bbox_to_anchor=(1.0, 0.8), ncol=1)
#fig1.savefig("cityexp_percent.jpg")
#fig1.clf()







