from django.core.management.base import BaseCommand
from user_app.models import AnswerRecord, Task, Classroom, CourseStudent, Question, Course, User

class Command(BaseCommand):
    help = 'Clear all data from the database'

    def handle(self, *args, **options):
        # 按照依赖关系的相反顺序删除数据
        # 1. 答题记录
        self.stdout.write('Clearing AnswerRecord...')
        AnswerRecord.objects.all().delete()
        self.stdout.write('✓ AnswerRecord cleared')

        # 2. 任务 (需要先删除 ManyToMany 关系)
        self.stdout.write('Clearing Task...')
        tasks = Task.objects.all()
        for task in tasks:
            task.questions.clear()
        tasks.delete()
        self.stdout.write('✓ Task cleared')

        # 3. 课堂
        self.stdout.write('Clearing Classroom...')
        Classroom.objects.all().delete()
        self.stdout.write('✓ Classroom cleared')

        # 4. 课程学生关系
        self.stdout.write('Clearing CourseStudent...')
        CourseStudent.objects.all().delete()
        self.stdout.write('✓ CourseStudent cleared')

        # 5. 题目
        self.stdout.write('Clearing Question...')
        Question.objects.all().delete()
        self.stdout.write('✓ Question cleared')

        # 6. 课程
        self.stdout.write('Clearing Course...')
        Course.objects.all().delete()
        self.stdout.write('✓ Course cleared')

        # 7. 用户
        self.stdout.write('Clearing User...')
        User.objects.all().delete()
        self.stdout.write('✓ User cleared')

        self.stdout.write('\n✅ All data has been cleared successfully!')
