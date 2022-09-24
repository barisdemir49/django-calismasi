#İş İlanları Tablo Yapısı

from pyexpat import model
from typing import Counter
from django.db import models
from uuid import uuid4
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Advert(models.Model):
    uuid=models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    slug=models.SlugField(
        unique=True,
        editable=False,
        max_length=150,
        null=False
    )
    title = models.CharField(
        max_length=100,
        null=False,
        verbose_name="İlan Başlığı"
    )
    content = RichTextField(
        null=False,
        verbose_name="İlan İçeriği"
    )
    createdDate=models.DateTimeField(
        auto_now_add=True,
        verbose_name="İlan Ekleme Tarihi"
    )
    
    isActive=models.BooleanField(
        default=True,
        verbose_name="İlan Yayın Durumu"
    )
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        verbose_name="İlanı Ekleyen"
    )
    tags = models.CharField(
        max_length=100,
        verbose_name="Etiketler",
        default="",
        null=True
        )

    def __str__(self) -> str:
        return self.title
    
    def createSlug(self):
        slug1 =slugify(self.title.replace('ı','İ'))
        uniqueSlug= slug1
        counter=1
        while Advert.objects.filter(slug=slug1).exists():
            uniqueSlug='{}-{}'.format(slug1,counter)
            counter+=1
        return uniqueSlug

    def save(self,*args,**kwargs):
        self.slug=self.createSlug()
        return super(Advert,self).save(*args,**kwargs)
    
    class Meta:
        ordering = ['-createdDate']


#İş arayanın başvuru yaptığı ilanlar
class RecourseAdverts(models.Model):
   author= models.ForeignKey(
    "auth.User",
    on_delete=models.CASCADE,
    verbose_name="Başvuru Yapan"
   )

   advert =models.ForeignKey(
    "Advert",
    on_delete=models.CASCADE,
    verbose_name="Başvuru Yapılan İlan"
   )
   createdDate=models.DateTimeField(
        auto_now_add=True,
        verbose_name="Başvuru  Tarihi"
   )

   class Meta:
    ordering = ['-createdDate']
    

#İş ilanı arama etiketlerim
class MyKewyords(models.Model):
   author= models.ForeignKey(
    "auth.User",
    on_delete=models.CASCADE,
    verbose_name="Kullanıcı"
   )
   keywrods=models.CharField(
    max_length=20
    )
