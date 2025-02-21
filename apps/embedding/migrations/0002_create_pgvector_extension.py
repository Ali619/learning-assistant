from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # Replace 'your_app' with your app name and the previous migration
        ('embedding', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE EXTENSION IF NOT EXISTS vector",
            "DROP EXTENSION IF EXISTS vector"
        )
    ]
