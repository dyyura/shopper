from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=222)
    slug = models.SlugField(unique=True)

    def str(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='image', upload_to='product')
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    ip = models.CharField(max_length=50, verbose_name='ip')

    def str(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='Телефон', max_length=30)
    address = models.CharField(verbose_name='Адресс', max_length=100)


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = '=completed'
    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен'),
    )
    BUYING_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовызов'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),
    )
    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders',
                                 on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    phone = models.CharField(verbose_name='Телефон', max_length=40)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    address = models.CharField(verbose_name='Адресс доставки', max_length=100)
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_status = models.CharField(max_length=100, verbose_name='Тип заказа', choices=BUYING_CHOICES,
                                     default=BUYING_TYPE_SELF)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey('Customer', null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField('CartProduct', related_name='cart_product')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    in_order = models.BooleanField(default=False)
    anonym_user = models.BooleanField(default=False)


class CartProduct(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def str(self):
        return "Продукт: {}(Для корзины)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.product.price
        super().save(*args, **kwargs)