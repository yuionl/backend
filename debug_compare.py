#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

output_lines = []

def log(msg):
    output_lines.append(str(msg))

try:
    import django
    django.setup()

    from user_app.models import User, Course, CourseStudent, Question, Task, Classroom, AnswerRecord
    from django.conf import settings

    log("=== 数据库诊断报告 ===")
    log("")
    log(f"数据库引擎: {settings.DATABASES['default']['ENGINE']}")
    log(f"数据库名称: {settings.DATABASES['default'].get('NAME', 'unknown')}")
    log("")

    # 统计数据
    log("--- 数据统计 ---")
    log(f"用户总数: {User.objects.count()}")
    log(f"  教师: {User.objects.filter(role=1).count()}")
    log(f"  学生: {User.objects.filter(role=2).count()}")
    log(f"课程总数: {Course.objects.count()}")
    log(f"课堂总数: {Classroom.objects.count()}")
    log(f"任务总数: {Task.objects.count()}")
    log(f"题目总数: {Question.objects.count()}")
    log(f"课程学生关系: {CourseStudent.objects.count()}")
    log(f"答题记录: {AnswerRecord.objects.count()}")
    log("")

    # 检查序列问题
    log("--- 序列检查 ---")
    from django.db import connection
    tables = ['user_app_user', 'user_app_course', 'user_app_classroom', 'user_app_coursestudent']
    for table in tables:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT COALESCE(MAX(id), 0) FROM {table}")
                max_id = cursor.fetchone()[0]
                cursor.execute(f"SELECT pg_get_serial_sequence('{table}', 'id')")
                seq_result = cursor.fetchone()[0]
                if seq_result:
                    cursor.execute(f"SELECT last_value FROM {seq_result}")
                    last_val = cursor.fetchone()[0]
                    log(f"{table}: 最大ID={max_id}, 序列值={last_val}")
                else:
                    log(f"{table}: 无序列")
        except Exception as e:
            log(f"{table}: 检查失败 - {e}")
    log("")

    # 检查第一个用户（教师）的课程
    log("--- 教师 'a001' 的课程 ---")
    try:
        teacher = User.objects.get(username='a001', role=1)
        courses = Course.objects.filter(teacher=teacher)
        log(f"教师 a001 的课程数: {courses.count()}")
        for c in courses:
            student_count = CourseStudent.objects.filter(course=c).count()
            log(f"  - {c.name} (ID:{c.id}, 学生数:{student_count})")
    except User.DoesNotExist:
        log("教师 a001 不存在!")
    log("")

    # 检查第一个学生
    log("--- 学生课程检查 ---")
    students = User.objects.filter(role=2)[:3]
    for student in students:
        course_count = CourseStudent.objects.filter(student=student).count()
        log(f"学生 {student.username}: 选修课程数={course_count}")

    log("")
    log("=== 诊断完成 ===")

except Exception as e:
    import traceback
    log(f"Error: {e}")
    log(traceback.format_exc())

# Write to file
with open('debug_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("诊断完成，结果已写入 debug_report.txt")