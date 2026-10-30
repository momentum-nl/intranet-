from django.db import migrations

LINKS = [
    ("Factory", "https://factory.momentumdigital.nl/", "Tools", 0),
    ("Productive · Planning", "https://app.productive.io/52169-momentum/scheduling/", "Tools", 1),
]


def seed(apps, schema_editor):
    Link = apps.get_model("intranet", "Link")
    for title, url, category, order in LINKS:
        Link.objects.get_or_create(url=url, defaults={"title": title, "category": category, "order": order})


class Migration(migrations.Migration):
    dependencies = [("intranet", "0002_initial")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
