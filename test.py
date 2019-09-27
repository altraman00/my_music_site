# -*- coding: utf-8 -*-
'''
Created by admin at 2019-07-11  
desc:
'''

import pymysql
import requests
import json

base_url = 'http://el-fec.supplus.cn'
# base_url = 'http://el-fec.ministudy.com'
exam_id = '36b0c6876bff36cc016bff9eafe40118'
chapterExamId = '36b0c6876c174a39016c17d1644a00c6'
chanceId = '4014ca826a5456db016a61dd53335b19'
plan_id = '1'


# 请求头
header = {}
header['Authorization'] = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOnsiaWQiOiI0MDE0Y2E4MjZhODVlYzlkMDE2YWFmNThmMGI0NDUyMCIsInRva2VuIjpudWxsLCJuYW1lIjoi6YOR5paMIiwidXNlcm5hbWUiOiJ6aGVuZ2JpbjA0Iiwicm9sZUxpc3QiOm51bGwsImVtcGxveWVlTmFtZSI6IumDkeaWjCIsImVtcGxveWVlSWQiOiIxMTI3MTUiLCJvcmdJZCI6MjEwMTcxNywicGhvbmUiOiIxNzYwMDMwNzI1NSIsInNzb1Rva2VuIjpudWxsfSwiY3JlYXRlZCI6MTU2Mzc2NzA5NDUyMiwiZXhwIjoxNTY0MzcxODk0fQ.qA2cWuizbYv9oh_n6L-QlZB9uf0RiZieaXyNCwzU8LtlbqdUTdRnRwsaQ68zsje2n1EqeKs6He0QeHJoDzIQvg'
header['Content-Type'] = 'application/json;charset=UTF-8'
header['Token-Type'] = 'bearer'

# 连接mysql数据库
conn = pymysql.connect(
    host='gz-cdb-f0ena0pp.sql.tencentcdb.com',
    port=62473,
    user='elearning_prod',
    password='feo@2020',
    database='test_db_feo_elearning_1_7_0',
    charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

'''考试'''
# # 查询考试答案
# sql = "select id, id as questionId, answer_correct as answer from bi_user_plan_exam_log_question where plan_exam_log_id='%s'" % exam_id
# cursor.execute(sql)
# ans = cursor.fetchall()
#
# # 拼接请求参数
# params = {}
# params['examId'] = exam_id
# params['chanceId'] = chanceId
# params['userAnswerVOS'] = ans[:-2]
# params = json.dumps(params)
#
# # 新人训考试
# # url = base_url + '/mapi/api/plan/exam_entry/commit'
# # 非新人训考试
# url = base_url + '/v1/api/plan/exam/answers'
# res = requests.post(url, data=params, headers=header)
# print(json.loads(res.content))


'''做练习'''
# 获取练习题
url1 = base_url + '/mapi/api/course/chapter/exam_questions'
res1 = requests.get(url1, params={'chapterExamId': chapterExamId}, headers=header)
data = json.loads(res1.content)['data']

# 提交练习答案answer
url2 = base_url + '/mapi/api/course/chapter/exam/answer'
for line in data:
    params = {}
    params['answerUser'] = line['answerCorrect']
    params['id'] = line['id']
    params = json.dumps(params)
    res = requests.post(url2, data=params, headers=header)
    print(json.loads(res.content))

# 提交完确认commit
url3 = base_url + '/mapi/api/course/chapter/exam/commit'
requests.get(url3, params={'chapterExamId': chapterExamId}, headers=header)



# '''抽题规则校验'''
# # 查询属于大本科的课程id
# sql1 = "select course_id from bi_def_course_table_mapping where table_name='大本科' and deleted=0 ORDER BY sort_no"
# # # 查询其他专题下的课程id
# # sql1 = "select course_id from bi_def_train_plan_course where plan_id=%s and deleted=0"%plan_id
# cursor.execute(sql1)
# course_list = [course['course_id'] for course in cursor.fetchall()]
#
# # 查询本次考试抽题的题目id
# sql2 = "select question_id from bi_user_plan_exam_log_question where plan_exam_log_id='%s'"%exam_id
# cursor.execute(sql2)
# question_list = cursor.fetchall()
# flag = True
# for question in question_list:
#     # 根据题目ID查询其所属的课程是否在大本科课程列表内
#     sql3 = "select course_id from bi_def_plan_question where id = %s" % question['question_id']
#     cursor.execute(sql3)
#     course = cursor.fetchone()
#     if course['course_id'] not in course_list:
#         flag = False
#         sql4 = "select course_name from bi_def_course where id = '%s'" % course['course_id']
#         cursor.execute(sql4)
#         res = cursor.fetchone()
#         res['course_id'] = course['course_id']
#         res['question_id'] = question['question_id']
#         print(res)
# print(flag)

# 关闭数据库连接
cursor.close()
conn.close()
