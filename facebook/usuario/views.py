from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Amigos, Informacoes, MensagemPrivada, Solicitacoes, Posts, Foto
from django.contrib import messages
from django import forms
from datetime import datetime

from . import models
from . import forms

class MiddlewareLogin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('usuario:index')
        return super().dispatch(*args,**kwargs)
    

class Base(View):
    template_name = 'usuario/index.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        if not self.request.user.is_authenticated:
            self.context = {
                'userform': forms.CreateUserForm(
                    data=self.request.POST or None
                    ),
                'loginform': forms.LoginForm(
                    data=self.request.POST or None
                    ),
            }

            self.userform = self.context['userform']

            self.render = render(self.request, self.template_name, self.context)
        else:
            render(self.request, self.template_name)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('timeline:index')
        else:
            return self.render

class SignIn(View):
    def post(self, *args, **kwargs):
        self.form = forms.CreateUserForm(data=self.request.POST or None)
        sem_erro = True

        if self.form.is_valid():
            username = self.form.cleaned_data.get('username')
            password = self.form.cleaned_data.get('password')
            password2 = self.form.cleaned_data.get('password2')
            email = self.form.cleaned_data.get('email')

            usuario_db = User.objects.filter(username=username).first()
            email_db = User.objects.filter(email=email).first()

            if usuario_db:
                messages.error(
                    self.request,
                    "Esse usuário já está cadastrado!"
                    )
                sem_erro = False
            if email_db:
                messages.error(
                    self.request,
                    "Esse email já está cadastrado!"
                    )
                sem_erro = False
            if password != password2:
                messages.error(
                    self.request,
                    "As senhas não conferem!"
                    )
                sem_erro = False

            if sem_erro:
                novo_usuario = self.form.save(commit=False)
                novo_usuario.set_password(password)
                novo_usuario.save()
                login(self.request, user=novo_usuario)

        return redirect('usuario:index')


class Login(View):
    def post(self, *args, **kwargs):
        self.form = forms.LoginForm(data=self.request.POST or None)

        if self.form.is_valid():
            
            username = self.form.cleaned_data.get('username')
            password = self.form.cleaned_data.get('password')

            user_db = User.objects.filter(username=username).first()

            if user_db:
                autenticado = authenticate(self.request, username=user_db, password=password)
                
                if autenticado:
                    login(self.request, user=user_db)
                else:
                    messages.error(
                    self.request,
                    "Senha incorreta"
                    )
            else:
                messages.error(
                self.request,
                "Usuário não existe"
                )

        return redirect('usuario:index')

