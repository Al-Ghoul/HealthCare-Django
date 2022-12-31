from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainView, name='Home'),
    path('symptomsearch/', views.SymptomsSearchView, name='SymptomsSearchView'),
    path('symptomselection/', views.SymptomsSelectionView, name='SymptomsSelectionView'),
    path('symptomanalyze/', views.SymptomsAnalyzeView, name='SymptomsAnalyzeView'),
    path('question/<answer>', views.QuestionsView, name='QuestionsView'),
    path('results/', views.ResultsView, name='ResultsView'),
]
