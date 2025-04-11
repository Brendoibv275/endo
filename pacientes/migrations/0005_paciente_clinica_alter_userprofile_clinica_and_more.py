# Generated by Django 4.2.7 on 2025-04-11 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0004_funcaousuario_clinica_userprofile_clinica_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='clinica',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pacientes', to='pacientes.clinica', verbose_name='Clínica'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='clinica',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pacientes.clinica'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='funcao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pacientes.funcaousuario'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_team_leader',
            field=models.BooleanField(default=False),
        ),
    ]
