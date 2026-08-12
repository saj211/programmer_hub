# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
      
        return self.name
    

CITY_CHOICES = [
        ('TEHRAN', 'تهران'),
        ('QOM', 'قم'),
        ('SHIRAZ', 'شیراز'),
        ('ISFAHAN', 'اصفهان'),
        ('MASHHAD', 'مشهد'),
        ('SEMNAN', 'سمنان'),
    ]
SKILL_CHOICES = [
    ('frontend', 'فرانت‌اند'),
    ('backend', 'بک‌اند'),
    ('fullstack', 'فول‌استک'),
    ('mobile-development', 'توسعه موبایل'),
    ('data-science', 'علم داده'),
    ('artificial-intelligence', 'هوش مصنوعی'),
    ('cybersecurity', 'امنیت سایبری'),
    ('devops', 'DevOps'),
    ('cloud-computing', 'رایانش ابری'),
    ('ui-ux-design', 'طراحی UI/UX'),
    ('game-development', 'توسعه بازی'),
    ('open-source', 'متن‌باز'),
]

PURPOSE_CHOICES = [
    ('collaboration', 'همکاری در پروژه'),
    ('looking_for_team', 'دنبال تیم'),
    ('looking_for_member', 'دنبال هم‌تیمی'),
    ('learning_partner', 'پارتنر یادگیری'),
    ('startup', 'همکاری استارتاپی'),
    ('job_opportunity', 'فرصت شغلی'),
]

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    city = models.CharField(max_length=20, choices=CITY_CHOICES, default='TEHRAN')
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='learning_partner')
    my_skills = models.CharField(
    max_length=50,
    choices=SKILL_CHOICES,
    default='frontend')
    skills_needed = models.CharField(
    max_length=50,
    choices=SKILL_CHOICES,
    default='frontend')
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title


ROLE_CHOICES = [
        ('frontend', 'فرانت‌اند'),
        ('backend', 'بک‌اند'),
        ('fullstack', 'فول استک'),
        ('mobile', 'موبایل'),
        ('devops', 'دواپس'),
        ('data', 'دیتا ساینس'),
        ('designer', 'طراح'),
        ('pm', 'مدیر پروژه'),
    ]


# profile
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, help_text="درباره خودت بنویس")
    avatar = models.FileField(upload_to='avatar/', blank=True, null=True)
    github_URL = models.URLField(blank=True, help_text="لینک گیت هاب")
    linkedin_URL = models.URLField(blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="profiles"
    )
    def __str__(self):
        return f"پروفایل {self.user.username}"

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"


class ChatConversation(models.Model):
    
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_as_p1')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_as_p2')
    last_message = models.TextField(blank=True)
    last_message_time = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"مکالمه بین {self.participant1.username} و {self.participant2.username}"
    
    class Meta:
        unique_together = ['participant1', 'participant2']
        verbose_name = "مکالمه"
        verbose_name_plural = "مکالمه‌ها"
    
    def get_other_user(self, user):
        if self.participant1 == user:
            return self.participant2
        return self.participant1
    
    def get_unread_count(self, user):
        return ChatMessage.objects.filter(
            receiver=user,
            sender=self.get_other_user(user),
            is_read=False
        ).count()
    
    
class ChatMessage(models.Model):
    conversation = models.ForeignKey(
    ChatConversation,
    on_delete=models.CASCADE,
    related_name='messages'
)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.message[:30]}"
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"
