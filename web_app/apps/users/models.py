from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Eigen usermodel vanaf dag één (later niet meer om te wisselen)."""

    @property
    def display_name(self) -> str:
        return self.get_full_name() or self.username
