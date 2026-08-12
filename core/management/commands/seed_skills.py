from django.core.management.base import BaseCommand
from core.models import Skill

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        skills = [
             ('frontend'),
    ('backend'),
    ('fullstack'),
    ('mobile-development'),
    ('data-science'),
    ('artificial-intelligence'),
    ('cybersecurity'),
    ('devops'),
    ('cloud-computing'),
    ('ui-ux-design'),
    ('game-development'),
    ('open-source'),
        ]

        for s in skills:
            Skill.objects.get_or_create(name=s)

        self.stdout.write(self.style.SUCCESS("Skills seeded"))