from pytest_factoryboy import register
from .factories import UserFactory, CategoryFactory, PostFactory, CommentFactory

register(UserFactory)
register(CategoryFactory)
register(PostFactory)
register(CommentFactory)
