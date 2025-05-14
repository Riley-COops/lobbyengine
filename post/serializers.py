from rest_framework import serializers
from .models import Post, Comment, Reaction

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    is_reshared = serializers.SerializerMethodField()
    original_post_data = serializers.SerializerMethodField()

    class Meta:
        models = Post
        fields = ['id', 'author_username', 'text', 'image', 'video', 'created_at', 'updated_at', 'original_post', 'is_reshared', 'original_post_data']

    def get_is_reshare(self, obj):
        return obj.original_post is not None
    
    def get_original_post_data(self, obj):
        if obj.original_post:
            return {
                'id': obj.original_post.id,
                'text': obj.original_post.text,
                'author_username': obj.original_post.author.username,
            }
        return None


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_username', 'text', 'created_at', 'updated_at']
        read_only_fields = ['post', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    

class ReactionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Reaction
        fields = ['id', 'post', 'user_username', 'reaction_type', 'created_at']
        read_only_fields = ['user_username', 'created_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
