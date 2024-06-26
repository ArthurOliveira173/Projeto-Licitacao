from django.urls import path
from . import views

urlpatterns = [
    path('', views.textEditor, name="editor"),

    #PDF & WORD
    # path('index/', views.index, name='index'),
    # path('save/', views.save, name='save'),

    #PDF CANVAS
    # path('view-pdf/', views.view_pdf, name='view_pdf'),

    path('upload/', views.upload, name='upload'),
    path('edit/<int:document_id>/', views.edit, name='edit'),
    path('delete/<int:document_id>/', views.delete, name='delete'),
    path('list/', views.list, name='list'),
    path('detail/<int:document_id>/', views.detail, name='detail'),
    path('download/<int:document_id>/', views.download, name='download'),

]
