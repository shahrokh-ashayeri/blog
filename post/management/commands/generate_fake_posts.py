import random
from faker import Faker
from post.models import Post, Category  
from django.contrib.auth.models import User 
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate fake blog posts'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of posts to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker()

        category = Category.objects.first()
        user = User.objects.first()
        
        for _ in range(total):
            Post.objects.create(
                title=fake.sentence(),
                slug=fake.slug(),
                category=category,
                content=fake.paragraph(nb_sentences=20),
                created_at=fake.date_time_this_year(),
                updated_at=fake.date_time_this_year(),
                published_time=fake.date_time_this_year(),
                status=random.choice(['draft', 'published', 'archived']),
                author=user,
            )

        self.stdout.write(self.style.SUCCESS(f'{total} fake posts created!'))
