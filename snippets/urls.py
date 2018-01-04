########################################
#                PATTERN 1             #
########################################
# # This is serving PATTERN 1 and PATTERN 2 in the views. Basically function based vies.
# from django.conf.urls import url
# from rest_framework.urlpatterns import format_suffix_patterns
# from snippets import views
#
# urlpatterns = [
#     url(r'^snippets/$', views.snippet_list),
#     url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
# ]

#########################################
#                PATTERN 2              #
#########################################
"""
# # This is serving PATTERNS 3, 4, 5. Class based views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippets'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
"""


from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

# API endpoints
urlpatterns = format_suffix_patterns([
    #url(r'^$', views.api_root),
    url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(), name='snippet-highlight'),
    #url(r'^users/$', views.UserList.as_view(), name='user-list'),
    #url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail')
])

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
# This suffix pattern is to serve "http://127.0.0.1:8000/snippets.json" format insted of the
# automatically created http://127.0.0.1:8000/snippets/?format=json
# As PATTERN 1 doesn't support different formats this line will be useful for PATTERN 2 onwards
# in case we want .json look for our urls. It applays for all the above patterns. For each in the urlpatterns
# list it creates one more with the corresponding regex. Interesting fact is that APIView creates thoose
# additional patterns automatically probably beacose browsable api is possible.
# In other words if we are happy with "?format=json" we don't need it.
