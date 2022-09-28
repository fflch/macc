# Generated by Django 4.1.1 on 2022-09-28 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0003_originalfragment_place_publisher_work_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='originalfragment',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='corpus.work', verbose_name='obra'),
        ),
        migrations.AlterField(
            model_name='place',
            name='city',
            field=models.CharField(max_length=255, null=True, verbose_name='cidade'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='local', to='corpus.place'),
        ),
        migrations.AlterField(
            model_name='translatedfragment',
            name='original',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='corpus.originalfragment', verbose_name='original'),
        ),
        migrations.AlterField(
            model_name='translatedfragment',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='corpus.translation', verbose_name='tradução'),
        ),
        migrations.AlterField(
            model_name='translation',
            name='authors',
            field=models.ManyToManyField(blank=True, to='corpus.translator', verbose_name='autores'),
        ),
        migrations.AlterField(
            model_name='translation',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='corpus.publisher', verbose_name='editora'),
        ),
        migrations.AlterField(
            model_name='translation',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='corpus.work', verbose_name='original'),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('year', models.PositiveIntegerField(verbose_name='ano')),
                ('title', models.CharField(max_length=255, verbose_name='título')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='código')),
                ('authors', models.ManyToManyField(blank=True, to='corpus.translator', verbose_name='autores')),
                ('publisher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='corpus.publisher', verbose_name='editora')),
            ],
            options={
                'verbose_name': 'coletânea',
                'verbose_name_plural': 'coletâneas',
            },
        ),
        migrations.AddField(
            model_name='translation',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='corpus.collection', verbose_name='coletânea'),
        ),
    ]
