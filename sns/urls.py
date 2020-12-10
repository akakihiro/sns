from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name='sns'
urlpatterns=[
    path('',views.index,name='index'),
    path('<int:page>',views.index,name='index'),
    path('groups',views.groups,name='groups'),
    path('add',views.add,name='add'),
    path('creategroup',views.creategroup,name='creategroup'),
    path('post',views.post,name='post'),
    path('share/<int:share_id>',views.share,name='share'),
    path('good/<int:good_id>',views.good,name='good'),
    path('entry',views.entry,name='entry'),
    path('login', auth_views.LoginView.as_view(\
    template_name="sns/login.html"), name='login'),
]