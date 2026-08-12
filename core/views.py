# core/views.py
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, ChatMessage, ChatConversation, Profile, Skill
from .forms import CreatingPostForm, UserRegistrationForm, EditingProfileForm, ChatMessageForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator



# home
def home_view(request):
    posts = Post.objects.select_related("author").order_by("-created_at")


    posts = Post.objects.order_by('-created_at')

    city = request.GET.get("city")
    skill = request.GET.get("skill")
    purpose = request.GET.get("purpose")

    if city:
        posts = posts.filter(city=city)

    if skill:
        posts = posts.filter(
            Q(my_skills=skill) |
            Q(skills_needed=skill)
        )

    if purpose:
        posts = posts.filter(purpose=purpose)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "core/home.html", {
    
    "city": city,
    "skill": skill,
    "purpose": purpose,
    "page_obj": page_obj,
})

# register
def register_view(request):
    form = UserRegistrationForm()  
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد')
            return redirect('profile', username= user.username)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    return render(request,'core/register.html', {'form': form})




# login
def login_view(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username= username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'خوش امدی {username}')
            return redirect('home')
        else:
            messages.error(request,'نام کاربری یا رمز عبور اشتباه است')

    return render(request,'core/login.html')

# logout
def logout_view(request):
    logout(request)
    messages.info(request,'با موفقیت خارج شدید')
    return redirect('home')

# profile view
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, 'core/profile.html', {
        'profile_user': user,
        'profile': profile,
    })


@login_required
def edit_profile_view(request, username):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = EditingProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            messages.success(request, f'با موفقیت ذخیره شد')
            skill_ids = request.POST.getlist("skills")
            profile.skills.set(skill_ids)
            return redirect(
                "profile",
                username=request.user.username
            )
        else:
            messages.error(request, f'مشکلی پیش آمده، لطفا دوباره تلاش کنید')


    else:
        form = EditingProfileForm(
            instance=profile
        )

    return render(
        request,
        "core/edit_profile.html",
        {
            "form": form,
            "profile": profile,
            "skills": Skill.objects.all(),
            "selected_skills": list(
                profile.skills.values_list('id', flat=True)
            ),
        }
    )

# create a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatingPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'پست با موفقیت ایجاد شد!')
            return redirect('post_list')
        else:
            messages.error(request, f'مشکلی پیش آمده، لطفا دوباره تلاش کنید')
    else:
        form = CreatingPostForm()


    return render(request, 'core/create_post.html', {'form': form})


from django.db.models import Q

@login_required
def post_list_view(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    city = request.GET.get('city')
    skill = request.GET.get('skill')
    purpose = request.GET.get('purpose')

    if city:
        posts = posts.filter(city=city)

    elif skill:
        posts = posts.filter(
            Q(my_skills=skill) |
            Q(skills_needed=skill)
        )

    elif purpose:
        posts = posts.filter(purpose=purpose)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'core/post_list.html',
        {"city": city,
    "skill": skill,
    "purpose": purpose,
    "page_obj": page_obj,}
    )

# post edit
@login_required
def edit_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == "POST":
        form = CreatingPostForm(
            request.POST,
            instance=post
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'پست با موفقیت ویرایش شد!')
            return redirect("post_list")
            
        else:
            messages.error(request, f'مشکلی پیش آمده، لطفا دوباره تلاش کنید')

    else:
        form = CreatingPostForm(instance=post)

    return render(
        request,
        "core/edit_post.html",
        {
            "form": form,
            "post": post
        }
    )

# post delete 
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )
    if request.method == "POST":
        post.delete()
        messages.success(request, 'پست با موفقیت حذف شد!')
            
    else:
        messages.error(request, f'مشکلی پیش آمده، لطفا دوباره تلاش کنید')
    return redirect("post_list")


# chat_deatail in when logged in
@login_required
def chat_list_view(request):

    conversations = ChatConversation.objects.filter(
        Q(participant1=request.user) | Q(participant2=request.user)
    ).order_by('-last_message_time')
    

    conversations_data = []
    for conv in conversations:
        other_user = conv.get_other_user(request.user)
        unread_count = conv.get_unread_count(request.user)
        
        conversations_data.append({
            'conversation': conv,
            'other_user': other_user,
            'last_message': conv.last_message,
            'last_message_time': conv.last_message_time,
            'unread_count': unread_count,
        })
        # notice how im not showing anything when nothing is selected
    return render(request, 'core/chat_list.html', 
                  {'conversations': conversations_data,
                   'other_user': None,
    'conversation': None,
                   })

# for when the user has opened a chat
@login_required
def chat_detail_view(request, user_id=None):

    # LEFT SIDE
    conversations = ChatConversation.objects.filter(
        Q(participant1=request.user) |
        Q(participant2=request.user)
    ).order_by('-last_message_time')

    conv_list = []

    for chat in conversations:
        other_user = chat.participant2 if chat.participant1 == request.user else chat.participant1

        unread_count = ChatMessage.objects.filter(
            sender=other_user,
            receiver=request.user,
            is_read=False
        ).count()

        conv_list.append({
            
            "other_user": other_user,
            "last_message": chat.last_message,
            "last_message_time": chat.last_message_time,
            "unread_count": unread_count,
        })

    # RIGHT SIDE 
    other_user = None
    conversation = None
    messages_list = []

    if user_id:
        other_user = get_object_or_404(User, id=user_id)

        if other_user != request.user:

            conversation = ChatConversation.objects.filter(
                (Q(participant1=request.user) & Q(participant2=other_user)) |
                (Q(participant1=other_user) & Q(participant2=request.user))
            ).first()

            if not conversation:
                user1, user2 = request.user, other_user
                if user1.id > user2.id:
                    user1, user2 = user2, user1

                conversation = ChatConversation.objects.create(
                    participant1=user1,
                    participant2=user2
                )
           
            messages_list = ChatMessage.objects.filter(
                conversation=conversation
            ).order_by('created_at')

            ChatMessage.objects.filter(
                sender=other_user,
                receiver=request.user,
                is_read=False
            ).update(is_read=True)

    return render(request, "core/chat_list.html", {
        "conversations": conv_list,
        "conversation": conversation,
        "other_user": other_user,
        "messages1": messages_list,
    })