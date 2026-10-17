from django.db import migrations

CATEGORIES = ["Streetlight", "Water", "Garbage Collection", "Roads", "Drainage"]


def add_categories(apps, schema_editor):
    Category = apps.get_model("requests_app", "Category")
    for name in CATEGORIES:
        Category.objects.get_or_create(name=name)


class Migration(migrations.Migration):
    dependencies = [("requests_app", "0001_initial")]

    operations = [
        migrations.RunPython(add_categories, migrations.RunPython.noop),
    ]