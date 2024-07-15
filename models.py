# JJJs/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom manager for User model
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            phone_number,
            password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom user model
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

    

# Model for Area
class Area(models.Model):
    name = models.CharField(max_length=100)
    # hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name




# Model for Hostel
class Hostel(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Area, on_delete=models.CASCADE)
    number_of_rooms = models.IntegerField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner_contact = models.CharField(max_length=100)

    def __str__(self):
        return self.name



# Model for Booking
class Booking(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateField()

    def __str__(self):
        return f'Booking for {self.hostel.name} by {self.user.email}'
