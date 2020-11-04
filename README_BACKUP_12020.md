# DataAnalysisSample-python
## 分析拉勾网数据分析师的需求
### 项目背景和介绍
---
#### 背景：
学习python爬虫技巧，复习python数据处理、分析、可视化，看看目前市场对数据分析人才的要求和需求
#### 简介：
了解现在求职市场上数据分析师的薪资，以及对数据分析人才的要求和需求，来分析、指导目前可以为数据分析求职做的准备，以及该岗位未来的发展。 本项目利用爬虫爬取拉勾网上数据分析这一岗位的信息，然后进行一些探索和分析。
#### 目的：
* 了解现在对数据分析师的技能、学历、工作经验的要求，及其对应的薪资；
* 分析不同地区对数据分析师的需求人数、工作经验和薪资分布；
* 不同学历的需求人数和月薪分布；
* 不同工作经验的需求人数和月薪分布；
* 不同企业规模对数据分析师的需求人数、学历、工作经验和薪资分布；
* 对数据分析师的技术和其他能力要求的占比。
#### 数据来源 （2019/04/30）：
本项目数据全部来自拉勾网，是通过python的urllib，request，BeautifulSoup等包从网页上爬取的。
样本量： 450 个招聘职位。 
【 样本不多，因此此次分析仅做参考。 】
选择拉勾网作为数据源主要是因为其岗位信息非常完整规范，极大的减少了前期数据清理和数据整理的工作量。
#### 爬取主要信息有：
								岗位名称 job_name,
								岗位类型 job_type,
								岗位标签 job_lable,
								公司简称 company_shortname,
								公司全称 company_fullname,
								所在城市 city,
								月薪     salary,
								经验要求 job_experience,
								学历要求 education,
								技能标签 skill_lables,
								需求人数 approve,
								全/兼职  job_status,
								工作地点 work_place,
								职位描述 job_description,
								职位福利 job_advantagelist,
								行业领域 industry_field,
								行业标签 industry_lables,
								公司规模 company_size,
								融资阶段 finance_phase,
								发布时间 release_time.
### 文件说明
---
<<<<<<< HEAD
	AnalyzeRecord.txt 						数据分析记录
	LagouAnalyst.pptx 						项目展示
	--------------------------------------------------------
	pythoncrawler/get_data.py 				爬虫爬取拉勾网数据
	pythoncrawler/LaGou_DataAnalyst.csv 	爬取的数据
	datapro_basic.py 						数据处理及可视化
	datapro_skill.py 						数据分析师技能的分析和可视化
	datapro_wc.py 							数据分析师技能词云
	figures/*.jpg 							图表（PPT中展示）
=======
	get_data.py 		爬虫爬取拉勾网数据
	LaGou_DataAnalyst.csv   爬取的数据
	datapro_basic.py 	数据处理及可视化
	datapro_skill.py 	数据分析师技能的分析和可视化
	datapro_wc.py 		数据分析师技能词云
	*.jpg 			图表（PPT中展示）
	AnalyzeRecord.txt 	数据分析记录
	LagouAnalyst.pptx 	项目展示


>>>>>>> e7fa1c854e37cbb1e623a4dc891a6cf9c96e4b91
