from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Comment
from django.db.models import Count

# Create your views here.
def index(request):
  return render(request, 'secret_app/index.html')

def login(request):
    print "gooz"
    PostData = {
        'first_name' : request.POST['first_name'],
        'last_name' : request.POST['last_name'],
        'email' : request.POST['email'],
        'password' : request.POST['password'],
        'confirm_password' : request.POST['confirm_password']
    }

    if not User.objects.login(PostData):
        new_user_id = User.objects.create_user(PostData)
        request.session['user_id'] = new_user_id
        request.session['name'] = User.objects.get(id = new_user_id).first_name
        request.session['isPop'] = 0
        return redirect("/success")
    for error in User.objects.login(PostData):
        messages.error(request, error)
    request.session['loginError']=False
    return redirect('/')

def register(request):
    PostData = {
        'email' : request.POST['email'],
        'password' : request.POST['password']
    }
    if not User.objects.register(PostData):
        user_id = User.objects.get(email=PostData['email']).id
        request.session['user_id'] = user.id
        request.session['isPop'] = 0
        return redirect('/success')
    for error in User.objects.register(PostData):
        messages.error(request, error)
    request.session['loginError']=True
    return redirect('/')

def comment(request):
    PostData = {
        'comment' : request.POST['comment'],
        'user_id' : request.session['user_id'],
    }
    Comment.objects.add_comment(PostData)
    return redirect('/success')

def success(request):
    if 'user_id' in request.session:
        first_name = User.objects.get(id=request.session['user_id']).first_name
        comments = Comment.objects.all().order_by('-created_at').annotate(num_likes=Count('likes'))
        liked_comments = Comment.objects.filter(likes = User.objects.get(id = request.session['user_id']))
        arr = []
        for liked_comment in liked_comments:
            arr.append(liked_comment.id)


        # allcomments = Comment.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')



        context = {
            'first_name' : first_name,
            'comments' : comments,
            'messages' : messages,
            'arr' : arr,
            'allcomments' : Comment.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
        }
        return render(request, "secret_app/show.html", context)
    messages.error(request, 'Please login')
    return redirect('/')

def like(request, comment_id):
    PostData = {
        'comment_id': comment_id,
        'user_id': request.session['user_id']
    }
    Comment.objects.like(PostData)
    return redirect('/success')
def unlike(request, comment_id):
    PostData = {
        'comment_id': comment_id,
        'user_id': request.session['user_id']
    }
    Comment.objects.unlike(PostData)
    return redirect('/success')

def popular(request):
    request.session['isPop'] = 1
    # if Comment.objects.all().count() != 0:
    #     allcomments = Comment.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
    #     context = {
    #         "secret" : allsecrets,
    #         "currentuser" : User.objects.get(user_id=request.session['user_id'])
    #     }
    return redirect('/success')

def recent(request):
    request.session['isPop'] = 0

    return redirect('/success')

def delete(self, PostData):
    dele = Comment.objects.get(id=PostData['comment_id'])
    dele.delete()
    return redirect('/success')

def logout(request):
    request.session.pop('user_id')
    return redirect('/')
