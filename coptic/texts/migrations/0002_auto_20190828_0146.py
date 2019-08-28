# Generated by Django 2.2.4 on 2019-08-28 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0001_remove_ingest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corpus',
            name='annis_corpus_name',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='corpus',
            name='urn_code',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='text',
            name='text_meta',
            field=models.ManyToManyField(blank=True, db_index=True, to='texts.TextMeta'),
        ),
        migrations.AlterField(
            model_name='textmeta',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='textmeta',
            name='value',
            field=models.CharField(db_index=True, max_length=10000),
        ),
    ]
