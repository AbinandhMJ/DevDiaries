import pytest
from blog.blogger.models import Post, Comment  # Add these import statements

pytestmark = pytest.mark.django_db

class TestPostModel:
    def test_str_return(self, post_factory):
        post = post_factory(title="test-post")
        assert str(post) == "test-post"

    def test_factory_creates_valid_instance(self, post_factory):
        post = post_factory()
        assert isinstance(post, Post)
        # Add additional assertions as needed to validate the created post instance

class TestCommentModel:
    def test_str_return(self, comment_factory):
        comment = comment_factory(author="test-author", post__title="test-post")
        assert str(comment) == "test-author on 'test-post'"

    def test_factory_creates_valid_instance(self, comment_factory):
        comment = comment_factory()
        assert isinstance(comment, Comment)
        # Add additional assertions as needed to validate the created comment instance
