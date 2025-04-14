from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from job.models import Job
from poll.models import Poll
from story.models import Story
from user_account.models import User
from ..permissions import OwnerPermission, AdminPermission, NotAllowed
from ..serializers import JobSerializer, UserSerializer, PollSerializer, StorySerializer


class ViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        pass

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [NotAllowed]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [OwnerPermission, IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()


class JobViewSet(ViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class StoryViewSet(ViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


class PollViewSet(ViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class UserViewSet(ViewSet):
    queryset = User.objects.filter(is_staff=False, is_superuser=False)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser, AdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [OwnerPermission, IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in self.permission_classes]


class ShowStoryList(ListAPIView):
    queryset = Story.objects.filter(title__startswith='Show HN:')
    serializer_class = StorySerializer


class AskStoryList(ListAPIView):
    queryset = Story.objects.filter(title__startswith='Ask HN:')
    serializer_class = StorySerializer
