#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.db import connection

def add_indexes():
    indexes = [
        # 用户表索引
        "CREATE INDEX IF NOT EXISTS idx_user_username_role ON user_app_user (username, role)",
        
        # 课程表索引
        "CREATE INDEX IF NOT EXISTS idx_course_teacher ON user_app_course (teacher_id)",
        "CREATE INDEX IF NOT EXISTS idx_course_code ON user_app_course (code)",
        
        # 课程学生关系索引
        "CREATE INDEX IF NOT EXISTS idx_coursestudent_student ON user_app_coursestudent (student_id)",
        "CREATE INDEX IF NOT EXISTS idx_coursestudent_course ON user_app_coursestudent (course_id)",
        
        # 课堂表索引
        "CREATE INDEX IF NOT EXISTS idx_classroom_course ON user_app_classroom (course_id)",
        "CREATE INDEX IF NOT EXISTS idx_classroom_is_active ON user_app_classroom (is_active)",
        
        # 任务表索引
        "CREATE INDEX IF NOT EXISTS idx_task_course ON user_app_task (course_id)",
        "CREATE INDEX IF NOT EXISTS idx_task_classroom ON user_app_task (classroom_id)",
        "CREATE INDEX IF NOT EXISTS idx_task_create_by ON user_app_task (create_by_id)",
        
        # 答题记录表索引
        "CREATE INDEX IF NOT EXISTS idx_answerrecord_task ON user_app_answerrecord (task_id)",
        "CREATE INDEX IF NOT EXISTS idx_answerrecord_student ON user_app_answerrecord (student_id)",
        "CREATE INDEX IF NOT EXISTS idx_answerrecord_question ON user_app_answerrecord (question_id)",
        "CREATE INDEX IF NOT EXISTS idx_answerrecord_is_correct ON user_app_answerrecord (is_correct)",
        
        # 题目表索引
        "CREATE INDEX IF NOT EXISTS idx_question_create_by ON user_app_question (create_by_id)",
        "CREATE INDEX IF NOT EXISTS idx_question_course ON user_app_question (course)",
        
        # 任务得分表索引
        "CREATE INDEX IF NOT EXISTS idx_taskscore_task ON user_app_taskscore (task_id)",
        "CREATE INDEX IF NOT EXISTS idx_taskscore_student ON user_app_taskscore (student_id)",
    ]
    
    print("正在创建数据库索引...")
    
    with connection.cursor() as cursor:
        for sql in indexes:
            try:
                cursor.execute(sql)
                print("成功: " + sql[:50] + "...")
            except Exception as e:
                print("失败: " + sql[:50] + "... " + str(e))
    
    print("索引创建完成！")

if __name__ == '__main__':
    add_indexes()