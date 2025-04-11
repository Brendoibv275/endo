# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fichas_clinicas', '0001_initial'),
    ]

    operations = [
        # Adicionar campos ao modelo SessaoAtendimento
        migrations.AddField(
            model_name='sessaoatendimento',
            name='ctp',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='CTP (Comprimento de Trabalho Provisu00f3rio)'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='iaf',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='IAF (Lima Apical Inicial)'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='crt',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='CRT (Comprimento Real de Trabalho)'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='lai',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='LAI (Limite Apical de Instrumentau00e7u00e3o)'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='im',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='IM (Instrumento de Memu00f3ria)'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='grampo',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Grampo'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='canal',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Canal'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='cad',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='CAD (Localizador Apical Eletru00f4nico)'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='solucao_irrigadora',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Soluu00e7u00e3o irrigadora'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='curativo_demora',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Curativo de demora'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='material_obturador',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Material Obturador'),
        ),
        migrations.AddField(
            model_name='sessaoatendimento',
            name='medicacao_sistemica',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Medicau00e7u00e3o Sistu00eamica'),
        ),
        
        # Remover campos do modelo FichaClinica
        migrations.RemoveField(
            model_name='fichaclinica',
            name='ctp',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='iaf',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='crt',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='lai',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='im',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='grampo',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='canal',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='cad',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='solucao_irrigadora',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='curativo_demora',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='material_obturador',
        ),
        migrations.RemoveField(
            model_name='fichaclinica',
            name='medicacao_sistemica',
        ),
    ]