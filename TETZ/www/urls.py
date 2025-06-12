from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new-employees/', views.new_employees, name='new_employees'),
    path('jubilees/', views.jubilees, name='jubilees'),
    path('lean-production/', views.lean_production, name='lean_production'),
    path('requests/', views.requests_view, name='requests'),
    path('download-ppu/<int:proposal_id>/', views.download_ppu, name='download_ppu'),
    path('visualization/', views.VisualizationView.as_view(), name='visualization'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('visualization_data/<int:file_id>/', views.visualization_data, name='visualization_data'),
    path('save_visualization/', views.save_visualization, name='save_visualization'),
    path('load_visualization/<int:viz_id>/', views.load_visualization, name='load_visualization'),
    path('delete_visualization/<int:viz_id>/', views.delete_visualization, name='delete_visualization'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('download-file/<int:file_id>/', views.download_file, name='download_file'),
    path('improvement-proposals/', views.improvement_proposals, name='improvement_proposals'),
    path('generate-ppu/<int:proposal_id>/', views.generate_ppu_document, name='generate_ppu_document'),
    # Аутентификация
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]