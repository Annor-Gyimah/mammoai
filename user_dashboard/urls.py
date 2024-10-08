from django.urls import path
from user_dashboard import views
from django.contrib.auth import views as auth_view

app_name = "user_dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("records", views.records, name="records"),
    path("add_patient", views.add_patient, name="add_patient"),
    path('edit_records/<int:pk>', views.edit_records, name='edit_records'),
    path('delete_records/<int:pk>', views.delete_records, name='delete_records'),
    path("notification_mark_as_seen/<id>/", views.notification_mark_as_seen, name='notification_mark_as_seen'),
    path('search/', views.search_patient, name='search'),
    
    path("results/", views.results, name='results'),
    path('view_invoice/<int:pk>/', views.view_invoice, name='view_invoice'),
    
    # path("bookmark/", views.bookmark, name='bookmark'),
    # path("delete_bookmark/<bid>/", views.delete_bookmark, name="delete_bookmark"),
    # path("add_to_bookmark/", views.add_to_bookmark, name='add_to_bookmark'),

    # path("book/", views.book, name="book"),
    # path("delete_book/<bkid>/", views.delete_book, name="delete_book"),
    # path("add_to_book/", views.add_to_book, name="add_to_book"),
    
    
    # path("change-password/", views.password_change, name='change_password'),
    # path("password-changed/", views.password_changed, name="password_changed"),
    # path("add_review/", views.add_review, name="add_review")

    # path("change-password/", 
    #     auth_view.PasswordChangeView.as_view(template_name="user_dashboard/password-reset/change-password.html", 
    #     success_url='/dashboard/password-changed/'), name="change_password"),




]