# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 09:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sqlreview', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='master_config',
            new_name='cluster_config',
        ),
    ]