from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class VoteUserManager(BaseUserManager):
    def create_user(self, username, email, password, date_of_birth, **extra_fields):
        if not username:
            raise ValueError(_('The Username must be set'))
        if not email:
            raise ValueError(_('The Email must be set'))
        if not date_of_birth:
            raise ValueError(_('The Date of birth must be set'))
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, email, password, date_of_birth, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        return self.create_user(username, email, password, date_of_birth, **extra_fields)