"""
URL configuration for crime_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from crime.views import (
    LoginView, RegisterView, IdentityBindView, UserProfileView,
    CrimeEventViewSet, ResidentViewSet, ClueViewSet, CaseProgressViewSet,
    SearchViewSet
)

router = DefaultRouter()
router.register(r'crime-events', CrimeEventViewSet, basename='crime-event')
router.register(r'residents', ResidentViewSet, basename='resident')
router.register(r'clues', ClueViewSet, basename='clue')
router.register(r'case-progress', CaseProgressViewSet, basename='case-progress')
router.register(r'search', SearchViewSet, basename='search')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # 用户认证接口
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/bind-identity/', IdentityBindView.as_view(), name='bind-identity'),
    path('api/auth/profile/', UserProfileView.as_view(), name='user-profile'),
    # 特殊接口
    path('crime-events/<int:pk>/clues/', ClueViewSet.as_view({'get': 'clues_for_event'}), name='clues-for-event'),
    path('crime-events/<int:pk>/progress/', CaseProgressViewSet.as_view({'get': 'progress_for_event'}), name='progress-for-event'),
    # 其他接口
    #path('stats/crime-trend/', CrimeTrendStatsView.as_view(), name='crime-trend'),
    #path('stats/crime-hotspots/', CrimeHotspotsView.as_view(), name='crime-hotspots')
]

'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/latterns/',views.funlan),
    path('api/latterns/<str:keyword>/', views.search_latterns, name='search_latterns'),
    path('api/users/',views.funuser),Evidence
    path('api/users/<int:uid>/', views.get_specific_user, name='get_specific_user'),
    # path('tijiao/',views.tijiao),
    # path('login/',views.login),
]'''