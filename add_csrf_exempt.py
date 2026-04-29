import re

filepath = r'e:\PyChram\backend\user_app\views.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import at the top
if 'from django.views.decorators.csrf import csrf_exempt' not in content:
    content = 'from django.views.decorators.csrf import csrf_exempt\n' + content

# Add @csrf_exempt before all API view functions (not helper functions like calculate_task_scores)
functions_to_decorate = [
    'def register(', 'def login(', 'def create_question(', 'def get_question_list(',
    'def delete_questions(', 'def get_question_detail(', 'def update_question(',
    'def create_course(', 'def get_teacher_courses(', 'def get_course_students(',
    'def get_course_statistics(', 'def get_classroom_history_stats(',
    'def get_classroom_overview(', 'def get_question_analysis(', 'def get_student_rank(',
    'def get_classroom_rank(', 'def get_course_total_rank(',
    'def get_teacher_student_profile(', 'def get_student_analysis(',
    'def remove_course_student(', 'def join_course(', 'def get_student_courses(',
    'def exit_course(', 'def create_task(', 'def get_teacher_tasks(',
    'def get_student_tasks(', 'def get_student_task_status(', 'def get_task_questions(',
    'def submit_answer(', 'def task_statistics(', 'def get_essay_answers(',
    'def grade_essay(', 'def get_student_answered_tasks(', 'def get_student_task_detail(',
    'def upload_image(', 'def create_classroom(', 'def get_active_classroom(',
    'def end_classroom(', 'def get_classroom_detail(', 'def get_classroom_history(',
    'def create_task_in_classroom(', 'def get_student_classroom(',
    'def get_student_performance('
]

for func in functions_to_decorate:
    # Only add if not already decorated and not the index function
    if func != 'def index(' and f'@csrf_exempt\n{func}' not in content:
        content = content.replace(func, '@csrf_exempt\n' + func)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done! Added @csrf_exempt to all API views.')