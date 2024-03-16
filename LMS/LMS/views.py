from django.shortcuts import render, redirect, get_object_or_404
from app.models import *
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import ProfileForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
def BASE(request):
    return render(request, 'base.html')
def BASE2(request):
    return render(request, 'base2.html')


def INDEX (request):
  return render(request, 'main/index.html')

def ABOUT_US(request):
    mission = Mission.objects.first()
    vision = Vision.objects.first()
    history = History.objects.first()
    return render(request, 'main/about.html', {'mission': mission, 'vision': vision, 'history': history})


def COURSE(request):
    categories = Categories.objects.all().order_by('id')
    course = Course.objects.filter(status='PUBLISH').order_by('-id')

    context = {
        'category': categories,
        'course': course,
    }
    return render(request, 'main/course.html', context)

def ALL_COURSE(request):
    categories = Categories.objects.all().order_by('id')
    course = Course.objects.filter(status='PUBLISH').order_by('-id')

    context = {
        'category': categories,
        'course': course,
    }
    return render(request, 'course/all_course.html', context)





@login_required
def COURSE_DETAILS(request, slug):
    try:
        # Retrieve the course object using the provided slug
        course = Course.objects.get(slug=slug)
        
        # Calculate the total time duration of videos related to the course
        time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
        
        # Retrieve the course object by slug
        course_id = Course.objects.get(slug=slug)
        
        try:
            # Check if the user is already enrolled in the course
            check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
        except UserCourse.DoesNotExist:
            # If not enrolled, set check_enroll to None
            check_enroll = None
        
        # Prepare context data to pass to the template
        context = {
            'course': course,
            'time_duration': time_duration,
            'check_enroll': check_enroll
        }
        # Render the course details page with the course object and context data
        return render(request, 'course/course_details.html', context)
    except Course.DoesNotExist:
        # If the course does not exist, redirect to the 404 page
        return redirect('404')

def WATCH_COURSE(request, slug=None):
    course = Course.objects.filter(slug=slug)
    lecture = request.GET.get('lecture')
    video = Video.objects.get(id=lecture)
    print (video)
    if course.exists():
        course = course.first()
    else: 
        return redirect('404')

    context = {
        'course': course,
        'video': first_video,
    }
    
    return render(request, 'course/watch_course.html', context)

def TEAM(request): 
    team_members = TeamMember.objects.all()
    context = {'team_members': team_members}
    return render(request, 'main/team.html', context)

def SIDEBAR(request):
    return render(request, 'main/sidebar.html')

def MAIN_PROFILLE(request):
     # Fetch the existing profile if it exists
    student_profile, created = StudentProfile.objects.get_or_create(user=request.user)
    course = UserCourse.objects.filter(user= request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('main_profile'))  # Redirect to the same page after saving
    else:
        form = ProfileForm(instance=student_profile)
    
    context = {
        'form': form,
        'student_profile': student_profile,
        'course':course,
    }
    return render(request, 'main/main_profile.html', context)

def NOTICE (request):
    notices = Notice.objects.all()
    return render (request, 'main/notice.html', {'notices': notices})


def CHECKOUT(request, slug):
    course = Course.objects.get(slug=slug)
    context = {'course': course}

    if course.price == 0:
        # If free, create a UserCourse object for the current user and course
        user_course = UserCourse.objects.create(
            user=request.user,
            course=course,
        )
        messages.success(request, 'Course is successfully enrolled')
        return redirect('all_course')

    return render(request, 'checkout/checkout.html', context)


from django.shortcuts import get_object_or_404

def WATCH_COURSE(request, slug=None):
    if slug:
        course = get_object_or_404(Course, slug=slug)
    else:
        course = Course.objects.first()  # Fetch the first course if no slug is provided

    video = None
    lecture = request.GET.get('lecture')
    
    if lecture:
        try:
            video = Video.objects.get(id=lecture)
        except Video.DoesNotExist:
            video = None

    context = {
        'course': course,
        'video': video,
        'lecture': lecture,
    }
    return render(request, 'course/watch_course.html', context)

def error_404(request):
    return render(request, 'error/404.html', status=404)

def MODELEXAM(request):
    quizzes = quiz.objects.all()
    return render(request, 'quiz/modelexam.html',  {'quizzes': quizzes})







