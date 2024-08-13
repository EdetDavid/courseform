from django.contrib import admin
from .models import Department, HOD, Student, CourseForm, SignedCourseForm


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class HODAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    search_fields = ('user__username', 'department__name')
    list_filter = ('department',)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    search_fields = ('user__username', 'department__name')
    list_filter = ('department',)


class CourseFormAdmin(admin.ModelAdmin):
    list_display = ['student', 'hod']  # Removed 'is_signed' and 'signed_at'
    list_filter = ['hod']  # Removed 'is_signed'
    search_fields = ['student__user__username']


class SignedCourseFormAdmin(admin.ModelAdmin):
    list_display = ['get_student_username', 'signed_at']
    list_filter = ['signed_at']
    date_hierarchy = 'signed_at'
    search_fields = ['course_form__student__user__username']

    def get_student_username(self, obj):
        return obj.course_form.student.user.username
    get_student_username.short_description = 'Student Username'





admin.site.register(Department, DepartmentAdmin)
admin.site.register(HOD, HODAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(CourseForm, CourseFormAdmin)
admin.site.register(SignedCourseForm, SignedCourseFormAdmin)


