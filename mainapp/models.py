from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

import jwt
from .Manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    # Каждому пользователю нужен понятный человеку уникальный идентификатор,
    # который мы можем использовать для предоставления User в пользовательском
    # интерфейсе. Мы так же проиндексируем этот столбец в базе данных для
    # повышения скорости поиска в дальнейшем.
    username = models.CharField(db_index=True, max_length=255, verbose_name = 'Логин', unique=True)
    first_name = models.CharField(db_index=True, verbose_name='Имя', max_length=150)
    last_name = models.CharField(db_index=True, verbose_name='Фамилия', max_length=150)
    surname = models.CharField(db_index=True, verbose_name='Отчество', max_length=150)
    email = models.EmailField(db_index=True, verbose_name='электоронная почта', unique=True)
    date_create = models.DateTimeField(auto_now_add=True)
    # Когда пользователь более не желает пользоваться нашей системой, он может
    # захотеть удалить свой аккаунт. Для нас это проблема, так как собираемые
    # нами данные очень ценны, и мы не хотим их удалять :) Мы просто предложим
    # пользователям способ деактивировать учетку вместо ее полного удаления.
    # Таким образом, они не будут отображаться на сайте, но мы все еще сможем
    # далее анализировать информацию.
    is_active = models.BooleanField(default=True)

    # Этот флаг определяет, кто может войти в административную часть нашего
    # сайта. Для большинства пользователей это флаг будет ложным.
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')

    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)

    # Дополнительный поля, необходимые Django
    # при указании кастомной модели пользователя.

    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'surname']

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    class Meta:
        ordering = ['id']
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return "{}".format(self.username)

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова Author.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class JK(models.Model):
    name = models.CharField(db_index=True, verbose_name='Тұрғын үй аты', max_length=255, unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name='ЖК'
        verbose_name_plural='ЖК'
    
    def __str__(self):
        return "{}".format(self.name)


class QrCode(models.Model):
    qr = models.CharField(db_index=True, verbose_name='QrCode данные', max_length=255)
    user = models.ForeignKey(User, verbose_name='Пользователь',blank = True,null = True, on_delete=models.CASCADE)
    id_in_electron = models.IntegerField(unique=True, verbose_name='id счетчика',)

    class Meta:
        ordering = ['-id']
        verbose_name='qr код'
        verbose_name_plural='QR кодтар'

    def __str__(self):
        return "{}".format(self.user)


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    QrCode = models.ForeignKey(QrCode,blank = True,null = True, verbose_name='Данные Qr кодов', on_delete=models.CASCADE)
    JK = models.ForeignKey(JK,null = True, verbose_name='Жк', on_delete=models.CASCADE)
    room_number =  models.CharField(db_index=True, verbose_name='Пәтер нөмірі', max_length=255, unique=True)
    
    
    class Meta:
        ordering = ['-id']
        verbose_name='профиль'
        verbose_name_plural='Профильдер'

    def __str__(self):
        return "{}".format(self.user)