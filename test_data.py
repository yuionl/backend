#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from user_app.models import User, Course, CourseStudent, Question, Task, Classroom

print("=== Database Test Report ===\n")

# 1. 检查所有用户
print("1. Users:")
users = User.objects.all()
for u in users:
    print(f"   ID:{u.id}, Username:{u.username}, Name:{u.name}, Role:{u.role}")
print(f"   Total: {users.count()}\n")

# 2. 检查所有课程
print("2. Courses:")
courses = Course.objects.all()
for c in courses:
    print(f"   ID:{c.id}, Name:{c.name}, Code:{c.code}, Teacher:{c.teacher.name if c.teacher else 'None'}")
print(f"   Total: {courses.count()}\n")

# 3. 检查课程-学生关系
print("3. Course-Student Relationships:")
course_students = CourseStudent.objects.all()
for cs in course_students:
    print(f"   CourseID:{cs.course.id}, CourseName:{cs.course.name}, StudentID:{cs.student.id}, StudentName:{cs.student.name}")
print(f"   Total: {course_students.count()}\n")

# 4. 测试教师查询课程
print("4. Testing Teacher Course Query:")
teachers = User.objects.filter(role=1)
for teacher in teachers:
    print(f"   Teacher: {teacher.name} ({teacher.username})")
    courses = Course.objects.filter(teacher=teacher)
    print(f"   Courses found: {courses.count()}")
    for c in courses:
        student_count = CourseStudent.objects.filter(course=c).count()
        print(f"     - {c.name} (students: {student_count})")
print()

# 5. 测试学生查询课程
print("5. Testing Student Course Query:")
students = User.objects.filter(role=2)
for student in students:
    print(f"   Student: {student.name} ({student.username})")
    course_students = CourseStudent.objects.filter(student=student)
    print(f"   Courses found: {course_students.count()}")
    for cs in course_students:
        print(f"     - {cs.course.name}")
print()

# 6. 检查任务关联
print("6. Task-Course Relationships:")
tasks = Task.objects.all()
for t in tasks:
    print(f"   Task:{t.title}, CourseID:{t.course_id}, CourseName:{t.course.name if t.course else 'None'}, ClassroomID:{t.classroom_id}")
print(f"   Total: {tasks.count()}\n")

# 7. 检查课堂关联
print("7. Classroom-Course Relationships:")
classrooms = Classroom.objects.all()
for c in classrooms:
    print(f"   Classroom:{c.name}, CourseID:{c.course_id}, CourseName:{c.course.name if c.course else 'None'}")
print(f"   Total: {classrooms.count()}\n")

print("=== Test Completed ===")