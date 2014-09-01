from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from polls.models import Product
from polls.forms import UserForm, UserProfileForm

def index(request):
    latest_products = Product.objects.all()
    context = {'latest_products': latest_products}
    return render(request, 'polls/index.html', context)

def detail(request, poll_id):
    return HttpResponse('You are looking at poll %s' % poll_id)

def results(request, poll_id):
    return HttpResponse('You are looking at the results of poll %s' % poll_id)

def vote(request, poll_id):
    return HttpResponse('You are voting on poll %s' % poll_id)

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'polls/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/polls/')
            else:
                return HttpResponse('Invalid login details.')
        else:
            print 'Invalid login details: {0}:{1}'.format(username, password)
            return HttpResponse('Your Dabbawala account is disabled')
    else:
        return render_to_response('polls/login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/polls/')
