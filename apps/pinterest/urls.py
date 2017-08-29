from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/$', views.index),
    url(r'^pins/$', views.pin_index, name='pin_index'),
    url(r'^pins/create/$', views.create_pin, name='create'),
    url(r'^pins/(?P<id>\d+)$', views.show_pin, name='show_pin'),
    url(r'^pins/(?P<id>)/edit/$', views.edit_pin),
    url(r'^pins/user/$', views.user_show, name='user_show'),
    url(r'^pins/user/(?P<id>\d+)$', views.user_show_info, name='user_show_info'),
    url(r'^pins/logout$', views.logout, name='logout'),
    url(r'^pins/user/user_pins/$', views.show_user_pins, name='show_user_pins'),
    url(r'^pins/user/user_pins/(?P<id>\d+)$', views.show_another_user_pins, name='show_another_user_pins'),
    url(r'^boards/create/$', views.create_board, name='create_board'),
    url(r'^boards/$', views.board_index, name='board_index'),
    url(r'^pins/create_topic/$', views.create_topic, name="create_topic"),
    url(r'^pins/search$', views.search, name="search"),
    url(r'^pins/add/(?P<id>\d+)', views.add_pin, name="add_pin"),
    url(r'^pins/delete/(?P<id>\d+)', views.unpin, name="unpin"),
    url(r'^pins/follow/(?P<id>\d+)', views.follow, name="follow"),
    url(r'^pins/unfollow/(?P<id>\d+)', views.unfollow, name="unfollow"),
    url(r'^pins/comment/create', views.create_comment, name="create_comment"),
    url(r'^pins/comment/delete/(?P<id>\d+)/(?P<pin_id>\d+)', views.delete_comment, name="delete_comment"),
    url(r'^boards/(?P<id>\d+)$', views.show_board, name='show_board'),
    url(r'^boards/edit/(?P<id>\d+)$', views.edit_board, name='edit_board'),
    url(r'^boards/(?P<id>\d+)/add_pin$', views.board_add_pin, name='board_add_pin'),
    url(r'^boards/(?P<id>\d+)/unpin/(?P<board_id>\d+)$', views.unpin_from_board, name='unpin_from_board'),
    url(r'^pins/switch_to_pin$', views.switch_to_pin, name='switch_to_pin'),
    url(r'^boards/(?P<id>\d+)/edit$', views.edit_board, name='edit_board'),
    url(r'^boards/user/(?P<id>\d+)$', views.show_another_user_boards, name='show_another_user_boards'),
    url(r'^boards/view/(?P<id>\d+)$', views.view_board, name='view_board'),
    # url(r'^boards/(?P<id>)/delete/$', views.delete_board)
]