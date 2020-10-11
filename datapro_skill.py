
# First import python packages
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
import collections # 词频统计库
import wordcloud
from wordcloud import WordCloud
from PIL import Image # 图像处理库
import matplotlib.pyplot as plt # 图像展示库
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

#=======================================================================================================



# 提取月薪
def a_salary(s):		# 区间则取中间数
	if (s.find('-')!=-1):
		a_split = s.split('-')
		a_min = int(a_split[0].strip('kK'))
		a_max = int(a_split[1].strip('kK'))
		a_ave = float((a_min+a_max)/2)
	else:
		a_ave = float(s.strip('kK'))
	return a_ave
data_clean['avg_salary'] = data_clean['salary'].apply(a_salary)
salary = data_clean["avg_salary"].tolist()



# 技能和工作经验、月薪关系
import seaborn as sns

# 提取岗位标签和描述部分，每个职位取关键词，计算出现次数，及月薪中位数
n_job = data_clean['job_id'].count()
skill = data_clean["skill_lables"].tolist()
desc = data_clean["job_description"].tolist()
skills_match = [u'sql', u'mysql', u'python', u'r', u'excel', u'office', u'ppt', u'linux', u'shell', u'hive', u'hadoop', u'bi', u'tableau', u'oracle', u'sas', u'spss', u'java', u'spark', u'matlab']
for i in range(19):
	skills_match[i] = skills_match[i].encode(encoding='utf8')  
skills_num = [0] * 19	# skill出现次数
skills_salary = [[0] for i in range(19)]	# 对应月薪
skills_medsalary = [0] * 19		# 对应中位数月薪

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
			skills_salary[k].append(salary[i])
#print(skills_num)	#[329, 73, 225, 287, 162, 19, 68, 10, 10, 75, 53, 103, 49, 35, 111, 111, 22, 46, 20]
#print(skills_salary)
# 每种技术对应的中位数月薪
for i in range(19):
	skills_medsalary[i] = np.median(skills_salary[i])
#print(skills_medsalary)

skill_count = pd.DataFrame({ 'skills':skills_match, 'number':skills_num, 'salary':skills_medsalary})
skill_count = skill_count.sort_values(by='number', ascending=False)
skill_count = skill_count.reset_index(drop=True)
#print(skill_count)
for i in range(19):
	skills_match[i] = str(skill_count['skills'][i],encoding='utf8')  
skills_match = skills_match[0:15]	# 保留前十五个最多的技术


# 画气泡图
sns.set(style = "whitegrid")#设置样式

x = np.arange(len(skills_match))	#X轴数据
y = skill_count['salary'][0:15]		#Y轴数据
z = skill_count['number'][0:15]		#用来调整各个点的大小s
#print(x,y,z)
cm = plt.cm.get_cmap('RdYlBu')
fig,ax = plt.subplots(figsize = (15,6))
#s是点的大小 = 当前点的数值*10
bubble = ax.scatter(x, y , s = z * 10, c = z, cmap = cm, linewidth = 0.8, alpha = 0.5)
ax.grid()
fig.colorbar(bubble)
plt.xticks(x, skills_match)
ax.set_xticklabels(skills_match)
ax.set_title(u'技能占比和月薪影响分布')
plt.ylabel(u'中位月薪',fontsize=20)
fig.savefig("skillsalary_bubble.jpg")
fig.clf()

