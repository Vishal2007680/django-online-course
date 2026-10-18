from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Add your existing course list and detail routes here...
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('<int:course_id>/submission/<int:submission_id>/show_exam_result/', views.show_exam_result, name='show_exam_result'),
]
