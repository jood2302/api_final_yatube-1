from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from posts.models import Comment, Follow, Group, Post, User
from .serializers import CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer

API_RAISE_403 = PermissionDenied('Изменение чужого контента запрещено!')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise API_RAISE_403
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise API_RAISE_403
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise API_RAISE_403
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise API_RAISE_403
        instance.delete()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username',)

    def get_queryset(self):
        follower = get_object_or_404(User, pk=self.request.user.id)
        new_queryset = follower.follower.all()
        # Follow.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, request):
        serializer = FollowSerializer(data=request.data)
        
        follower = User.objects.get(pk=self.request.user.id)
        print('follower', follower)        

        follow_obj = serializer.initial_data.get('following')
        print('follow_obj', follow_obj)
        following = User.objects.get(username=follow_obj)
        if follower == following:
            raise ParseError(
                detail=(
                    'Неверные данные для создания подписки: '
                    f'Подписчик: "{follower.username}" | '
                    f'Объект подписки: "{follow_obj}" '
                    'Подписка на самого себя запрещена.'
                )
            )
        elif Follow.objects.filter(
            user=follower, following=following
        ).exists():
            raise ParseError(
                detail=(
                    'Неверные данные для создания подписки: '
                    f'Подписчик: "{follower.username}" | '
                    f'Объект подписки: "{follow_obj}" '
                    'Такая одписка уже существует.'
                )
            )
        elif serializer.is_valid():
            serializer.save(user=follower)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""    def perform_create(self, request):
        serializer = FollowSerializer(data=request.data)
        user = self.request.user
        follow_obj = serializer.initial_data.get('following')

        if user.username == follow_obj:
            raise PermissionDenied(
                'Неверные данные для создания подписки: '
                f'Подписчик: "{user.username}" | '
                f'Объект подписки: "{follow_obj}" '
                'Подписка на самого себя запрещена.'
            )
        elif Follow.objects.filter(
            user=user,
            following=User.objects.get(username=follow_obj)
        ).exists():
            raise PermissionDenied(
                'Неверные данные для создания подписки: '
                f'Подписчик: "{user.username}" | '
                f'Объект подписки: "{follow_obj}" '
                'Такая одписка уже существует.'
            )
        elif serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""

"""def list(self, request):
        queryset = Follow.objects.filter(user=self.request.user)
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)
"""
