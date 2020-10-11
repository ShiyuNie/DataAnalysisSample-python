
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
data = pd.read_csv("LaGou_DataAnalyst.csv",encoding='utf-8')
print(data.dtypes.value_counts()) # 查看每列数据类型
print(data.shape)  # 查看数据的行列大小
#data.info()
#print(data.head(30))  # 查看前30行


# 备份data1
data1 = data.copy()

# 查看缺失值 
nan_all = data1.isnull()
#print(nan_all)
nan_lie = data1.isnull().any()
nanall_lie = data1.isnull().all()
#print(nan_lie,nanall_lie)

# 去重
data1.duplicated()
data1.drop_duplicates()	
data1.drop_duplicates(["job_id"])

# 数据列改为list
data1_num = data1.select_dtypes(include=['float64', 'int64'])
approve = data1["approve"].tolist()
job_id = data1["job_id"].tolist()
#print(approve,job_id)

# 去除不需要的列
data2 = data1.drop(['Unnamed: 0','approve','job_id','company_shortname','work_place'], axis=1)
data2.info()


#data2.to_csv('cleandata1.csv', index=True, header=True, encoding='utf_8_sig') # Chinese 'utf_8_sig'


# 提取岗位标签和描述部分，每个职位取前20个关键词，存入txt文件
n_job = data2['job_name'].count()
skill = data2["skill_lables"].tolist()
desc = data2["job_description"].tolist()
jieba.load_userdict('mydict.txt')
jieba.suggest_freq('office',False)
f = open('skilltags.txt','a')

for i in range(n_job):
	if (skill[i] != 'Null') and (skill[i] != 'null') and (skill[i] != 'None') and (skill[i] != 'none') and (skill[i] != ''):
		text = skill[i]+desc[i]
	else:
		text = desc[i]
	text = text.encode(encoding='utf8')
	words = jieba.analyse.extract_tags(text, topK=20, withWeight=False, allowPOS=())
	for j in words:
		f.writelines(j + u',')

f.close()





# 提取高频词汇
fo = open('skilltags.txt','r')
get_words = fo.read()
fo.close()
mydict = open('mydict.txt','r',encoding='utf8').read()

skill_list = []
other_list = []
get_words = get_words.split(u",")
mydict = mydict.split('\n')
remove_words = mydict + [u'数据',u'分析', u'数据分析', u'熟悉', u'熟练', u'优先', u'工作', u'岗位职责', u'以上学历', u'相关', u'能力', u'具备', u'良好', u'优秀'] # 自定义去除词库
# mydict中的词存入skill列表，并去除‘去除词库’里的词后，其余存入other列表
for word in get_words: 
	if word.lower() in [i.lower() for i in mydict]:
		skill_list.append(word.lower())
	if word.lower() not in [i.lower() for i in remove_words]: 
		other_list.append(word.lower()) 

# 词频统计
skill_counts = collections.Counter(skill_list)
other_counts = collections.Counter(other_list) # 对分词做词频统计
#word_counts_top10 = word_counts.most_common(10) # 获取前10最高频的词
print (skill_counts) # 输出检查

# skill词频展示
fig1 = plt.figure(figsize=(10,6))
#mask = np.array(Image.open('wordcloud.jpg')) # 定义词频背景
wc1 = WordCloud(
	width=800, height=400, background_color='white',
    font_path='C:/Windows/Fonts/simhei.ttf', # 设置字体格式
    #mask=mask, # 设置背景图
    max_words=30, # 最多显示词数
    max_font_size=400 # 字体最大值
)
wc1.generate_from_frequencies(skill_counts) # 从skill字典生成词云
#image_colors = wordcloud.ImageColorGenerator(mask) # 从背景图建立颜色方案
#wc.recolor(color_func=image_colors) # 将词云颜色设置为背景图方案
plt.imshow(wc1) # 显示词云
plt.axis('off') 
#plt.show() 
fig1.savefig("skills_wc.jpg")
fig1.clf()



# other词频展示
fig2 = plt.figure(figsize=(10,6))
#mask = np.array(Image.open('wordcloud.jpg')) # 定义词频背景
wc2 = WordCloud(
	width=800, height=400, background_color='white',
    font_path='C:/Windows/Fonts/simhei.ttf', # 设置字体格式
    #mask=mask, # 设置背景图
    max_words=80, # 最多显示词数
    max_font_size=200 # 字体最大值
)
wc2.generate_from_frequencies(other_counts) # 从skill字典生成词云
#image_colors = wordcloud.ImageColorGenerator(mask) # 从背景图建立颜色方案
#wc.recolor(color_func=image_colors) # 将词云颜色设置为背景图方案
plt.imshow(wc2) # 显示词云
plt.axis('off') 
#plt.show() 
fig2.savefig("others_wc.jpg")
fig2.clf()


