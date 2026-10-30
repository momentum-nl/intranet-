from django.conf import settings


def sso(request) -> dict[str, bool]:
    return {"sso_enabled": bool(settings.AZURE_AD_SSO_CLIENT_ID)}
