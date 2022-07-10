import os
from pickletools import optimize
from PIL import Image
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Foto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    foto = models.ImageField(
        upload_to='fotos/', blank=True, null=True
    )

    @staticmethod
    def resize_image(img):
        full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(full_path)
        ow, oh = img_pil.size

        nh = (1500 * oh) / ow

        imagem = img_pil.resize((1500, int(nh)), Image.LANCZOS)
        imagem.save(
            full_path,
            optimize=False,
            quality=100
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.foto:
            self.resize_image(self.foto)

class Informacoes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=300)
    localizacao = models.CharField(max_length=300)

class Solicitacoes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_usuario_solicitado = models.IntegerField()

class Amigos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_amigo = models.IntegerField()

class Posts(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.CharField(max_length=300)
    data = models.DateTimeField()

class MensagemPrivada(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="destinatario")
    texto = models.CharField(max_length=300)
    data = models.DateTimeField()