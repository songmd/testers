from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^snippets/$', views.snippet_list),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),

]

urlpatterns2 = [
url(r'^$', views.api_root),
url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)$', views.SnippetDetail.as_view()),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    url(r'^shops/$', views.ShopInfoList.as_view()),
    url(r'^shops/(?P<pk>[\w]+)$', views.ShopInfoDetail.as_view()),

    # url(r'^products(?:/shop_id/(?P<shop_id>[-\w]+))?/$', views.ProductList.as_view()),
    url(r'^products/$', views.ProductList.as_view()),
    url(r'^basket/(?P<pk>[\w]+)$', views.BasketView.as_view()),
    url(r'^basketunits/(?P<user_token>[\w]+)/$', views.BasketUnitView.as_view()),
    url(r'^basketunits/(?P<user_token>[\w]+)/(?P<pk>[\w]+)/$', views.BasketUnitDeleteView.as_view()),
    # url(r'^products/(?P<pk>[\w]+)$', views.P.as_view()),

    url(r'login/$',views.customer_login,name='customer_login')

]

urlpatterns += format_suffix_patterns(urlpatterns2)
