from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'users', views.ReadOnlyUserViewSet)

urlpatterns = [
    url(r'^users/', include(router.urls)),
    url(r'^accounts/signup/$', views.UserSignUpView.as_view(), name='user-signup'),
    url(r'^accounts/profile/$', views.MyUserView.as_view(), name='my-user-view'),
]