from main_app import views
from django.urls import path
urlpatterns = [
    path('',views.index,name='index'),
    path('todo',views.to_do_list,name='to_do_list'),
    path(r'todo/del/<item_id>',views.remove_item,name='del'),

]
