from django.db import migrations

def fix_data(apps, schema_editor):
    FichaClinica = apps.get_model('fichas_clinicas', 'FichaClinica')
    Anamnese = apps.get_model('fichas_clinicas', 'Anamnese')
    ExameClinico = apps.get_model('fichas_clinicas', 'ExameClinico')
    Diagnostico = apps.get_model('fichas_clinicas', 'Diagnostico')
    
    # Limpa as referências inválidas
    FichaClinica.objects.all().update(
        anamnese=None,
        exame_clinico=None,
        diagnostico=None
    )

class Migration(migrations.Migration):
    dependencies = [
        ('fichas_clinicas', '0004_anamnese_diagnostico_exameclinico_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_data),
    ] 