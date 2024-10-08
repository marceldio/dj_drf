from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from lms.models import Course, Lesson


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Мы не используем поле username
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=15, verbose_name="Телефон", blank=True, null=True
    )
    city = models.CharField(max_length=100, verbose_name="Город", blank=True, null=True)
    avatar = models.ImageField(
        upload_to="users/avatars", blank=True, null=True, verbose_name="Аватар"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    token = models.CharField(
        max_length=255, verbose_name="Токен", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Только email и пароль

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course,
        verbose_name="Оплаченный курс",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        verbose_name="Оплаченный урок",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHODS, verbose_name="Способ оплаты"
    )
    currency = models.CharField(max_length=10, default="usd", verbose_name="Валюта")
    stripe_session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="ID сессии Stripe"
    )
    stripe_payment_status = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Статус платежа"
    )
    link = models.URLField(
        max_length=400, blank=True, null=True, verbose_name="Ссылка на оплату"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        if self.paid_course:
            return f"Payment for course '{self.paid_course}' by {self.user} on {self.payment_date}"
        elif self.paid_lesson:
            return f"Payment for lesson '{self.paid_lesson}' by {self.user} on {self.payment_date}"
        return f"Payment by {self.user} on {self.payment_date}"
