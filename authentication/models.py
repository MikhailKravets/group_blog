from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Manager that helps you to filter or do some actions
    with the model
    """

    def create_user(self, email, password):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('email address'), max_length=255, unique=True)

    birth_year = models.PositiveIntegerField(null=True, blank=True,
                                             validators=[
                                                 validators.MinValueValidator(
                                                     limit_value=1900
                                                 )
                                             ])

    is_staff = models.BooleanField(default=False,
                                   help_text=_('Designates whether this user can access this admin site.'),
                                   verbose_name=_('is staff'))
    is_active = models.BooleanField(
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
        verbose_name=_('is active')
    )
    is_superuser = models.BooleanField(default=False,
                                       help_text=_('Designates that this user has all permissions without '
                                                   'explicitly assigning them.'),
                                       verbose_name=_('is superuser'))

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('date joined'))
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    def __str__(self):
        return f"{self.id}, {self.email}"

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_staff:
            return True

        # Otherwise we need to check the backends.
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Second simplest possible answer: yes, if user is staff
        return self.is_staff

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-id',)