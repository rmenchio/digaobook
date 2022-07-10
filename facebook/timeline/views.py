from re import I
from django.shortcuts import redirect, render
from django.views import View
from usuario.models import Posts
from usuario.models import Informacoes, Solicitacoes, Amigos, Posts, Foto
from django.contrib.auth.models import User

class Timeline(View):
    template_name = 'timeline/index.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('usuario:index')
        
        self.context = {}

        # seleciona a bio do usuario
        bio = Informacoes.objects.filter(usuario=self.request.user).first()

        # busca as solicitacoes recebidas, para poder mostrar no campo solicitacoes de amizade
        solicitacoes_recebidas = Solicitacoes.objects.filter(id_usuario_solicitado=self.request.user.id)

        # busca as solicitacoes enviadas, para poder mostrar no campo convites enviados
        solicitacoes_realizadas = Solicitacoes.objects.filter(usuario=self.request.user)

        # seleciona os ids da solicitacoes enviadas, para evitar redundancia na hora de mostrar "Adicionar amigos"
        lista_ids_solicitacoes = list()
        for s in solicitacoes_realizadas:
            lista_ids_solicitacoes.append(s.id_usuario_solicitado)

        usuarios_solicitados = User.objects.filter(id__in=lista_ids_solicitacoes)

        # prepara a lista dos usuarios para exibir na aba de Adicionar amigos
        todos_os_usuarios = User.objects.exclude(id=self.request.user.id)

        # limpa da lista de adicionar amigos os amigos que voce ja enviou convite
        for s in solicitacoes_realizadas:
            todos_os_usuarios = todos_os_usuarios.exclude(id=s.id_usuario_solicitado)

        # limpa da lista de adicionar amigos os amigos que ja te enviaram um convite
        for s in solicitacoes_recebidas:
            todos_os_usuarios = todos_os_usuarios.exclude(id=s.usuario.id)

        # limpa da lista de adicionar amigos os seus proprios amigos
        lista_ids_amigos = list()
        amigos = Amigos.objects.filter(usuario=self.request.user)

        for a in amigos:
            lista_ids_amigos.append(a.id_amigo)

        for id in lista_ids_amigos:
            todos_os_usuarios = todos_os_usuarios.exclude(id=id)

        todos_os_amigos = User.objects.filter(id__in=lista_ids_amigos)

        lista_ids_amigos.append(self.request.user.id)

        posts = Posts.objects.filter(usuario__id__in=lista_ids_amigos).order_by('-data')
        meus_posts = Posts.objects.filter(usuario=self.request.user)

        avatar = Foto.objects.filter(usuario=self.request.user).first()

        self.context = {
            'usuarios': todos_os_usuarios,
            'bio': bio,
            'solicitacoes': solicitacoes_recebidas,
            'convites_pendentes': usuarios_solicitados,
            'amigos': todos_os_amigos,
            'posts': posts,
            'avatar': avatar,
            'qnt_amigos': len(todos_os_amigos),
            'qnt_posts': len(meus_posts)
        }

        return render(self.request, self.template_name, self.context)

