from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    selected_choices = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            selected_choices.append(int(value))
            
    submission = Submission.objects.create(enrollment=enrollment)
    submission.choices.set(selected_choices)
    
    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    selected_ids = list(submission.choices.values_list('id', flat=True))
    
    total_score = 0
    total_possible = 0
    
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_possible += question.grade
            if question.is_get_score(selected_ids):
                total_score += question.grade
                
    percentage = int((total_score / total_possible) * 100) if total_possible > 0 else 0
    passed = percentage >= 80

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'total_score': total_score,
        'total_possible': total_possible,
        'percentage': percentage,
        'passed': passed
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
