from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .models import AcademicGroup, Course, Department, StudentProfile
from .forms import AcademicGroupForm, CourseForm, DepartmentForm


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required 
def profile(request): 
    return render( 
        request, 
        'profile.html', 
        { 
            'is_methodist': is_methodist( 
                request.user 
            ) 
        } 
    ) 

@login_required 
def department_list(request): 
    departments = Department.objects.all() 
 
    return render( 
        request, 
        'department_list.html', 

        { 
            'departments': departments, 
            'is_methodist': is_methodist( 
                request.user 
            ), 
        } 
    ) 

def is_methodist(user): 
    return user.groups.filter( 
        name='Методист' 
    ).exists() 

@login_required 
@user_passes_test(is_methodist) 
def department_create(request): 
    if request.method == 'POST': 
 
        form = DepartmentForm( 
            request.POST 
        ) 
 
        if form.is_valid(): 
            form.save() 
 
            return redirect( 
                'department_list' 
            ) 
 
    else: 
        form = DepartmentForm() 
 
    return render( 
        request, 
        'object_form.html', 
        { 
            'form': form, 
            'title': 'Добавление факультета', 
        } 
    )

@login_required 
@user_passes_test(is_methodist) 
def department_update( 
    request, 
    pk 
): 
 
    department = get_object_or_404( 
        Department, 
        pk=pk 
    ) 
 
    if request.method == 'POST': 
 
        form = DepartmentForm(
            request.POST, 
            instance=department 
        ) 
 
        if form.is_valid(): 
            form.save() 
 
            return redirect( 
                'department_list' 
            ) 
 
    else: 
 
        form = DepartmentForm( 
            instance=department 
        ) 
 
    return render( 
        request, 
        'object_form.html', 
        { 
            'form': form, 
            'title': 'Изменение факультета', 
        } 
    ) 

@login_required 
@user_passes_test(is_methodist) 
def department_delete( 
    request, 
    pk 
): 
 
    department = get_object_or_404( 
        Department, 
        pk=pk 
    ) 
 
    if request.method == 'POST': 
 
        department.delete() 
 
        return redirect( 
            'department_list' 
        ) 
 
    return render( 
        request, 
        'object_confirm_delete.html', 
        { 
            'object': department, 
            'title': 'Удаление факультета', 
        } 
    )

@login_required
def academic_group_list(request):
    academic_groups = AcademicGroup.objects.select_related(
        'department'
    ).all()

    return render(
        request,
        'academic_group_list.html',
        {
            'academic_groups': academic_groups,
            'is_methodist': is_methodist(request.user),
        }
    )


@login_required
@user_passes_test(is_methodist)
def academic_group_create(request):
    if request.method == 'POST':
        form = AcademicGroupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('academic_group_list')
    else:
        form = AcademicGroupForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление учебной группы',
        }
    )


@login_required
@user_passes_test(is_methodist)
def academic_group_update(request, pk):
    academic_group = get_object_or_404(AcademicGroup, pk=pk)

    if request.method == 'POST':
        form = AcademicGroupForm(
            request.POST,
            instance=academic_group
        )

        if form.is_valid():
            form.save()
            return redirect('academic_group_list')
    else:
        form = AcademicGroupForm(instance=academic_group)

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение учебной группы',
        }
    )


@login_required
@user_passes_test(is_methodist)
def academic_group_delete(request, pk):
    academic_group = get_object_or_404(AcademicGroup, pk=pk)

    if request.method == 'POST':
        academic_group.delete()
        return redirect('academic_group_list')

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': academic_group,
            'title': 'Удаление учебной группы',
        }
    )

@login_required
def course_list(request):
    courses = Course.objects.select_related('department').all()

    return render(
        request,
        'course_list.html',
        {
            'courses': courses,
            'is_methodist': is_methodist(request.user),
        }
    )

@login_required
@user_passes_test(is_methodist)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Добавление курса',
        }
    )


@login_required
@user_passes_test(is_methodist)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)

    return render(
        request,
        'object_form.html',
        {
            'form': form,
            'title': 'Изменение курса',
        }
    )


@login_required
@user_passes_test(is_methodist)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        course.delete()
        return redirect('course_list')

    return render(
        request,
        'object_confirm_delete.html',
        {
            'object': course,
            'title': 'Удаление курса',
        }
    )

@login_required
def dashboard(request):
    departments = Department.objects.annotate(
        courses_total=Count('courses', distinct=True),
        students_total=Count('students', distinct=True),
    ).order_by('name')

    groups = AcademicGroup.objects.annotate(
        students_total=Count('students', distinct=True),
    ).select_related('department').order_by('name')

    chart_data = {
        'courses_by_department': {
            'labels': [department.name for department in departments],
            'values': [department.courses_total for department in departments],
        },
        'students_by_department': {
            'labels': [department.name for department in departments],
            'values': [department.students_total for department in departments],
        },
        'students_by_group': {
            'labels': [group.name for group in groups],
            'values': [group.students_total for group in groups],
        },
    }

    context = {
        'departments_count': Department.objects.count(),
        'courses_count': Course.objects.count(),
        'groups_count': AcademicGroup.objects.count(),
        'students_count': StudentProfile.objects.count(),
        'chart_data': chart_data,
    }

    return render(request, 'dashboard.html', context)