class Logout(MiddlewareLogin, View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('usuario:index')

class Perfil(MiddlewareLogin, View):
    template_name = 'usuario/perfil.html'
    def get(self, *args, **kwargs):
        self.context = {}

        self.context['bio'] = Informacoes.objects.filter(usuario=self.request.user).first()
        self.context['meus_posts'] = Posts.objects.filter(usuario__id=self.request.user.id)
        self.context['avatar'] = Foto.objects.filter(usuario=self.request.user).first()
        self.context['qnt_posts'] = len(self.context['meus_posts'])

        amigos = Amigos.objects.filter(usuario=self.request.user)
        lista_ids_amigos = list()
        for a in amigos:
            lista_ids_amigos.append(a.id_amigo)
        amigos = User.objects.filter(id__in=lista_ids_amigos)

        self.context['amigos'] = amigos
        self.context['qnt_amigos'] = len(amigos)

        return render(self.request, self.template_name, self.context)

class PerfilPublico(MiddlewareLogin, View):
    template_name = 'usuario/perfil-publico.html'
    def get(self, *args, **kwargs):
        id_usuario = kwargs['id']
        if id_usuario == self.request.user.id:
            return redirect('usuario:perfil')
        else:

            self.context = {}

            self.context['bio'] = Informacoes.objects.filter(usuario__id=id_usuario).first()
            self.context['usuario'] = User.objects.filter(id=id_usuario).first()
            self.context['posts'] = Posts.objects.filter(usuario__id=id_usuario)
            self.context['avatar'] = Foto.objects.filter(usuario__id=id_usuario).first()
            self.context['qnt_posts'] = len(self.context['posts'])

            amigos = Amigos.objects.filter(usuario__id=id_usuario)
            lista_ids_amigos = list()
            for a in amigos:
                lista_ids_amigos.append(a.id_amigo)
            amigos = User.objects.filter(id__in=lista_ids_amigos)

            self.context['amigos'] = amigos
            self.context['qnt_amigos'] = len(amigos)

            return render(self.request, self.template_name, self.context)

class AlterarBio(MiddlewareLogin, View):
    def post(self, *args, **kwargs):
        status = self.request.POST["status"]
        localizacao = self.request.POST["localizacao"]

        if 'foto-perfil' in self.request.FILES.keys():
            foto_existe = Foto.objects.filter(usuario=self.request.user).first()

            if foto_existe != None:
                foto_existe.foto = self.request.FILES['foto-perfil']
                foto_existe.save()
            else:
                novo_avatar = Foto.objects.create(usuario=self.request.user, foto=self.request.FILES['foto-perfil'])

        info = Informacoes.objects.filter(usuario=self.request.user).first()

        if not info:
            info = Informacoes.objects.create(status=status, localizacao=localizacao, usuario=self.request.user)
        else:
            if status != "":
                info.status = status
            if localizacao != "":
                info.localizacao = localizacao
            info.save()


        return redirect('usuario:perfil')

class SolicitarAmizade(MiddlewareLogin, View):
    def get(self, *args, **kwargs):
        id_usuario = kwargs['id']
        solicitacao = Solicitacoes.objects.create(usuario=self.request.user, id_usuario_solicitado=id_usuario)
        return redirect('timeline:index')

class AceitarAmizade(MiddlewareLogin, View):
    def get(self, *args, **kwargs):
        id_usuario = kwargs['id']

        usuario_adicionado = User.objects.filter(id=id_usuario).first()

        Amigos.objects.create(usuario=self.request.user, id_amigo=id_usuario)
        Amigos.objects.create(usuario=usuario_adicionado, id_amigo=self.request.user.id)

        solicitacao = Solicitacoes.objects.filter(usuario=usuario_adicionado, id_usuario_solicitado=self.request.user.id)
        solicitacao.delete()
        
        return redirect('timeline:index')

class NegarAmizade(MiddlewareLogin, View):
    def get(self, *args, **kwargs):
        id_usuario = kwargs['id']

        usuario_adicionado = User.objects.filter(id=id_usuario).first()

        solicitacao = Solicitacoes.objects.filter(usuario=usuario_adicionado, id_usuario_solicitado=self.request.user.id).first()
        solicitacao.delete()
        
        return redirect('timeline:index')

class DesfazerAmizade(MiddlewareLogin, View):
    def get(self, *args, **kwargs):
        id_usuario = kwargs['id']

        amigo = User.objects.filter(id=id_usuario).first()

        amizade = Amigos.objects.filter(usuario=self.request.user, id_amigo=id_usuario).first()
        amizade_mutua = Amigos.objects.filter(usuario=amigo, id_amigo=self.request.user.id).first()

        amizade.delete()
        amizade_mutua.delete()
        
        return redirect('timeline:index')

class Publicar(MiddlewareLogin, View):
    def post(self, *args, **kwargs):
        texto = self.request.POST["texto"]

        now = datetime.now()

        post = Posts.objects.create(texto=texto, data=now, usuario=self.request.user)

        return redirect('timeline:index')

class ExcluirPost(MiddlewareLogin, View):
    def get(self, *args, **kwargs):
        id = kwargs['id']

        post = Posts.objects.filter(id=id).first()
        post.delete()

        return redirect('timeline:index')


class ChatPrivado(MiddlewareLogin, View):
    template_name = 'usuario/chat-privado.html'

    def get(self, *args, **kwargs):
        id = kwargs['id']

        self.context = dict()

        amigo = User.objects.filter(pk=id).first()

        self.context['minha_bio'] = Informacoes.objects.filter(usuario=self.request.user).first()
        self.context['meu_avatar'] = Foto.objects.filter(usuario=self.request.user).first()

        self.context['amigo'] = amigo
        self.context['bio_amigo'] = Informacoes.objects.filter(usuario=amigo).first()
        self.context['avatar_amigo'] = Foto.objects.filter(usuario=amigo).first()

        self.context['mensagens'] = MensagemPrivada.objects.filter(
            remetente=self.request.user, destinatario=amigo
            ).union(
                MensagemPrivada.objects.filter(destinatario=self.request.user)
                ).order_by('-data')

        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        id_amigo = kwargs['id']
        amigo = User.objects.filter(pk=id_amigo).first()

        mensagem = self.request.POST["mensagem"]

        mensagem_privada = MensagemPrivada.objects.create(
            remetente=self.request.user,
            destinatario=amigo,
            texto=mensagem,
            data=datetime.now()
        )

        return redirect('usuario:chat-privado', id=int(id_amigo))