import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


ROLE_CHOICES = (
    (0, 'Адміністратор'),
    (1, 'Тренер'),
    (2, 'Гравець'),
)


def time_c(x):
    return int(datetime.datetime.timestamp(x))


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        print("Create custom super user")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 0)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class CustomUser(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, default='', verbose_name="Ім'я")
    last_name = models.CharField(max_length=20, default='', verbose_name="Прізвище")
    middle_name = models.CharField(max_length=20, default='', verbose_name="По батькові")
    email = models.EmailField(max_length=100, unique=True, default='', verbose_name="Email")
    password = models.CharField(max_length=200,blank=True, verbose_name="Пароль")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створений в")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлений")
    role = models.IntegerField(default=2, choices=ROLE_CHOICES, verbose_name="Роль")
    is_active = models.BooleanField(default=False, verbose_name="Є активним?")
    is_staff = models.BooleanField(default=False, verbose_name="Має доступ до адмін панелі?")
    is_superuser = models.BooleanField(default=False, verbose_name="Є суперюзером?")

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.user_id}){self.last_name if self.last_name else ''} " \
               f"{self.first_name if self.first_name else ''} " \
               f"{self.middle_name if self.middle_name else ''}" \
               f" {self.email} : {ROLE_CHOICES[self.role][1]}"

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.user_id})'

    @staticmethod
    def get_by_id(user_id):
        result = CustomUser.objects.filter(user_id=user_id).first()
        if result:
            return result
        else:
            return None

    @staticmethod
    def get_by_email(email):
        result = CustomUser.objects.filter(email=email).first()
        if result:
            return result
        else:
            return None

    @staticmethod
    def delete_by_id(user_id):
        if CustomUser.objects.filter(user_id=user_id).delete()[0] == 0:
            return False
        else:
            return True

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        if len(first_name) > 20 or len(last_name) > 20 or len(middle_name) > 20:
            return None

        all_user = CustomUser.get_all()
        for user in all_user:
            if email == user.email:
                return None

        import re
        match = re.findall(r'[a-z0-9]+@[a-z]+\.[a-z]{2,3}', email)
        if match:
            user = CustomUser(first_name=first_name, middle_name=middle_name, last_name=last_name,
                              email=email, password=password)
            user.save()
            return user
        else:
            return None

    def to_dict(self):

        result = {
            'id': self.user_id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': time_c(self.created_at),
            'updated_at': time_c(self.updated_at),
            'role': self.role,
            'is_active': self.is_active
        }

        return result

    def update(self,
               first_name=None,
               last_name=None,
               middle_name=None,
               password=None,
               role=None,
               is_active=None):

        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if middle_name:
            self.middle_name = middle_name
        if password:
            self.password = password
        if role:
            self.role = role
        if is_active:
            self.is_active = is_active

        self.save()

        return None

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    def get_role_name(self):
        result = None
        for role in ROLE_CHOICES:
            if role[0] == self.role:
                result = role[1]
        return result

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class PlayerStatistic(models.Model):
    stat_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name="player_stat", verbose_name="Гравець")
    games = models.IntegerField(null=True,default=0, verbose_name="Ігри")
    points = models.IntegerField(null=True,default=0, verbose_name="Зароблено пунктів")
    defence = models.IntegerField(null=True,default=0, verbose_name="Успішних захистів")
    year = models.IntegerField(null=False, default=int(datetime.datetime.now().year), verbose_name="Рік статистики")

    class Meta:
        verbose_name = "статистику"
        verbose_name_plural = 'Статистика'

    def __str__(self):
        return f"{self.stat_id}) {self.player.last_name if self.player.last_name else ''} " \
               f"{self.player.first_name if self.player.first_name else ''} " \
               f"{self.player.middle_name if self.player.middle_name else ''} : {self.year}"

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.stat_id})'

    @staticmethod
    def get_by_id(id):
        stat = PlayerStatistic.objects.filter(stat_id=id)[0]

        if stat:
            return stat
        else:
            raise "Статистику не знайдено"

    @staticmethod
    def delete_by_id(id):
        if PlayerStatistic.objects.filter(stat_id=id).delete()[0] == 0:
            return True
        else:
            raise "Статистику не знайдено"

    @staticmethod
    def create(player, year):
        if player and year:
            stat = PlayerStatistic(player=player, year=year)
            stat.save()

            return True
        else:
            return False

    def to_dict(self):
        return {
            "id": self.stat_id,
            "player": self.player,
            "games": self.games,
            "points": self.points,
            "defence": self.defence,
            "year": self.year,
        }

    def update(self, games=None, points=None, defence=None,year=None):
        if games:
            self.games = games

        if points:
            self.points = points

        if defence:
            self.defence = defence

        if year:
            self.year = year

        self.save()

        return None

    def add_stat(self,points,defence):
        self.games += 1
        self.points += points
        self.defence += defence

        return True

    @staticmethod
    def get_all():
        return PlayerStatistic.objects.all()

