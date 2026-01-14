from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, full_name, role, password=None):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, role="HR", password=None):
        user = self.create_user(email, full_name, role, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
