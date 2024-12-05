from django.urls import path
from . import views

urlpatterns = [
    # User Authentication URLs
    path('', views.user_login, name='user_login'), 
    path('register/', views.register, name='register'),  
    path('login/', views.user_login, name='login'),      
    path('logout/', views.user_logout, name='logout'), 

    path('dashboard/', views.dashboard, name='dashboard'),
    path('folder_detail/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    
    path('create_folder/', views.create_folder, name='create_folder'),

    path('upload_file/<int:folder_id>/', views.upload_file, name='upload_file'),
    path('upload_file_root/', views.upload_file_root, name='upload_file_root'),

    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete_root_file/<int:fileid>/', views.delete_root_file, name='delete_root_file'),
    
    path('folder/create/', views.create_folder, name='create_folder'),
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    path('folder/<int:folder_id>/create/', views.create_folder, name='create_folder_in_subfolder'),

    path('folder/delete/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('folder/<int:folder_id>/create_subfolder/', views.create_subfolder, name='create_subfolder'),
    path('file/create/<int:folder_id>/', views.create_file, name='create_file'),

]
