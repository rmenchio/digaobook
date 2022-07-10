from django.urls import path

from . import views

app_name = 'usuario'

urlpatterns = [
    path('', views.Base.as_view(), name='index'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('perfil/', views.Perfil.as_view(), name='perfil'),
    path('perfil-publico/<int:id>', views.PerfilPublico.as_view(), name='perfil-publico'),
    path('alterar-bio/', views.AlterarBio.as_view(), name='alterar-bio'),

    path('solicitar-amizade/<int:id>', views.SolicitarAmizade.as_view(), name='solicitar-amizade'),
    path('aceitar-amizade/<int:id>', views.AceitarAmizade.as_view(), name='aceitar-amizade'),
    path('negar-amizade/<int:id>', views.NegarAmizade.as_view(), name='negar-amizade'),
    path('desfazer-amizade/<int:id>', views.DesfazerAmizade.as_view(), name='desfazer-amizade'),

    path('publicar/', views.Publicar.as_view(), name='publicar'),
    path('chat-privado/<int:id>', views.ChatPrivado.as_view(), name='chat-privado'),
    path('exluir-post/<int:id>', views.ExcluirPost.as_view(), name='excluir-post'),
]