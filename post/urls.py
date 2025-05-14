from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResharePostView, PostView, ReactionView, CommentView,MyFeedView

router = DefaultRouter()
router.register(r'posts', PostView, basename='post')
router.register(r'comments', PostView, basename='comment')
router.register(r'reactions', PostView, basename='reaction')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/my-feed/', MyFeedView.as_view(), name='my-feed'),
    path('posts/<int:post_id>/reshare/', ResharePostView, name='reshare-post')
]