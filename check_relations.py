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

    log("=== 数据关系完整性检查 ===")
    log("")

    # 1. 检查课程与教师的关系
    log("1. 检查课程与教师的关系:")
    courses = Course.objects.all()
    for c in courses:
        teacher_valid = c.teacher is not None and User.objects.filter(id=c.teacher_id).exists()
        log(f"   Course '{c.name}' (ID:{c.id}) -> Teacher ID:{c.teacher_id} -> {'存在' if teacher_valid else '不存在!'}")
    log("")

    # 2. 检查课堂与课程的关系
    log("2. 检查课堂与课程的关系:")
    classrooms = Classroom.objects.all()
    for c in classrooms:
        course_valid = Course.objects.filter(id=c.course_id).exists()
        log(f"   Classroom '{c.name}' (ID:{c.id}) -> Course ID:{c.course_id} -> {'存在' if course_valid else '不存在!'}")
    log("")

    # 3. 检查任务与课程的关系
    log("3. 检查任务与课程的关系:")
    tasks = Task.objects.all()
    for t in tasks:
        course_valid = Course.objects.filter(id=t.course_id).exists()
        teacher_valid = User.objects.filter(id=t.create_by_id).exists() if t.create_by_id else True
        log(f"   Task '{t.title}' (ID:{t.id}) -> Course ID:{t.course_id} {'存在' if course_valid else '不存在!'}, Teacher ID:{t.create_by_id} {'存在' if teacher_valid else '不存在!'}")
    log("")

    # 4. 检查课程学生关系
    log("4. 检查课程学生关系:")
    course_students = CourseStudent.objects.all()
    for cs in course_students:
        course_valid = Course.objects.filter(id=cs.course_id).exists()
        student_valid = User.objects.filter(id=cs.student_id).exists()
        log(f"   CourseStudent (ID:{cs.id}) -> Course ID:{cs.course_id} {'存在' if course_valid else '不存在!'}, Student ID:{cs.student_id} {'存在' if student_valid else '不存在!'}")
    log("")

    # 5. 检查题目与教师的关系
    log("5. 检查题目与教师的关系:")
    questions = Question.objects.all()
    for q in questions:
        teacher_valid = User.objects.filter(id=q.create_by_id).exists()
        log(f"   Question '{q.title[:30]}' (ID:{q.id}) -> Teacher ID:{q.create_by_id} -> {'存在' if teacher_valid else '不存在!'}")
    log("")

    log("=== 检查完成 ===")

except Exception as e:
    import traceback
    log(f"Error: {e}")
    log(traceback.format_exc())

# Write to file
with open('relation_check_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("检查完成，结果已写入 relation_check_result.txt")