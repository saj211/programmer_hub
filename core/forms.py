from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Profile, Skill, ChatMessage
import re


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('این نام کاربری قبلاً ثبت شده است')
        return username
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        
        # بررسی طول رمز
        if len(password) < 8:
            raise forms.ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد')
        
        # بررسی وجود حرف بزرگ
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('رمز عبور باید حداقل یک حرف بزرگ (A-Z) داشته باشد')
        
        # بررسی وجود حرف کوچک
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError('رمز عبور باید حداقل یک حرف کوچک (a-z) داشته باشد')
        
        # بررسی وجود عدد
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError('رمز عبور باید حداقل یک عدد (0-9) داشته باشد')
        
        # بررسی شبیه نبودن به نام کاربری
        if username and password.lower() == username.lower():
            raise forms.ValidationError('رمز عبور نباید شبیه نام کاربری باشد')
        
        return password
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('رمز عبور و تکرار آن مطابقت ندارند')
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# what to be shown when you creating a post
class CreatingPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'my_skills', 'skills_needed', 
                    'city', 'purpose', 'title']
        widgets = {
                'description': forms.Textarea(attrs={'rows': 5}),
                'my_skills': forms.Select(attrs={
                    'class': 'form-control',
                    'style': 'width: 100%;'
                }),
                'skills_needed': forms.Select(attrs={
                    'class': 'form-control',
                    'style': 'width: 100%;'
                }),
                'purpose': forms.Select(attrs={
                    'class': 'form-control',
                    'style': 'width: 100%;'
                }),
                'city': forms.Select(attrs={
                    'class': 'form-control',
                    'style': 'width: 100%;'
                }),
                
                'title': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder' : 'یه رفیق برای کد زدن'
                }),
            }
        
class EditingProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'skills', 'github_URL', 'linkedin_URL', 'avatar']

        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
            }),

            'bio': forms.Textarea(attrs={
                'rows': 5
            }),

            'github_URL': forms.URLInput(attrs={
                'class': 'form-control'
            }),

            'linkedin_URL': forms.URLInput(attrs={
                'class': 'form-control'
            }),

            'skills': forms.CheckboxSelectMultiple(),
        }


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2 bg-black border border-hacker-green text-hacker-green rounded-lg focus:outline-none focus:ring-2 focus:ring-hacker-green focus:ring-opacity-50',
                'placeholder': 'پیام خود را بنویسید...',
                'id': 'message-input'
            })
        }
        labels = {
            'message': ''
        }
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and message.strip():
            return message.strip()
        raise forms.ValidationError("پیام نمی‌تواند خالی باشد")