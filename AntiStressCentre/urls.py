from django.urls import path

from . import views
from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from django.views.generic.base import TemplateView

from .views import HomeView
from .views import MyDiscussionsView
from .views import CreatePost
from .views import PostsDetailView
from .views import DeletePost
from .views import HomeSort
from .views import ReplyPost
from .views import HelpView
from AntiStressCentre import views


logged_users_redirect = user_passes_test(lambda u: u.is_anonymous, "/")

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/<str:sorting>/', HomeSort.as_view(), name='home-sort'),
    path("posts/mydiscussions/<str:username>/", MyDiscussionsView.as_view(), name="my-discussions-view"),
    path("posts/create/input_details/", CreatePost.as_view(), name="create-post-view"),
    path("posts/<int:pk_post>/", PostsDetailView.as_view(), name="posts-detail-view"),
    path("posts/delete/<int:pk_post>/", DeletePost.as_view(), name="posts-delete"),
    path("posts/upvote/", views.upvote, name="upvote"),
    path("posts/downvote/", views.downvote, name="downvote"),
    path("posts/reply/<int:pk_post>/", ReplyPost.as_view(), name="reply-post-view"),
    path("help/", HelpView.as_view(), name="help-view"),

]