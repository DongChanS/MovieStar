from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import ProfileModelForm, CustomUserChangeForm
from .models import Profile
from django.http import JsonResponse
import sys
sys.path.append("..")
from movies.models import Actor

# Create your views here.
@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

def login(request):
    next_path = request.GET.get('next')
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(next_path or 'index')
        else:
            return redirect('accounts:login')
    else:
        login_form = AuthenticationForm()
        return render(request, 'accounts/account.html',{
            'form' : login_form
        })
        

def signup(request):
    if request.method == "POST":
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            auth_login(request, user)
            return redirect('index')
        else:
            return redirect('accounts:signup')
    else:
        user_creation_form = UserCreationForm()
        return render(request, 'accounts/account.html', {
            'form' : user_creation_form
        })
       
@login_required 
def password(request):
    if request.method == "POST":
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            auth_login(request, user)
            return redirect('index')
        else:
            return redirect('accounts:password')
    else:
        password_form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/password.html', {
            'password_form' : password_form
        })
        
@login_required
def change(request):
    # 먼저 프로필 인스턴스를 지정해줘야함.
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_model_form = ProfileModelForm(request.POST, request.FILES, instance=user_profile)
        
        if profile_model_form.is_valid() and user_change_form.is_valid():
            user = user_change_form.save()
            profile = profile_model_form.save()
            return redirect('index')
        else:
            return redirect('accounts:change')
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        profile_model_form = ProfileModelForm(instance=user_profile)
        return render(request, 'accounts/change.html', {
            'user_change_form' : user_change_form,
            'profile_model_form' : profile_model_form,
        })

@login_required
def recommend(request):
    return render(request, 'recommend.html')
    
@login_required
def like(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)    
    
    if request.user in actor.like_users.all():
        # 좋아요 취소하기
        actor.like_users.remove(request.user)
        message = False
    else:
        # 좋아요 새로 하기
        actor.like_users.add(request.user)
        message = True
        
    return JsonResponse({'liked' : message})
    
def profile(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    
    """
    1. 유저정보 <- user 오브젝트
        - 프로필 사진
        - 개인정보
    2. 이 유저가 달았던 댓글들
        - 유저의 리뷰들을 뽑아서가야함
    3. 이 유저가 좋아하는 배우들
        - 유저가 좋아하는 배우들 가져가야함
    """
    reviews = user.review_set.all()
    actors = user.like_actors.all()
    
    return render(request, 'accounts/profile.html', {
        'reviews' : reviews,
        'actors' : actors,
        'person' : user,
    })
    