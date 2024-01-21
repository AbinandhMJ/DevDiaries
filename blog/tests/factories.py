import factory
from django.contrib.auth.models import User
from blog.blogger.models import Post, Category, Comment

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    password = 'test'
    username = factory.Sequence(lambda n: f'user{n}')
    is_superuser = True
    is_staff = True

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Sequence(lambda n: f'Category {n}')

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f'Title {n}')
    subtitle = factory.Sequence(lambda n: f'Subtitle {n}')
    slug = factory.Sequence(lambda n: f'slug-{n}')
    author = factory.SubFactory(UserFactory)
    content = factory.Sequence(lambda n: f'Content {n}')
    status = 'published'

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.Sequence(lambda n: f'Author {n}')
    content = factory.Sequence(lambda n: f'Comment content {n}')
    post = factory.SubFactory(PostFactory)
