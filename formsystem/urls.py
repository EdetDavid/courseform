# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("blog/", views.blog, name="blog"),
    path("register/student/", views.register_student, name="register_student"),
    path("register/hod/", views.register_hod, name="register_hod"),
    path("submit_course_form/", views.submit_course_form,
         name="submit_course_form"),
    path("course_forms/", views.course_forms, name="course_forms"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("hod_dashboard/", views.hod_dashboard, name="hod_dashboard"),
    path("profile/", views.profile, name="profile"),
    path("update_profile/", views.update_profile, name="update_profile"),
    path('view_course_form/<int:pk>/',
         views.view_course_form, name='view_course_form'),

    path("toggle_is_signed/<int:pk>/",
         views.toggle_is_signed, name="toggle_is_signed"),
path("download_course_form/<int:pk>/", views.download_course_form, name="download_course_form"),
path("send_signed_form/", views.send_signed_form, name="send_signed_form"),

path("signed_course_forms/", views.signed_course_forms, name="signed_course_forms"),

    path("logout/", views.logout_user, name="logout_user"),
]
