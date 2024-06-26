from django.urls import path, include

urlpatterns = [
    # path('blog/', include(('bubook.blog.urls', 'blog')))
    path('user/', include(('bubook.users.urls', 'user'))),
    path('authentication/', include(('bubook.authentication.urls', 'authentication'))),
]
