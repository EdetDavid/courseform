# from django.db import models
# from django.utils import timezone

# class Department(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


# class HOD(models.Model):
#     user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
#     department = models.OneToOneField(Department, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username


# class Student(models.Model):
#     user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username


# class CourseForm(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     hod = models.ForeignKey(HOD, on_delete=models.CASCADE)
#     form_content = models.FileField(upload_to='course_forms/')
#     is_signed = models.BooleanField(default=False)
#     signed_at = models.DateTimeField(null=True, blank=True)
    

#     def __str__(self):
#         return f"Course Form for {self.student.user.username}"


# class SignedCourseForm(models.Model):
#     course_form = models.OneToOneField(CourseForm, on_delete=models.CASCADE)
#     signed_at = models.DateTimeField(default=timezone.now)
#     signed_form = models.FileField(upload_to='signed_course_forms/')

#     def __str__(self):
#         return f"Signed Course Form for {self.course_form.student.user.username}"


from django.db import models
from django.utils import timezone
from django.db.models.signals import post_migrate
from django.apps import apps

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

def create_default_departments(sender, **kwargs):
    """Create default departments after migrations."""
    Department = apps.get_model('formsystem', 'Department')
    if not Department.objects.exists():
        Department.objects.create(name='Computer Science')
        Department.objects.create(name='Mathematics')

post_migrate.connect(create_default_departments, sender=apps.get_app_config('formsystem'))


class HOD(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CourseForm(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hod = models.ForeignKey(HOD, on_delete=models.CASCADE)
    form_content = models.FileField(upload_to='course_forms/')
    is_signed = models.BooleanField(default=False)
    signed_at = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"Course Form for {self.student.user.username}"


class SignedCourseForm(models.Model):
    course_form = models.OneToOneField(CourseForm, on_delete=models.CASCADE)
    signed_at = models.DateTimeField(default=timezone.now)
    signed_form = models.FileField(upload_to='signed_course_forms/')

    def __str__(self):
        return f"Signed Course Form for {self.course_form.student.user.username}"
