from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),   
    path('catalog/', views.catalog, name='catalog'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.search_view, name='search'),
    path('book/<int:book_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('book/<int:book_id>/preview/<int:page_number>/', views.book_preview_view, name='book_preview'),
    path('upload/', views.upload_book, name='upload_book'),
    path("book/edit/<int:book_id>/", views.edit_book, name="edit_book"),
    path("book/<int:book_id>/delete/", views.delete_book, name="delete_book"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path("favorites/", views.favorite_books_view, name="favorite_books"),






]
