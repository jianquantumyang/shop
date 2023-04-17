from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class CUser(AbstractUser):
    regis_data = models.DateField(auto_now=True,verbose_name="Дата создания")
    face = models.ImageField(verbose_name="Аватар",upload_to="avatars/%Y/%m/%d/")
    about = models.TextField(verbose_name="О себе")
    country = models.CharField(max_length=128)
    geo_position = models.CharField(max_length=300,verbose_name="Адрес пользователья")
    def __str__(self):
        return self.username



class Category(models.Model):
    category_img = models.ImageField(upload_to='category/img/%Y/%m/%d/')
    name = models.CharField(max_length=100,verbose_name="Категория",db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Pod_Category(models.Model):
    category_img = models.ImageField(upload_to='pod_category/img/%Y/%m/%d/')

    name = models.CharField(max_length=100,verbose_name="Под Категория",db_index=True)
    category_roditel = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name="Категорий родитель")
    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = "Под Категория"
        verbose_name_plural = "Под Категории"

class Product(models.Model):
    name = models.CharField(max_length=255,verbose_name="Товар")
    about = models.TextField(verbose_name="О товаре")

    rating = models.IntegerField(verbose_name="Рейтинг",null=True,blank=True,default=0)
    
    gender_choices = (("Мужчина","Мужчина"),
                      ("Женщина","Женщина"),
                      ("Всем","Всем"),)


    gender = models.CharField(max_length=20,verbose_name="Пол",choices=gender_choices)

    img1 = models.ImageField(verbose_name="Картинка для товара 1",upload_to="product/1/%m/%d/")
    img2 = models.ImageField(blank=True,null=True,verbose_name="Картинка для товара 2",upload_to="product/2/%m/%d/")
    img3 = models.ImageField(blank=True,null=True,verbose_name="Картинка для товара 3",upload_to="product/3/%m/%d/")
    img4 = models.ImageField(blank=True,null=True,verbose_name="Картинка для товара 4",upload_to="product/4/%m/%d/")
    img5 = models.ImageField(blank=True,null=True,verbose_name="Картинка для товара 5",upload_to="product/5/%m/%d/")

    
    are_available = models.BooleanField(verbose_name="Есть в наличии?")
    price = models.IntegerField(verbose_name="Цена в ₸")
    category = models.ForeignKey(Category,on_delete=models.PROTECT,verbose_name="Категория продукта")
    pod_category = models.ForeignKey(Pod_Category,on_delete=models.PROTECT,verbose_name="Под Категория продукта")
    def __str__(self):
        return self.name
    
    class Meta:
        
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class RatingProduct(models.Model):
    
    author = models.ForeignKey(CUser,on_delete=models.PROTECT)
    text = models.TextField(verbose_name="Комментарий к товару",null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    rating = models.IntegerField(default=1,verbose_name="Оценка товару",blank=True,null=True,validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    def __str__(self):
        return self.author.username + " | " + self.product.name
    class Meta:
        verbose_name = "Рейтинг продукта"
        verbose_name_plural = "Рейтинг продуктов"


class Zakaz(models.Model):
    count = models.IntegerField(verbose_name="Сколько продуктов",default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    zakazatel = models.ForeignKey(CUser,verbose_name="Заказавший", on_delete=models.CASCADE)
    product_zakaz = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name="Продукт")
    time_zakaz = models.DateField(auto_now=True,verbose_name="Время заказа")
   
    def __str__(self):
        return self.product_zakaz.name
   
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["time_zakaz"]