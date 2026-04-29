import json
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt
from .models import User, Question, Task, AnswerRecord, Course, CourseStudent, Classroom, TaskScore


def get_request_data(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            if body:
                return json.loads(body)
        except:
            pass
        return request.POST
    return request.GET


def index(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>课堂互动系统</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                font-size: 100px;
            }
        </style>
    </head>
    <body>
        你好
    </body>
    </html>
    """
    from django.http import HttpResponse
    return HttpResponse(html_content)


@csrf_exempt
def register(request):
    data = get_request_data(request)
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role')

    if User.objects.filter(username=username).exists():
        return JsonResponse({'code': 0, 'msg': '用户名已存在'})

    User.objects.create(
        username=username,
        password=password,
        name=name,
        role=role
    )
    return JsonResponse({'code': 1, 'msg': '注册成功'})


@csrf_exempt
def login(request):
    data = get_request_data(request)
    username = data.get('username')
    password = data.get('password')

    return JsonResponse({
        'received': {'username': username, 'password': password},
        'body': request.body.decode('utf-8') if request.body else 'EMPTY',
        'method': request.method
    })


@csrf_exempt
def create_question(request):
    title = request.GET.get('title', '').strip()
    q_type = request.GET.get('q_type', '').strip()
    level = request.GET.get('level', '').strip()
    course = request.GET.get('course', '').strip()
    options = request.GET.get('options', '').strip()
    answer = request.GET.get('answer', '').strip()
    create_by = request.GET.get('username', '').strip()

    if not q_type:
        q_type = request.GET.get('type', '').strip()

    missing_fields = []
    if not title: missing_fields.append('题干')
    if not q_type: missing_fields.append('题型')
    if not level: missing_fields.append('难度')
    if not course: missing_fields.append('课程')
    if not answer: missing_fields.append('答案')
    if not create_by: missing_fields.append('创建人')

    if missing_fields:
        return JsonResponse({'code': 0, 'msg': f'请填写所有必填项：{",".join(missing_fields)}'})

    try:
        q_type = int(q_type)
        level = int(level)
        teacher = User.objects.get(username=create_by, role=1)
        Question.objects.create(
            title=title,
            q_type=q_type,
            level=level,
            course=course,
            options=options,
            answer=answer,
            create_by=teacher
        )
        return JsonResponse({'code': 1, 'msg': '题目创建成功'})
    except ValueError:
        return JsonResponse({'code': 0, 'msg': '题型/难度必须是数字'})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '创建人不是教师或不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': f'创建失败：{str(e)}'})


@csrf_exempt
def get_question_list(request):
    username = request.GET.get('username')
    course = request.GET.get('course', '')
    level = request.GET.get('level', '')
    q_type = request.GET.get('q_type', '')

    try:
        teacher = User.objects.get(username=username, role=1)
        questions = Question.objects.filter(create_by=teacher)

        total = questions.count()

        if course:
            questions = questions.filter(course__icontains=course)
        if level:
            questions = questions.filter(level=int(level))
        if q_type:
            questions = questions.filter(q_type=int(q_type))

        questions = questions.values(
            'id', 'title', 'q_type', 'level', 'course', 'options', 'answer'
        )
        type_map = {1: '单选题', 2: '多选题', 3: '判断题', 4: '填空题', 5: '简答题'}
        level_map = {1: '简单', 2: '中等', 3: '困难'}
        question_list = []
        for q in questions:
            q_type_val = q['q_type']
            level_val = q['level']
            if isinstance(q_type_val, str):
                try:
                    q_type_val = int(q_type_val)
                except:
                    q_type_val = None
            if isinstance(level_val, str):
                try:
                    level_val = int(level_val)
                except:
                    level_val = None
            q['q_type'] = type_map.get(q_type_val, '未知题型')
            q['level'] = level_map.get(level_val, '未知难度')
            question_list.append(q)
        return JsonResponse({'code': 1, 'data': question_list, 'total': total})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '教师不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': f'获取题库失败：{str(e)}'})


@csrf_exempt
def delete_questions(request):
    username = request.GET.get('username')
    q_ids_str = request.GET.get('q_ids')

    if not username or not q_ids_str:
        return JsonResponse({'code': 0, 'msg': '参数缺失'})

    try:
        teacher = User.objects.get(username=username, role=1)
        q_ids = [int(qid) for qid in q_ids_str.split(',') if qid.strip().isdigit()]
        Question.objects.filter(id__in=q_ids, create_by=teacher).delete()
        return JsonResponse({'code': 1, 'msg': '删除成功'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': f'删除失败：{str(e)}'})


@csrf_exempt
def get_question_detail(request):
    question_id = request.GET.get('question_id')
    if not question_id:
        return JsonResponse({'code': 0, 'msg': '缺少题目ID'})
    
    try:
        question = Question.objects.get(id=question_id)
        return JsonResponse({
            'code': 1,
            'data': {
                'id': question.id,
                'title': question.title,
                'q_type': question.q_type,
                'level': question.level,
                'course': question.course,
                'options': question.options or '',
                'answer': question.answer
            }
        })
    except Question.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '题目不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def update_question(request):
    question_id = request.GET.get('question_id')
    title = request.GET.get('title', '').strip()
    q_type = request.GET.get('q_type', '').strip()
    level = request.GET.get('level', '').strip()
    course = request.GET.get('course', '').strip()
    options = request.GET.get('options', '').strip()
    answer = request.GET.get('answer', '').strip()

    if not question_id:
        return JsonResponse({'code': 0, 'msg': '缺少题目ID'})
    
    if not title or not answer:
        return JsonResponse({'code': 0, 'msg': '题干和答案不能为空'})

    try:
        question = Question.objects.get(id=question_id)
        question.title = title
        if q_type:
            question.q_type = int(q_type)
        if level:
            question.level = int(level)
        question.course = course
        question.options = options
        question.answer = answer
        question.save()
        return JsonResponse({'code': 1, 'msg': '修改成功'})
    except Question.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '题目不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def create_course(request):
    name = request.GET.get('name', '').strip()
    semester = request.GET.get('semester', '').strip()
    description = request.GET.get('description', '').strip()
    username = request.GET.get('username', '').strip()

    if not name or not semester or not username:
        return JsonResponse({'code': 0, 'msg': '请填写课程名称和学期'})

    try:
        teacher = User.objects.get(username=username, role=1)
        course = Course.objects.create(
            name=name,
            semester=semester,
            description=description,
            teacher=teacher
        )
        return JsonResponse({
            'code': 1,
            'msg': '课程创建成功',
            'course_id': course.id,
            'course_code': course.code
        })
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '教师不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': f'创建失败：{str(e)}'})


@csrf_exempt
def get_teacher_courses(request):
    username = request.GET.get('username')
    try:
        teacher = User.objects.get(username=username, role=1)
        courses = Course.objects.filter(teacher=teacher).order_by('-create_time')
        result = []
        for c in courses:
            student_count = CourseStudent.objects.filter(course=c).count()
            task_count = Task.objects.filter(course=c).count()
            result.append({
                'id': c.id,
                'name': c.name,
                'code': c.code,
                'semester': c.semester,
                'description': c.description or '',
                'student_count': student_count,
                'task_count': task_count,
                'create_time': c.create_time.astimezone().strftime('%Y-%m-%d %H:%M') if c.create_time else ''
            })
        return JsonResponse({'code': 1, 'data': result})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '教师不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_course_students(request):
    course_id = request.GET.get('course_id')
    if not course_id:
        return JsonResponse({'code': 0, 'msg': '缺少课程ID'})

    try:
        course = Course.objects.get(id=course_id)
        students = CourseStudent.objects.filter(course=course).select_related('student')
        result = []
        for cs in students:
            # 转换为本地时间
            local_time = cs.join_time.astimezone()
            result.append({
                'id': cs.student.id,
                'username': cs.student.username,
                'name': cs.student.name,
                'join_time': local_time.strftime('%Y-%m-%d %H:%M')
            })
        return JsonResponse({'code': 1, 'data': result, 'course_name': course.name})
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_course_statistics(request):
    course_id = request.GET.get('course_id')
    if not course_id:
        return JsonResponse({'code': 0, 'msg': '缺少课程ID'})
    
    try:
        course = Course.objects.get(id=course_id)
        classrooms = Classroom.objects.filter(course=course).order_by('create_time')
        
        classroom_stats = []
        total_tasks = 0
        total_accuracy = 0
        classroom_count = 0
        
        for c in classrooms:
            tasks = Task.objects.filter(classroom=c)
            task_ids = list(tasks.values_list('id', flat=True))
            total_tasks += tasks.count()
            
            records = AnswerRecord.objects.filter(task_id__in=task_ids)
            total = records.count()
            correct = records.filter(is_correct=True).count()
            accuracy = round(correct / total * 100) if total > 0 else 0
            
            # 无论是否有答题记录，都添加课堂统计数据
            classroom_stats.append({
                'id': c.id,
                'name': c.name,
                'accuracy': accuracy
            })
            if total > 0:
                total_accuracy += accuracy
                classroom_count += 1
        
        avg_accuracy = round(total_accuracy / classroom_count) if classroom_count > 0 else 0
        
        return JsonResponse({
            'code': 1,
            'course_name': course.name,
            'semester': course.semester,
            'total_classrooms': classrooms.count(),
            'total_tasks': total_tasks,
            'avg_accuracy': avg_accuracy,
            'classroom_stats': classroom_stats
        })
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_classroom_history_stats(request):
    course_id = request.GET.get('course_id')
    if not course_id:
        return JsonResponse({'code': 0, 'msg': '缺少课程ID'})
    
    try:
        course = Course.objects.get(id=course_id)
        classrooms = Classroom.objects.filter(course=course, is_active=False).order_by('-end_time')
        
        result = []
        for c in classrooms:
            tasks = Task.objects.filter(classroom=c)
            task_ids = list(tasks.values_list('id', flat=True))
            
            records = AnswerRecord.objects.filter(task_id__in=task_ids)
            student_ids = records.values_list('student_id', flat=True).distinct()
            participation = student_ids.count()
            
            total = records.count()
            correct = records.filter(is_correct=True).count()
            accuracy = round(correct / total * 100) if total > 0 else 0
            
            course_students = CourseStudent.objects.filter(course=course).count()
            participation_rate = round(participation / course_students * 100) if course_students > 0 else 0
            
            result.append({
                'id': c.id,
                'name': c.name,
                'time': c.end_time.astimezone().strftime('%Y-%m-%d %H:%M') if c.end_time else c.create_time.astimezone().strftime('%Y-%m-%d %H:%M'),
                'task_count': tasks.count(),
                'participation': participation_rate,
                'accuracy': accuracy
            })
        
        return JsonResponse({
            'code': 1,
            'course_name': course.name,
            'classrooms': result
        })
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_classroom_overview(request):
    classroom_id = request.GET.get('classroom_id')
    if not classroom_id:
        return JsonResponse({'code': 0, 'msg': '缺少课堂ID'})
    
    try:
        classroom = Classroom.objects.get(id=classroom_id)
        tasks = Task.objects.filter(classroom=classroom)
        task_ids = list(tasks.values_list('id', flat=True))
        
        records = AnswerRecord.objects.filter(task_id__in=task_ids)
        student_ids = records.values_list('student_id', flat=True).distinct()
        participant_count = student_ids.count()
        
        total = records.count()
        correct = records.filter(is_correct=True).count()
        avg_score = round(correct / total * 100) if total > 0 else 0
        
        course_students = CourseStudent.objects.filter(course=classroom.course).count()
        participation = round(participant_count / course_students * 100) if course_students > 0 else 0
        
        task_list = []
        for t in tasks:
            t_records = AnswerRecord.objects.filter(task=t)
            t_total = t_records.count()
            t_correct = t_records.filter(is_correct=True).count()
            t_accuracy = round(t_correct / t_total * 100) if t_total > 0 else 0
            
            t_student_ids = t_records.values_list('student_id', flat=True).distinct()
            t_participation = round(t_student_ids.count() / course_students * 100) if course_students > 0 else 0
            
            task_list.append({
                'id': t.id,
                'title': t.title,
                'participation': t_participation,
                'accuracy': t_accuracy
            })
        
        return JsonResponse({
            'code': 1,
            'classroom_name': classroom.name,
            'classroom_time': classroom.create_time.astimezone().strftime('%Y-%m-%d %H:%M'),
            'overview': {
                'taskCount': tasks.count(),
                'participantCount': participant_count,
                'avgScore': avg_score,
                'participation': participation
            },
            'tasks': task_list
        })
    except Classroom.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课堂不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_question_analysis(request):
    classroom_id = request.GET.get('classroom_id')
    if not classroom_id:
        return JsonResponse({'code': 0, 'msg': '缺少课堂ID'})
    
    try:
        classroom = Classroom.objects.get(id=classroom_id)
        # 获取课程的学生总数（应参与人数）
        total_students = CourseStudent.objects.filter(course=classroom.course).count()
        tasks = Task.objects.filter(classroom=classroom)
        
        task_questions = []
        for t in tasks:
            questions = t.questions.all()
            question_list = []
            for q in questions:
                records = AnswerRecord.objects.filter(task=t, question=q)
                answered_count = records.count()
                correct_count = records.filter(is_correct=True).count()
                # 计算未参与人数
                not_participated = total_students - answered_count
                # 正确率基于已参与人数
                accuracy = round(correct_count / answered_count * 100) if answered_count > 0 else 0
                
                question_list.append({
                    'questionId': q.id,
                    'title': q.title,
                    'q_type': q.q_type,
                    'correctAnswer': q.answer,
                    'totalStudents': total_students,  # 应参与人数
                    'answeredCount': answered_count,  # 实际参与人数
                    'notParticipated': not_participated,  # 未参与人数
                    'correctCount': correct_count,
                    'accuracy': accuracy
                })
            
            if question_list:
                task_questions.append({
                    'taskId': t.id,
                    'taskTitle': t.title,
                    'questions': question_list
                })
        
        return JsonResponse({
            'code': 1,
            'classroom_name': classroom.name,
            'task_questions': task_questions
        })
    except Classroom.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课堂不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_student_rank(request):
    classroom_id = request.GET.get('classroom_id')
    if not classroom_id:
        return JsonResponse({'code': 0, 'msg': '缺少课堂ID'})
    
    try:
        classroom = Classroom.objects.get(id=classroom_id)
        tasks = Task.objects.filter(classroom=classroom)
        task_ids = list(tasks.values_list('id', flat=True))
        
        records = AnswerRecord.objects.filter(task_id__in=task_ids)
        
        student_stats = {}
        for r in records:
            sid = r.student_id
            if sid not in student_stats:
                student_stats[sid] = {
                    'studentId': sid,
                    'studentName': r.student.name,
                    'answeredCount': 0,
                    'correctCount': 0
                }
            student_stats[sid]['answeredCount'] += 1
            if r.is_correct:
                student_stats[sid]['correctCount'] += 1
        
        students = []
        for sid, stats in student_stats.items():
            accuracy = round(stats['correctCount'] / stats['answeredCount'] * 100) if stats['answeredCount'] > 0 else 0
            students.append({
                'studentId': sid,
                'studentName': stats['studentName'],
                'answeredCount': stats['answeredCount'],
                'correctCount': stats['correctCount'],
                'accuracy': accuracy
            })
        
        students.sort(key=lambda x: x['accuracy'], reverse=True)
        
        participant_count = len(students)
        total_correct = sum(s['correctCount'] for s in students)
        total_answered = sum(s['answeredCount'] for s in students)
        avg_accuracy = round(total_correct / total_answered * 100) if total_answered > 0 else 0
        
        return JsonResponse({
            'code': 1,
            'classroom_name': classroom.name,
            'participant_count': participant_count,
            'avg_accuracy': avg_accuracy,
            'students': students
        })
    except Classroom.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课堂不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


def calculate_task_scores(task_id):
    task = Task.objects.get(id=task_id)
    questions = task.questions.all()
    answer_records = AnswerRecord.objects.filter(task=task)

    for question in questions:
        question_answers = answer_records.filter(question=question)
        total_answers = question_answers.count()
        if total_answers == 0:
            continue

        correct_answers = question_answers.filter(is_correct=True).count()
        if correct_answers == 0:
            continue

        accuracy = correct_answers / total_answers
        score_per_question = round((1 - accuracy) * 10)

        for record in question_answers.filter(is_correct=True):
            TaskScore.objects.update_or_create(
                task=task,
                student=record.student,
                defaults={'score': score_per_question}
            )


@csrf_exempt
def get_classroom_rank(request):
    classroom_id = request.GET.get('classroom_id')
    if not classroom_id:
        return JsonResponse({'code': 0, 'msg': '缺少课堂ID'})

    try:
        classroom = Classroom.objects.get(id=classroom_id)
        tasks = Task.objects.filter(classroom=classroom, status=2)
        task_ids = list(tasks.values_list('id', flat=True))

        if not task_ids:
            return JsonResponse({
                'code': 1,
                'classroom_name': classroom.name,
                'students': []
            })

        for task_id in task_ids:
            calculate_task_scores(task_id)

        scores = TaskScore.objects.filter(task_id__in=task_ids)
        student_scores = {}
        for s in scores:
            sid = s.student_id
            if sid not in student_scores:
                student_scores[sid] = {
                    'studentId': sid,
                    'studentName': s.student.name,
                    'totalScore': 0,
                    'taskCount': 0
                }
            student_scores[sid]['totalScore'] += s.score
            student_scores[sid]['taskCount'] += 1

        students = []
        for sid, stats in student_scores.items():
            students.append({
                'studentId': sid,
                'studentName': stats['studentName'],
                'totalScore': stats['totalScore'],
                'taskCount': stats['taskCount'],
                'avgScore': round(stats['totalScore'] / stats['taskCount'], 1) if stats['taskCount'] > 0 else 0
            })

        students.sort(key=lambda x: x['totalScore'], reverse=True)

        return JsonResponse({
            'code': 1,
            'classroom_name': classroom.name,
            'students': students
        })
    except Classroom.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课堂不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_course_total_rank(request):
    course_id = request.GET.get('course_id')
    if not course_id:
        return JsonResponse({'code': 0, 'msg': '缺少课程ID'})

    try:
        course = Course.objects.get(id=course_id)
        classrooms = Classroom.objects.filter(course=course)
        classroom_ids = list(classrooms.values_list('id', flat=True))
        tasks = Task.objects.filter(classroom_id__in=classroom_ids, status=2)
        task_ids = list(tasks.values_list('id', flat=True))

        if not task_ids:
            return JsonResponse({
                'code': 1,
                'course_name': course.name,
                'students': []
            })

        for task_id in task_ids:
            calculate_task_scores(task_id)

        scores = TaskScore.objects.filter(task_id__in=task_ids)
        student_scores = {}
        for s in scores:
            sid = s.student_id
            if sid not in student_scores:
                student_scores[sid] = {
                    'studentId': sid,
                    'studentName': s.student.name,
                    'totalScore': 0,
                    'taskCount': 0
                }
            student_scores[sid]['totalScore'] += s.score
            student_scores[sid]['taskCount'] += 1

        students = []
        for sid, stats in student_scores.items():
            students.append({
                'studentId': sid,
                'studentName': stats['studentName'],
                'totalScore': stats['totalScore'],
                'taskCount': stats['taskCount'],
                'avgScore': round(stats['totalScore'] / stats['taskCount'], 1) if stats['taskCount'] > 0 else 0
            })

        students.sort(key=lambda x: x['totalScore'], reverse=True)

        return JsonResponse({
            'code': 1,
            'course_name': course.name,
            'students': students
        })
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_teacher_student_profile(request):
    username = request.GET.get('username')
    course_id = request.GET.get('course_id')
    
    if not username or not course_id:
        return JsonResponse({'code': 0, 'msg': '缺少参数'})
    
    try:
        student = User.objects.get(username=username, role=2)
        course = Course.objects.get(id=course_id)
        
        classrooms = Classroom.objects.filter(course=course)
        classroom_ids = list(classrooms.values_list('id', flat=True))
        tasks = Task.objects.filter(classroom_id__in=classroom_ids)
        task_ids = list(tasks.values_list('id', flat=True))
        
        records = AnswerRecord.objects.filter(student=student, task_id__in=task_ids)
        
        total_questions = records.count()
        correct_count = records.filter(is_correct=True).count()
        accuracy = round(correct_count / total_questions * 100) if total_questions > 0 else 0
        
        task_records = {}
        for r in records:
            if r.task_id not in task_records:
                task_records[r.task_id] = {
                    'correct': 0,
                    'total': 0,
                    'task': r.task,
                    'classroom': r.task.classroom
                }
            task_records[r.task_id]['total'] += 1
            if r.is_correct:
                task_records[r.task_id]['correct'] += 1
        
        classroom_records = {}
        for tid, data in task_records.items():
            cid = data['classroom'].id if data['classroom'] else None
            if cid and cid not in classroom_records:
                classroom_records[cid] = {
                    'classroomId': cid,
                    'classroomName': data['classroom'].name if data['classroom'] else '未知课堂',
                    'time': data['classroom'].create_time.astimezone().strftime('%Y-%m-%d %H:%M') if data['classroom'] else '',
                    'answeredCount': 0,
                    'correctCount': 0
                }
            if cid:
                classroom_records[cid]['answeredCount'] += data['total']
                classroom_records[cid]['correctCount'] += data['correct']
        
        record_list = []
        for cid, data in classroom_records.items():
            accuracy = round(data['correctCount'] / data['answeredCount'] * 100) if data['answeredCount'] > 0 else 0
            record_list.append({
                'classroomId': cid,
                'classroomName': data['classroomName'],
                'time': data['time'],
                'answeredCount': data['answeredCount'],
                'correctCount': data['correctCount'],
                'accuracy': accuracy
            })
        
        record_list.sort(key=lambda x: x['time'], reverse=True)
        
        return JsonResponse({
            'code': 1,
            'student_name': student.name,
            'course_name': course.name,
            'stats': {
                'totalTasks': len(task_records),
                'totalQuestions': total_questions,
                'correctCount': correct_count,
                'accuracy': accuracy
            },
            'records': record_list
        })
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '学生不存在'})
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_student_analysis(request):
    username = request.GET.get('username')
    
    if not username:
        return JsonResponse({'code': 0, 'msg': '缺少参数'})
    
    try:
        student = User.objects.get(username=username, role=2)
        
        course_students = CourseStudent.objects.filter(student=student)
        course_ids = list(course_students.values_list('course_id', flat=True))
        
        courses = Course.objects.filter(id__in=course_ids)
        total_courses = courses.count()
        
        classrooms = Classroom.objects.filter(course_id__in=course_ids)
        total_classrooms = classrooms.count()
        
        tasks = Task.objects.filter(course_id__in=course_ids)
        task_ids = list(tasks.values_list('id', flat=True))
        
        records = AnswerRecord.objects.filter(student=student, task_id__in=task_ids)
        total_questions = records.count()
        correct_count = records.filter(is_correct=True).count()
        accuracy = round(correct_count / total_questions * 100) if total_questions > 0 else 0
        
        course_stats = []
        for cs in course_students:
            course = cs.course
            course_tasks = Task.objects.filter(course=course)
            course_task_ids = list(course_tasks.values_list('id', flat=True))
            course_records = records.filter(task_id__in=course_task_ids)
            course_total = course_records.count()
            course_correct = course_records.filter(is_correct=True).count()
            course_accuracy = round(course_correct / course_total * 100) if course_total > 0 else 0
            course_stats.append({
                'course_id': course.id,
                'course_name': course.name,
                'teacher_name': course.teacher.name if course.teacher else '未知',
                'total_questions': course_total,
                'accuracy': course_accuracy
            })
        course_stats.sort(key=lambda x: x['total_questions'], reverse=True)
        
        classroom_records = {}
        for r in records:
            task = r.task
            if task and task.classroom:
                cid = task.classroom.id
                if cid not in classroom_records:
                    classroom_records[cid] = {
                        'classroom': task.classroom,
                        'correct': 0,
                        'total': 0
                    }
                classroom_records[cid]['total'] += 1
                if r.is_correct:
                    classroom_records[cid]['correct'] += 1
        
        trend = []
        sorted_classrooms = sorted(classroom_records.values(), key=lambda x: x['classroom'].create_time, reverse=True)[:5]
        for cr in reversed(sorted_classrooms):
            cr_accuracy = round(cr['correct'] / cr['total'] * 100) if cr['total'] > 0 else 0
            trend.append({
                'label': cr['classroom'].name[:4] if len(cr['classroom'].name) > 4 else cr['classroom'].name,
                'accuracy': cr_accuracy
            })
        
        task_records = {}
        for r in records:
            if r.task_id not in task_records:
                task_records[r.task_id] = {
                    'task': r.task,
                    'correct': 0,
                    'total': 0
                }
            task_records[r.task_id]['total'] += 1
            if r.is_correct:
                task_records[r.task_id]['correct'] += 1
        
        recent_records = []
        sorted_tasks = sorted(task_records.values(), key=lambda x: x['task'].create_time, reverse=True)[:10]
        for tr in sorted_tasks:
            score = round(tr['correct'] / tr['total'] * 100) if tr['total'] > 0 else 0
            recent_records.append({
                'id': tr['task'].id,
                'task_title': tr['task'].title,
                'course_name': tr['task'].course.name if tr['task'].course else '未知',
                'create_time': tr['task'].create_time.astimezone().strftime('%m-%d %H:%M'),
                'score': score
            })
        
        return JsonResponse({
            'code': 1,
            'stats': {
                'totalCourses': total_courses,
                'totalClassrooms': total_classrooms,
                'totalQuestions': total_questions,
                'accuracy': accuracy
            },
            'trend': trend,
            'courseStats': course_stats,
            'recentRecords': recent_records
        })
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '学生不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def remove_course_student(request):
    course_id = request.GET.get('course_id')
    student_id = request.GET.get('student_id')
    if not course_id or not student_id:
        return JsonResponse({'code': 0, 'msg': '缺少参数'})

    try:
        CourseStudent.objects.filter(course_id=course_id, student_id=student_id).delete()
        return JsonResponse({'code': 1, 'msg': '移除成功'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def join_course(request):
    code = request.GET.get('code', '').strip().upper()
    username = request.GET.get('username', '').strip()

    if not code or not username:
        return JsonResponse({'code': 0, 'msg': '请输入课程码'})

    try:
        student = User.objects.get(username=username, role=2)
        course = Course.objects.get(code=code)

        if CourseStudent.objects.filter(course=course, student=student).exists():
            return JsonResponse({'code': 0, 'msg': '您已加入该课程'})

        CourseStudent.objects.create(course=course, student=student)
        return JsonResponse({
            'code': 1,
            'msg': '加入成功',
            'course_name': course.name,
            'teacher_name': course.teacher.name
        })
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '学生不存在'})
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程码无效'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_student_courses(request):
    username = request.GET.get('username')
    try:
        student = User.objects.get(username=username, role=2)
        course_students = CourseStudent.objects.filter(student=student).select_related('course', 'course__teacher')
        result = []
        for cs in course_students:
            course = cs.course
            task_count = Task.objects.filter(course=course).count()
            result.append({
                'id': course.id,
                'name': course.name,
                'code': course.code,
                'semester': course.semester,
                'teacher_name': course.teacher.name,
                'task_count': task_count,
                'join_time': cs.join_time.astimezone().strftime('%Y-%m-%d %H:%M')
            })
        return JsonResponse({'code': 1, 'data': result})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '学生不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def exit_course(request):
    course_id = request.GET.get('course_id')
    username = request.GET.get('username')

    if not course_id or not username:
        return JsonResponse({'code': 0, 'msg': '缺少参数'})

    try:
        student = User.objects.get(username=username, role=2)
        CourseStudent.objects.filter(course_id=course_id, student=student).delete()
        return JsonResponse({'code': 1, 'msg': '退出成功'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def create_task(request):
    title = request.GET.get('title')
    description = request.GET.get('desc')
    username = request.GET.get('username')
    course_id = request.GET.get('course_id')
    question_ids = request.GET.get('question_ids')
    duration = request.GET.get('duration', 10)

    if not (title and username and question_ids and course_id):
        return JsonResponse({'code': 0, 'msg': '任务名称、课程、题目不能为空'})

    try:
        teacher = User.objects.get(username=username, role=1)
        course = Course.objects.get(id=course_id, teacher=teacher)
        end_time = timezone.now() + timezone.timedelta(minutes=int(duration))
        task = Task.objects.create(
            title=title,
            description=description,
            course=course,
            create_by=teacher,
            duration=duration,
            end_time=end_time,
            status=1
        )
        for qid in question_ids.split(','):
            task.questions.add(int(qid))
        return JsonResponse({'code': 1, 'msg': '发布成功'})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '教师不存在'})
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在或无权限'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_teacher_tasks(request):
    username = request.GET.get('username')
    course_id = request.GET.get('course_id', '')

    try:
        teacher = User.objects.get(username=username, role=1)
        tasks = Task.objects.filter(create_by=teacher)
        if course_id:
            tasks = tasks.filter(course_id=course_id)

        for t in tasks:
            if t.end_time and t.end_time < timezone.now() and t.status == 1:
                t.status = 2
                t.save()

        data = []
        for t in tasks:
            status_text = '已结束' if t.status == 2 else '进行中'
            create_time_str = t.create_time.astimezone().strftime('%Y-%m-%d %H:%M') if t.create_time else '无'
            data.append({
                'id': t.id,
                'title': t.title,
                'course_name': t.course.name,
                'status': status_text,
                'create_time': create_time_str
            })
        return JsonResponse({'code': 1, 'data': data})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '教师不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_student_tasks(request):
    username = request.GET.get('username')
    course_id = request.GET.get('course_id', '')

    try:
        student = User.objects.get(username=username, role=2)

        if course_id:
            course_student = CourseStudent.objects.filter(student=student, course_id=course_id).first()
            if not course_student:
                return JsonResponse({'code': 0, 'msg': '未加入该课程'})
            tasks = Task.objects.filter(course_id=course_id, status=1, end_time__gt=timezone.now())
        else:
            course_ids = CourseStudent.objects.filter(student=student).values_list('course_id', flat=True)
            tasks = Task.objects.filter(course_id__in=course_ids, status=1, end_time__gt=timezone.now())

        data = []
        for t in tasks:
            answered_count = AnswerRecord.objects.filter(task=t, student=student).count()
            total_questions = t.questions.count()
            is_completed = answered_count >= total_questions and total_questions > 0
            remaining_seconds = 0
            if t.end_time:
                delta = t.end_time - timezone.now()
                remaining_seconds = max(0, int(delta.total_seconds()))
            data.append({
                'id': t.id,
                'title': t.title,
                'course_name': t.course.name,
                'description': t.description,
                'is_completed': is_completed,
                'answered_count': answered_count,
                'total_questions': total_questions,
                'remaining_seconds': remaining_seconds,
                'end_time': t.end_time.astimezone().strftime('%Y-%m-%d %H:%M:%S') if t.end_time else ''
            })
        return JsonResponse({'code': 1, 'data': data})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '学生不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_student_task_status(request):
    username = request.GET.get('username')
    task_ids_str = request.GET.get('task_ids', '')
    
    if not task_ids_str:
        return JsonResponse({'code': 1, 'data': []})
    
    try:
        student = User.objects.get(username=username, role=2)
        task_ids = [int(tid) for tid in task_ids_str.split(',') if tid.strip()]
        
        data = []
        for task_id in task_ids:
            task = Task.objects.filter(id=task_id).first()
            if task:
                answered_count = AnswerRecord.objects.filter(task=task, student=student).count()
                total_questions = task.questions.count()
                is_completed = answered_count >= total_questions and total_questions > 0
                data.append({
                    'task_id': task_id,
                    'is_completed': is_completed,
                    'answered_count': answered_count,
                    'total_questions': total_questions
                })
        
        return JsonResponse({'code': 1, 'data': data})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '学生不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_task_questions(request):
    task_id = request.GET.get('task_id')
    if not task_id or not task_id.isdigit():
        return JsonResponse({'code': 0, 'msg': '任务ID无效'})
    try:
        task = Task.objects.get(id=int(task_id))
        questions = task.questions.all().values(
            'id', 'title', 'q_type', 'level', 'course', 'options', 'answer'
        )
        type_map = {1: '单选题', 2: '多选题', 3: '判断题', 4: '填空题', 5: '简答题'}
        question_list = []
        for q in questions:
            q['q_type'] = type_map.get(int(q['q_type']), '未知题型')
            question_list.append(q)
        remaining_seconds = 0
        if task.end_time:
            delta = task.end_time - timezone.now()
            remaining_seconds = max(0, int(delta.total_seconds()))
        return JsonResponse({
            'code': 1,
            'data': question_list,
            'remaining_seconds': remaining_seconds,
            'end_time': task.end_time.astimezone().strftime('%Y-%m-%d %H:%M:%S') if task.end_time else ''
        })
    except Task.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '任务不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': f'获取题目失败：{str(e)}'})


@csrf_exempt
def submit_answer(request):
    task_id = request.GET.get('task_id')
    q_id = request.GET.get('q_id')
    username = request.GET.get('username')
    student_answer = request.GET.get('answer')

    if not task_id or not task_id.isdigit() or not q_id or not q_id.isdigit():
        return JsonResponse({'code': 0, 'msg': '任务ID或题目ID无效'})
    if not username or not student_answer:
        return JsonResponse({'code': 0, 'msg': '用户名或答案不能为空'})

    try:
        student = User.objects.get(username=username, role=2)
        task = Task.objects.get(id=int(task_id))
        question = Question.objects.get(id=int(q_id))

        if question.q_type == 5:
            is_correct = None
        else:
            is_correct = student_answer.strip() == question.answer.strip()

        AnswerRecord.objects.create(
            task=task,
            student=student,
            question=question,
            student_answer=student_answer,
            is_correct=is_correct
        )

        return JsonResponse({
            'code': 1,
            'msg': '答题提交成功',
            'is_correct': is_correct,
            'is_essay': question.q_type == 5
        })
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '学生不存在'})
    except Task.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '任务不存在'})
    except Question.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '题目不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': f'提交失败：{str(e)}'})


@csrf_exempt
def task_statistics(request):
    task_id = request.GET.get('task_id')
    try:
        task = Task.objects.get(id=task_id)
        # 获取课程的学生总数（应参与人数）
        total_students = CourseStudent.objects.filter(course=task.course).count()
        questions = task.questions.filter(q_type__in=[1,3])
        result = []
        for q in questions:
            records = AnswerRecord.objects.filter(task=task, question=q)
            total = records.count()
            correct = records.filter(is_correct=True).count()
            # 计算未参与人数
            not_participated = total_students - total
            opts = {}
            for opt in ['A','B','C','D']:
                cnt = records.filter(student_answer=opt).count()
                if cnt>0: opts[opt] = cnt
            result.append({
                'title': q.title,
                'q_type': int(q.q_type),
                'answer': q.answer,
                'total': total,
                'totalStudents': total_students,  # 应参与人数
                'notParticipated': not_participated,  # 未参与人数
                'correct': correct,
                'options': opts
            })
        return JsonResponse({'code':1, 'data':result})
    except:
        return JsonResponse({'code':0, 'msg':'错误'})


@csrf_exempt
def get_essay_answers(request):
    task_id = request.GET.get('task_id')
    if not task_id:
        return JsonResponse({'code': 0, 'msg': '缺少任务ID'})
    try:
        task = Task.objects.get(id=task_id)
        essay_questions = task.questions.filter(q_type=5)
        result = []
        for q in essay_questions:
            records = AnswerRecord.objects.filter(task=task, question=q, is_correct__isnull=True)
            for r in records:
                result.append({
                    'record_id': r.id,
                    'question_id': q.id,
                    'question_title': q.title,
                    'reference_answer': q.answer,
                    'student_name': r.student.username,
                    'student_answer': r.student_answer
                })
        return JsonResponse({'code': 1, 'data': result, 'total': len(result)})
    except Task.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '任务不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def grade_essay(request):
    record_id = request.GET.get('record_id')
    is_correct = request.GET.get('is_correct')
    if not record_id or not is_correct:
        return JsonResponse({'code': 0, 'msg': '缺少参数'})
    try:
        record = AnswerRecord.objects.get(id=record_id)
        record.is_correct = is_correct == 'true' or is_correct == '1'
        record.save()
        return JsonResponse({'code': 1, 'msg': '批改成功'})
    except AnswerRecord.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '答题记录不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_student_answered_tasks(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'code': 0, 'msg': '缺少用户名'})
    try:
        student = User.objects.get(username=username, role=2)
        records = AnswerRecord.objects.filter(student=student).values_list('task_id', flat=True)
        task_ids = list(set(records))
        tasks = Task.objects.filter(id__in=task_ids).order_by('-create_time')
        result = []
        for task in tasks:
            task_records = AnswerRecord.objects.filter(task=task, student=student)
            total_questions = task.questions.count()
            answered_count = task_records.count()
            correct_count = task_records.filter(is_correct=True).count()
            pending_count = task_records.filter(is_correct__isnull=True).count()
            result.append({
                'task_id': task.id,
                'title': task.title,
                'course_name': task.course.name,
                'description': task.description or '',
                'create_time': task.create_time.astimezone().strftime('%Y-%m-%d %H:%M') if task.create_time else '',
                'total_questions': total_questions,
                'answered_count': answered_count,
                'correct_count': correct_count,
                'pending_count': pending_count
            })
        return JsonResponse({'code': 1, 'data': result})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '学生不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_student_task_detail(request):
    username = request.GET.get('username')
    task_id = request.GET.get('task_id')
    if not username or not task_id:
        return JsonResponse({'code': 0, 'msg': '缺少参数'})
    try:
        student = User.objects.get(username=username, role=2)
        task = Task.objects.get(id=task_id)
        questions = task.questions.all()
        records = AnswerRecord.objects.filter(task=task, student=student)
        record_map = {r.question_id: r for r in records}
        type_map = {1: '单选题', 2: '多选题', 3: '判断题', 4: '填空题', 5: '简答题'}
        result = []
        for q in questions:
            record = record_map.get(q.id)
            result.append({
                'question_id': q.id,
                'title': q.title,
                'q_type': type_map.get(int(q.q_type), '未知题型'),
                'options': q.options or '',
                'correct_answer': q.answer,
                'student_answer': record.student_answer if record else '未作答',
                'is_correct': record.is_correct if record else None,
                'is_answered': record is not None
            })
        return JsonResponse({'code': 1, 'data': result, 'task_title': task.title})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '学生不存在'})
    except Task.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '任务不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


import os
import uuid
from django.core.files.storage import default_storage

@csrf_exempt
def upload_image(request):
    if request.method != 'POST':
        return JsonResponse({'code': 0, 'msg': '仅支持POST请求'})
    
    if 'image' not in request.FILES:
        return JsonResponse({'code': 0, 'msg': '未上传图片'})
    
    image = request.FILES['image']
    
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if image.content_type not in allowed_types:
        return JsonResponse({'code': 0, 'msg': '不支持的图片格式'})
    
    if image.size > 5 * 1024 * 1024:
        return JsonResponse({'code': 0, 'msg': '图片大小不能超过5MB'})
    
    ext = os.path.splitext(image.name)[1]
    filename = f'question_images/{uuid.uuid4().hex}{ext}'
    
    saved_path = default_storage.save(filename, image)
    url = f'http://127.0.0.1:8000/media/{saved_path}'
    
    return JsonResponse({'code': 1, 'msg': '上传成功', 'url': url})


@csrf_exempt
def create_classroom(request):
    course_id = request.GET.get('course_id')
    name = request.GET.get('name', '').strip()
    username = request.GET.get('username')
    
    if not course_id or not username:
        return JsonResponse({'code': 0, 'msg': '缺少参数'})
    
    try:
        teacher = User.objects.get(username=username, role=1)
        course = Course.objects.get(id=course_id, teacher=teacher)
        
        active_classroom = Classroom.objects.filter(course=course, is_active=True).first()
        if active_classroom:
            return JsonResponse({'code': 0, 'msg': '该课程已有进行中的课堂，请先结束当前课堂'})
        
        if not name:
            name = f'第{Classroom.objects.filter(course=course).count() + 1}节课'
        
        classroom = Classroom.objects.create(
            course=course,
            name=name,
            is_active=True
        )
        return JsonResponse({
            'code': 1,
            'msg': '课堂创建成功',
            'classroom_id': classroom.id,
            'classroom_name': classroom.name
        })
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '教师不存在'})
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在或无权限'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_active_classroom(request):
    course_id = request.GET.get('course_id')
    if not course_id:
        return JsonResponse({'code': 0, 'msg': '缺少课程ID'})
    
    try:
        course = Course.objects.get(id=course_id)
        classroom = Classroom.objects.filter(course=course, is_active=True).first()
        
        if classroom:
            task_count = Task.objects.filter(classroom=classroom).count()
            return JsonResponse({
                'code': 1,
                'has_active': True,
                'classroom': {
                    'id': classroom.id,
                    'name': classroom.name,
                    'create_time': classroom.create_time.astimezone().strftime('%Y-%m-%d %H:%M'),
                    'task_count': task_count
                }
            })
        else:
            return JsonResponse({'code': 1, 'has_active': False, 'classroom': None})
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def end_classroom(request):
    classroom_id = request.GET.get('classroom_id')
    username = request.GET.get('username')
    
    if not classroom_id or not username:
        return JsonResponse({'code': 0, 'msg': '缺少参数'})
    
    try:
        teacher = User.objects.get(username=username, role=1)
        classroom = Classroom.objects.get(id=classroom_id)
        
        if classroom.course.teacher != teacher:
            return JsonResponse({'code': 0, 'msg': '无权限操作此课堂'})
        
        classroom.is_active = False
        classroom.end_time = timezone.now()
        classroom.save()
        
        Task.objects.filter(classroom=classroom, status=1).update(status=2, end_time=timezone.now())
        
        return JsonResponse({'code': 1, 'msg': '课堂已结束'})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '教师不存在'})
    except Classroom.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课堂不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_classroom_detail(request):
    classroom_id = request.GET.get('classroom_id')
    if not classroom_id:
        return JsonResponse({'code': 0, 'msg': '缺少课堂ID'})
    
    try:
        classroom = Classroom.objects.get(id=classroom_id)
        tasks = Task.objects.filter(classroom=classroom).order_by('-create_time')
        
        task_list = []
        for t in tasks:
            if t.end_time and timezone.now() > t.end_time:
                status_text = '已结束'
            else:
                status_text = '进行中'
            remaining_seconds = 0
            if t.end_time:
                delta = t.end_time - timezone.now()
                remaining_seconds = max(0, int(delta.total_seconds()))
            has_essay = t.questions.filter(q_type=5).exists()
            task_list.append({
                'id': t.id,
                'title': t.title,
                'status': status_text,
                'create_time': t.create_time.astimezone().strftime('%Y-%m-%d %H:%M'),
                'question_count': t.questions.count(),
                'has_essay': has_essay,
                'remaining_seconds': remaining_seconds
            })
        
        return JsonResponse({
            'code': 1,
            'classroom': {
                'id': classroom.id,
                'name': classroom.name,
                'is_active': classroom.is_active,
                'create_time': classroom.create_time.astimezone().strftime('%Y-%m-%d %H:%M'),
                'end_time': classroom.end_time.astimezone().strftime('%Y-%m-%d %H:%M') if classroom.end_time else '',
                'course_name': classroom.course.name
            },
            'tasks': task_list
        })
    except Classroom.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课堂不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_classroom_history(request):
    course_id = request.GET.get('course_id')
    if not course_id:
        return JsonResponse({'code': 0, 'msg': '缺少课程ID'})
    
    try:
        course = Course.objects.get(id=course_id)
        classrooms = Classroom.objects.filter(course=course, is_active=False).order_by('-end_time')
        
        result = []
        for c in classrooms:
            task_count = Task.objects.filter(classroom=c).count()
            result.append({
                'id': c.id,
                'name': c.name,
                'create_time': c.create_time.astimezone().strftime('%Y-%m-%d %H:%M'),
                'end_time': c.end_time.astimezone().strftime('%Y-%m-%d %H:%M') if c.end_time else '',
                'task_count': task_count
            })
        
        return JsonResponse({'code': 1, 'data': result})
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def create_task_in_classroom(request):
    title = request.GET.get('title')
    description = request.GET.get('desc')
    username = request.GET.get('username')
    classroom_id = request.GET.get('classroom_id')
    question_ids = request.GET.get('question_ids')
    duration = request.GET.get('duration', 10)

    if not (title and username and question_ids and classroom_id):
        return JsonResponse({'code': 0, 'msg': '任务名称、课堂、题目不能为空'})

    try:
        teacher = User.objects.get(username=username, role=1)
        classroom = Classroom.objects.get(id=classroom_id)
        
        if classroom.course.teacher != teacher:
            return JsonResponse({'code': 0, 'msg': '无权限在此课堂发布任务'})
        
        if not classroom.is_active:
            return JsonResponse({'code': 0, 'msg': '课堂已结束，无法发布任务'})
        
        end_time = timezone.now() + timezone.timedelta(minutes=int(duration))
        task = Task.objects.create(
            title=title,
            description=description,
            course=classroom.course,
            classroom=classroom,
            create_by=teacher,
            duration=duration,
            end_time=end_time,
            status=1
        )
        for qid in question_ids.split(','):
            task.questions.add(int(qid))
        return JsonResponse({'code': 1, 'msg': '发布成功'})
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '教师不存在'})
    except Classroom.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课堂不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_student_classroom(request):
    course_id = request.GET.get('course_id')
    if not course_id:
        return JsonResponse({'code': 0, 'msg': '缺少课程ID'})
    
    try:
        course = Course.objects.get(id=course_id)
        classroom = Classroom.objects.filter(course=course, is_active=True).first()
        
        if classroom:
            tasks = Task.objects.filter(classroom=classroom, status=1, end_time__gt=timezone.now())
            task_list = []
            for t in tasks:
                task_list.append({
                    'id': t.id,
                    'title': t.title,
                    'end_time': t.end_time.astimezone().strftime('%Y-%m-%d %H:%M:%S') if t.end_time else ''
                })
            return JsonResponse({
                'code': 1,
                'has_active': True,
                'classroom': {
                    'id': classroom.id,
                    'name': classroom.name,
                    'tasks': task_list
                }
            })
        else:
            return JsonResponse({'code': 1, 'has_active': False, 'classroom': None})
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})


@csrf_exempt
def get_student_performance(request):
    username = request.GET.get('username')
    course_id = request.GET.get('course_id')
    
    if not username or not course_id:
        return JsonResponse({'code': 0, 'msg': '缺少参数'})
    
    try:
        student = User.objects.get(username=username, role=2)
        course = Course.objects.get(id=course_id)
        
        tasks = Task.objects.filter(course=course)
        task_ids = list(tasks.values_list('id', flat=True))
        
        records = AnswerRecord.objects.filter(student=student, task_id__in=task_ids)
        
        total_questions = records.count()
        correct_count = records.filter(is_correct=True).count()
        
        task_records = {}
        for r in records:
            if r.task_id not in task_records:
                task_records[r.task_id] = {'correct': 0, 'total': 0, 'task': r.task}
            task_records[r.task_id]['total'] += 1
            if r.is_correct:
                task_records[r.task_id]['correct'] += 1
        
        record_list = []
        for tid, data in task_records.items():
            score = round(data['correct'] / data['total'] * 100) if data['total'] > 0 else 0
            record_list.append({
                'id': tid,
                'task_title': data['task'].title,
                'create_time': data['task'].create_time.astimezone().strftime('%Y-%m-%d %H:%M'),
                'score': score
            })
        
        record_list.sort(key=lambda x: x['create_time'], reverse=True)
        
        accuracy = round(correct_count / total_questions * 100) if total_questions > 0 else 0
        
        return JsonResponse({
            'code': 1,
            'course_name': course.name,
            'stats': {
                'totalTasks': len(task_records),
                'accuracy': accuracy,
                'totalQuestions': total_questions
            },
            'records': record_list
        })
    except User.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '学生不存在'})
    except Course.DoesNotExist:
        return JsonResponse({'code': 0, 'msg': '课程不存在'})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': str(e)})
