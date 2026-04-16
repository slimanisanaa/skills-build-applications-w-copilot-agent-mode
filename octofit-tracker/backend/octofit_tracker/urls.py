"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet, UserViewSet, ActivityViewSet, LeaderboardViewSet, WorkoutViewSet, api_root
import os
from rest_framework.settings import api_settings
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'users', UserViewSet, basename='user')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')



# Patch le reverse pour utiliser le bon host dynamique
@api_view(['GET'])
def api_root_custom(request, format=None):
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        host = f"https://{codespace_name}-8000.app.github.dev"
    else:
        # Utilise le host de la requête (localhost ou autre)
        host = request.build_absolute_uri('/')[:-1]
    return Response({
        'teams': host + reverse('team-list', request=request, format=format).replace('http://testserver', ''),
        'users': host + reverse('user-list', request=request, format=format).replace('http://testserver', ''),
        'activities': host + reverse('activity-list', request=request, format=format).replace('http://testserver', ''),
        'leaderboard': host + reverse('leaderboard-list', request=request, format=format).replace('http://testserver', ''),
        'workouts': host + reverse('workout-list', request=request, format=format).replace('http://testserver', ''),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root_custom, name='api-root'),
    path('api/', include(router.urls)),
]
