from django.db import models
import random
import string

class User(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    role = models.IntegerField(default=2, verbose_name='角色：1教师 2学生')
    name = models.CharField(max_length=50, verbose_name='姓名')

    def __str__(self):
        return self.username

class Question(models.Model):
    title = models.CharField(max_length=500, verbose_name='题目内容')
    q_type = models.IntegerField(verbose_name='题型：1单选 2多选 3判断 4填空 5简答')
    level = models.IntegerField(default=1, verbose_name='难度：1简单 2中等 3困难')
    course = models.CharField(max_length=50, verbose_name='科目')
    options = models.TextField(blank=True, null=True, verbose_name='选项（A.xx,B.xx）')
    answer = models.CharField(max_length=200, verbose_name='正确答案')
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建教师')

    def __str__(self):
        return self.title

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='课程名称')
    code = models.CharField(max_length=6, unique=True, verbose_name='课程码')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaching_courses', verbose_name='授课教师')
    semester = models.CharField(max_length=50, verbose_name='学期')
    description = models.TextField(blank=True, null=True, verbose_name='课程描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self):
        chars = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.choices(chars, k=6))
            if not Course.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return f'{self.name}({self.code})'

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'

class CourseStudent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_records', verbose_name='课程')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_records', verbose_name='学生')
    join_time = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')

    class Meta:
        unique_together = ['course', 'student']
        verbose_name = '课程学生关系'
        verbose_name_plural = '课程学生关系'

    def __str__(self):
        return f'{self.course.name}-{self.student.username}'

class Classroom(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classrooms', verbose_name='所属课程')
    name = models.CharField(max_length=100, verbose_name='课堂名称')
    is_active = models.BooleanField(default=True, verbose_name='是否进行中')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')

    class Meta:
        verbose_name = '课堂'
        verbose_name_plural = '课堂'

    def __str__(self):
        return f'{self.course.name}-{self.name}'

class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name='任务标题')
    description = models.TextField(blank=True, null=True, verbose_name='任务描述')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tasks', verbose_name='所属课程')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True, verbose_name='所属课堂')
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建教师')
    questions = models.ManyToManyField(Question, verbose_name='题目列表')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    duration = models.IntegerField(default=10, verbose_name='时长（分钟）')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    status = models.IntegerField(default=1, verbose_name='状态：1进行中 2已结束')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务'

class AnswerRecord(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='所属任务')
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='答题学生')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='答题题目')
    student_answer = models.CharField(max_length=200, verbose_name='学生答案')
    is_correct = models.BooleanField(null=True, blank=True, default=None, verbose_name='是否正确（None表示待批改）')

    def __str__(self):
        return f'{self.student.username}-{self.question.title}'

    class Meta:
        verbose_name = '答题记录'
        verbose_name_plural = '答题记录'

class TaskScore(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='scores', verbose_name='所属任务')
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='学生')
    score = models.IntegerField(default=0, verbose_name='得分')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='计算时间')

    class Meta:
        unique_together = ['task', 'student']
        verbose_name = '任务得分'
        verbose_name_plural = '任务得分'

    def __str__(self):
        return f'{self.student.username}-{self.task.title}: {self.score}'
