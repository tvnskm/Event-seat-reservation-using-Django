# urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home_view, name='home'),  # Home page to list events
    path('events/create/', views.event_creation_view, name='event_creation'),  # Admin creates events
    path('events/<int:event_id>/seats/', views.seat_selection_view, name='seat_selection'),  # Seat selection for event
    path('events/<int:event_id>/book/', views.seat_selection_view, name='book_seat'),  # Book seat
    path('success/', views.success_view, name='success_page'),  # Success page after booking seats
    path('admin/login/', views.admin_login_view, name='admin_login'),  # Admin login
    path('seat_management/', views.seat_management_view, name='seat_management_view'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
]
