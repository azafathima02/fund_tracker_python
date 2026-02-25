from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Add Transaction Page
    path('add/', views.add_transaction, name='add_transaction'),

    # All Transactions Page
    path('transactions/', views.all_transactions, name='transactions'),

    path('delete/<int:id>/', views.delete_transaction, name='delete_transaction'),

    path('export-transactions-pdf/', views.export_transactions_pdf, name='export-transactions-pdf'),

    path('export-monthly-pdf/<int:month>/<int:year>/', views.export_monthly_pdf, name='export_monthly_pdf'),
    
    path('transactions/', views.all_transactions, name='all_transactions'),
    ]