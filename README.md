# Momentum intranet

Handige links, notificaties, pin of shame (meeste rode merges van de maand), corvee met rating, en picnic-voorkeuren. Django, zelfde opzet als de andere Momentum-apps.

## Draaien

```bash
uv sync
cp .env.example .env.local
cd web_app && npm install && npm run build
uv run --env-file=../.env.local python manage.py migrate
uv run --env-file=../.env.local python manage.py createsuperuser
uv run --env-file=../.env.local python manage.py seed_demo   # optioneel: demodata
uv run --env-file=../.env.local python manage.py runserver
```

Beheer (links, notificaties, rode merges, corvee-planning) via `/admin/`.

## Tests

```bash
uv run pytest
```

## Branches

`main` is productie, `develop` is integratie. Feature-branches gaan via PR naar `develop`.

## Nog niet

- Entra SSO (nu Django-login). Zie vesting-werkbon-review voor de allauth-opzet.
- Rode merges komen handmatig binnen via Beheer; een GitHub-webhook kan dat later vullen.
