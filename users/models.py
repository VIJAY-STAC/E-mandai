from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

USER_TYPES = (
    ("admin", "Admin"),
    ("supervisor", "Supervisor"),
    ("customer", "Customer"),
    ("seller", "Seller"),
    ("rider", "Rider" )
)

class UserManager(BaseUserManager):
    def create_user(self, email, name , tc, date_of_birth, phone_number , user_type , address, pincode , city, country, password=None, password2=None):
        """
        Creates and saves a User with the given email,name , tc , date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name =name,
            date_of_birth= date_of_birth,
            phone_number = phone_number,
            user_type = user_type,
            address = address,
            pincode = pincode,
            city = city, 
            country = country,
            tc = tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name , tc, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name = name,
            tc = tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    date_of_birth = models.DateField(null=False, blank=False )
    phone_number = PhoneNumberField(blank=True, null=True)
    user_type = models.CharField(
        null=False, blank=False, max_length=32, choices=USER_TYPES,
    )
    address = models.CharField(max_length=1000, null=False, blank=False )
    pincode = models.CharField(max_length=255, null=False, blank=False)
    city = models.CharField(max_length=255, null=False, blank=False )
    country = models.CharField(max_length=255, null=False, blank=False )


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'tc']


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
