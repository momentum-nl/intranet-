"""Allauth-adapters: geen zelfregistratie, gebruikersnaam afleiden bij SSO."""

from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.http import HttpRequest

from apps.users.models import User


def next_available_username(*, email: str) -> str:
    base = email.split("@")[0][:140] or "gebruiker"
    candidate, n = base, 1
    while User.objects.filter(username=candidate).exists():
        n += 1
        candidate = f"{base}{n}"
    return candidate


class AccountAdapter(DefaultAccountAdapter):
    """Wachtwoordaccounts maakt alleen een beheerder aan."""

    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return False


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """SSO vanuit de Momentum-tenant maakt het account aan."""

    def is_open_for_signup(
        self, request: HttpRequest, sociallogin: SocialLogin
    ) -> bool:
        return True

    def populate_user(
        self, request: HttpRequest, sociallogin: SocialLogin, data: dict[str, Any]
    ) -> User:
        user = super().populate_user(request, sociallogin, data)
        if user.email:
            user.email = user.email.lower()
            user.username = next_available_username(email=user.email)
        return user
