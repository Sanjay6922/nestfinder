from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('reg_form/',views.register,name='reg_form'),
    path('login/',views.login,name='login'),
    path('userhome/',views.userhome, name='userhome'),
    path('logout/', views.logout, name='logout'),
    path('reviews/',views.add_review, name='add_reviews'),
    path("register_product/", views.register_product, name="register_product"),
   
    # path("rooms/", views.rooms, name="rooms"),
    # path("pg/", views.pg_list_view, name="pg"),
    # path("hostels/", views.hostels, name="hostels"),
    path("profile/", views.user_profile, name="profile"),
    
    path("edit-profile/", views.edit_profile, name="edit-profile"),
    path("delete_profile/", views.delete_profile, name="delete_profile"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("admin_home/", views.admin_home, name="admin_home"),
    path("list_users/", views.list_users, name="list_users"),
    path("delete_user/<int:id>/", views.delete_user, name="delete_user"),
    path('message/', views.message, name='message'),
    path('view_messages/', views.view_messages, name='view_messages'),
    path('verify_otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path("reply/<int:m_id>/", views.reply_message, name="reply"),
    path("user_messages/", views.user_messages, name="user_messages"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("verify_otp1/", views.verify_otp1, name="verify_otp1"),
    path("reset_password/", views.reset_password, name="reset_password"),

    path("list111/", views.list111, name="list111"),

    path("search_results/", views.search_results, name="search_results"),
    path('search_results/<str:location>/', views.search_results, name='search_results'),

    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    path('rooms/', views.rooms, name='rooms'),
    path('pg/', views.pg_list_view, name='pg'),
    path('hostels/', views.hostels, name='hostels'),
    path('toggle_hostel_wishlist/', views.toggle_hostel_wishlist, name='toggle_hostel_wishlist'),
    path('product/<int:product_id>/nearby/<str:place_type>/', views.search_nearby_places, name='search_nearby_places'),
    path('toggle_wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
    path('toggle_pg_wishlist/', views.toggle_pg_wishlist, name='toggle_pg_wishlist'),
    path('review/', views.show_reviews, name='show_reviews'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('ind/',views.userhome2,name='gg')
    
    
    
]
