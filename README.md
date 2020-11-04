#DataAnalysisSample-python
##分析拉勾网数据分析师的需求
===
###项目背景和介绍
---
####背景：
学习python爬虫技巧，复习python数据处理、分析、可视化，看看目前市场对数据分析人才的要求和需求
####简介：
了解现在求职市场上数据分析师的薪资，以及对数据分析人才的要求和需求，来分析、指导目前可以为数据分析求职做的准备，以及该岗位未来的发展。 本项目利用爬虫爬取拉勾网上数据分析这一岗位的信息，然后进行一些探索和分析。
####目的：
了解现在对数据分析师的技能、学历、工作经验的要求，及其对应的薪资；\<br>
分析不同地区对数据分析师的需求人数、工作经验和薪资分布；\<br>
不同学历的需求人数和月薪分布；\<br>
不同工作经验的需求人数和月薪分布；\<br>
不同企业规模对数据分析师的需求人数、学历、工作经验和薪资分布；\<br>
以及对数据分析师的技术和其他能力要求的占比。
####数据来源 （2019/04/30）：
本项目数据全部来自拉勾网，是通过python的urllib，request，BeautifulSoup等包从网页上爬取的。\<br>
样本量： 450 个招聘职位。 
*** 【 样本不多，因此此次分析仅做参考。 】\<br>
选择拉勾网作为数据源主要是因为其岗位信息非常完整规范，极大的减少了前期数据清理和数据整理的工作量。
####爬取主要信息有：
								岗位名称 job_name,\<br>
								岗位类型 job_type,\<br>
								岗位标签 job_lables,\<br>
								公司简称 company_shortname,\<br>
								公司全称 company_fullname,\<br>
								所在城市 city,\<br>
								月薪     salary,\<br>
								经验要求 job_experience,\<br>
								学历要求 education,\<br>
								技能标签 skill_lables,\<br>
								需求人数 approve,\<br>
								全/兼职  job_status,\<br>
								工作地点 work_place,\<br>
								职位描述 job_description,\<br>
								职位福利 job_advantagelist,\<br>
								行业领域 industry_field,\<br>
								行业标签 industry_lables,\<br>
								公司规模 company_size,\<br>
								融资阶段 finance_phase,\<br>
								发布时间 release_time\<br>


