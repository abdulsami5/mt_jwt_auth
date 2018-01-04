from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from . import views


# router = DefaultRouter()
# router.register(r'users', views.ReadOnlyUserViewSet)

urlpatterns = [
    # url(r'^users/', include(router.urls)),
    url(r'^login/$', views.UserLoginView.as_view(), name='user-login'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name='user-logout'),
    url(r'^obtain-jwt/$', views.ObtainJSONWebToken.as_view(), name='obtain-jwt'),
    # url(r'^profile/$', views.MyUserView.as_view(), name='my-user-view'),
    url(r'^test-authentication-view', views.TestJWTAuthenticationView.as_view(), name='test-authentication-view'),
    url(r'^test-permission-view', views.TestJWTPermissionView.as_view(), name='test-permission-view')
]
