from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, response
from django.urls import reverse
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm
from .models import Topic, Course, Student, Order, Review
from django.shortcuts import get_object_or_404
# Create your views here.
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'mysiteS21',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def user_login(request):
    print(request.get_full_path())

    if(request.GET.get('next')):
        request.session['profile']=request.GET.get('next')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if('profile' in request.session.keys()):
                    if('myapp/myaccount' in request.session['profile']):
                        return HttpResponseRedirect(reverse('myapp:myaccount'))
                else:
                    return HttpResponseRedirect(reverse('myapp:index'))

            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    login_time = request.session.get('last_login', 'over 1 hour ago')
    return render(request, 'myapp/index.html', {'top_list': top_list, 'name': request.user})


# ------Lab 5 content-------
# top_list = Topic.objects.all().order_by('id')[:10]
# response = HttpResponse()
# heading1 = '<p>' + 'List of topics: ' + '</p>'
# response.write(heading1)
# for topic in top_list:
#     para = '<p>'+ str(topic.id) + ': ' + str(topic) + ':</p>'
#     response.write(para)
#
#     response.write('<ul>')
#     for courses in Course.objects.filter(topic_id=topic.id).order_by('-title')[:5]:
#         list = '<li>'+str(courses)+': $'+str(courses.price)+'</li>'
#         response.write(list)
#     response.write('</ul>')

# return response

def about(request):
    response = HttpResponse()
    heading = '<p>' + 'This is new E-Learning platform! Enjoy learning in a new way' + '</p>'
    response.write(heading)
    visits = int(request.COOKIES.get('about_visits', '0'))
    visits += 1
    max_age = 300
    last_user = request.COOKIES.get('last_user', 'New User')
    response = render(request, 'myapp/about.html',
                      {'user': request.user, 'about_visits': visits, 'last_user': last_user})
    response.set_cookie('about_visits', visits, max_age=max_age)
    response.set_cookie('last_user', request.user.username)
    return response
    # return HttpResponsePermanentRedirect(reverse('about'))


def detail(request, topic_id):
    response = HttpResponse()
    topic = get_object_or_404(Topic, id=topic_id)
    course_list = Course.objects.filter(topic=topic)
    response = HttpResponse()
    for course in course_list:
        para = '<p>' + str(course.title.upper()) + "is of " + str(course.topic.length) + "$weeks" + "</p>"
    response.write(para)
    return render(request, 'myapp/detail.html', {'course_list': course_list})
    # ---lab5 --content:
    # response.write('<h3>'+ topic.name.upper() +"</h3>")
    # response.write('Length:'+ str(topic.length))
    # for courses in Course.objects.filter(topic_id=topic_id).order_by('title')[:5]:
    #     list = '<p>'+ str(courses) +': $'+ str(courses.price)+ '</p>'
    #     response.write(list)
    #
    # return response


def findcourses(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            maxPrice = form.cleaned_data['max_price']
            topics = Topic.objects.filter(length=length)
            courselist = {}
            if length == 0:  # user did not select a course length
                courselist = Course.objects.filter(price__lte=maxPrice)
                return render(request, 'myapp/results.html',
                              {'courselist': courselist, 'name': name, 'price': maxPrice})
            else:
                for top in topics:
                    courselist[top] = list(top.courses.all() and top.courses.filter(price__lte=maxPrice))
                return render(request, 'myapp/results.html',
                              {'courselist': courselist, 'name': name, 'length': length, 'price': maxPrice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findcourses.html', {'form': form, 'name': request.user})


def placeorder(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=True)
            student = order.Student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
                return render(request, 'myapp/order_response.html',
                              {'courses': courses, 'order': order, 'name': request.user})
        else:
            return render(request, 'myapp/place_order.html', {'form': form, 'name': request.user})
    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form, 'name': request.user})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            course_name = form.cleaned_data['course']
            reviewer = form.cleaned_data['reviewer']
            comments = form.cleaned_data['comments']
            if rating in range(0, 6):
                review_obj = Review.objects.create(reviewer=reviewer, course=course_name, rating=rating,
                                                   comments=comments)
                review_obj.save()
                update_review = Course.objects.get(title=course_name)
                update_review.num_reviews += 1
                update_review.save()
                return redirect('/myapp/')
            else:
                form = ReviewForm()
                messages.info(request, 'PLease rate on scale of 5 :)')
                return render(request, 'myapp/review.html', {'form': form, 'name': request.user})
        return render(request, 'myapp/review.html', {'form': form, 'name': request.user})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form, 'name': request.user})


@login_required
def myaccount(request):
    print("entered my accout")
    if request.user.is_authenticated:
        user_name = request.user.username
        fname = User.first_name
        lname = User.last_name
        #course_list = Student.objects.filter(username=user_name).first().registered_courses.all()
        #topics = Student.objects.filter(username=user_name).first().interested_in.all()
        try:
            course_list = Student.objects.filter(username=user_name).first().registered_courses.all()
            topics = Student.objects.filter(username=user_name).first().interested_in.all()
        except AttributeError as e:
            return render(request, 'myapp/myaccount.html')
        return render(request, 'myapp/myaccount.html',
                      {'name': request.user, 'fname': fname, 'lname': lname, 'course_list': course_list,
                       'topics': topics})
    else:
        print("myaccount- ",request.get_full_path())
        return redirect(request.GET.get('next','/myaccount'))

def isLogin(user):
    if user.is_authenticated:
        return False
    else:
        return True

@user_passes_test(isLogin)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_obj = User.objects.create(username=username, first_name=first_name, last_name=last_name, password=password)
            user_obj.set_password(password)
            user_obj.save()
            return redirect('/myapp/')
        return render(request, 'myapp/register.html', {'form': form, 'name': request.user})
    else:
        form = RegisterForm
        return render(request, 'myapp/register.html', {'form': form, 'name': request.user})
