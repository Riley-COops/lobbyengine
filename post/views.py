from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Comment, Reaction, Follow
from .serializers import PostSerializer, CommentSerializer, ReactionSerializer

class MyFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        posts = Post.objects.filter(author_in=followed_users).select_related('author', 'original_post').order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'original_post').all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['text', 'author__email']
    ordering_fields = ['created_at', 'updated_at']


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReactionView(viewsets.ModelViewSet):
    queryset = Reaction.objects.select_related('user', 'post').all()
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ResharePostView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            original_post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        text = request.data.get('text', '')

        reshared_post = Post.objects.create(
            author=request.user,
            text=text,
            original_post=original_post
        )

        return Response({"details": "Post reshared successfully", "post_id": reshared_post.id}, status=status.HTTP_201_CREATED)