from django.urls import path

import web.views as views

urlpatterns = [
    path('', views.NoteListView.as_view(), name='main'),
    path('register/', views.RegistrationFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.change_password_view, name='account'),
    path('notes/new', views.NoteCreateView.as_view(), name='new_note'),
    path('notes/<int:pk>/', views.NoteEditView.as_view(), name='note'),
    path('notes/<int:pk>/delete', views.NoteDeleteView.as_view(), name='delete_note'),
    path('tags', views.TagCreateView.as_view(), name='tags'),
    path('tags/<int:pk>/', views.TagEditView.as_view(), name='tag'),
    path('tags/<int:pk>/delete', views.TagDeleteView.as_view(), name='delete_tag'),
    path('website_analytics', views.website_analytics_view, name='website_analytics'),
    path('notes/analytics', views.notes_analytics_view, name='notes_analytics'),
]
