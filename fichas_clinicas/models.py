from django.db import models
from django.urls import reverse
from pacientes.models import Paciente
from django.contrib.auth.models import User
import datetime

class Anamnese(models.Model):
    # História Médica
    tratamento_medico = models.BooleanField('Está sob tratamento médico?', default=False)
    uso_medicamentos = models.TextField('Uso de medicamentos', blank=True, null=True)
    alergias = models.TextField('Alergias', blank=True, null=True)
    problemas_cardiacos = models.BooleanField('Problemas Cardíacos', default=False)
    gastrite_ulceras = models.BooleanField('Gastrite/Úlceras', default=False)
    problemas_neurologicos = models.BooleanField('Problemas Neurológicos', default=False)
    problemas_coagulacao = models.BooleanField('Problemas de Coagulação', default=False)
    diabetes = models.BooleanField('Diabetes', default=False)
    sensibilidade_anestesicos = models.BooleanField('Sensibilidade a anestésicos/antibióticos', default=False)
    pressao_arterial = models.BooleanField('Pressão arterial alterada', default=False)
    gravidez = models.BooleanField('Gravidez', default=False)
    sifilis = models.BooleanField('Sífilis', default=False)
    epilepsia = models.BooleanField('Epilepsia', default=False)
    lesao_figado = models.BooleanField('Lesão de Fígado', default=False)
    lesao_renal = models.BooleanField('Lesão Renal', default=False)
    outras_condicoes = models.TextField('Outras condições', blank=True, null=True)
    
    # História Dental
    historia_dental = models.TextField('História Dental', blank=True, null=True)
    
    # Análise da Dor
    dor_presente = models.BooleanField('Dor Presente', default=False)
    
    ESTIMULO_CHOICES = (
        ('E', 'Espontânea'),
        ('T', 'Térmico'),
        ('Q', 'Químico'),
        ('M', 'Mecânico'),
    )
    estimulo = models.CharField('Estímulo', max_length=1, choices=ESTIMULO_CHOICES, blank=True, null=True)
    
    LOCALIZACAO_CHOICES = (
        ('L', 'Localizada'),
        ('D', 'Difusa'),
        ('R', 'Referida'),
    )
    localizacao = models.CharField('Localização', max_length=1, choices=LOCALIZACAO_CHOICES, blank=True, null=True)
    
    FREQUENCIA_CHOICES = (
        ('C', 'Constante'),
        ('I', 'Intermitente'),
    )
    frequencia = models.CharField('Frequência', max_length=1, choices=FREQUENCIA_CHOICES, blank=True, null=True)
    
    INTENSIDADE_CHOICES = (
        ('L', 'Leve'),
        ('M', 'Moderada'),
        ('I', 'Intensa'),
    )
    intensidade = models.CharField('Intensidade', max_length=1, choices=INTENSIDADE_CHOICES, blank=True, null=True)
    
    INICIO_CHOICES = (
        ('R', 'Recentemente'),
        ('A', 'Antigo'),
    )
    inicio = models.CharField('Início', max_length=1, choices=INICIO_CHOICES, blank=True, null=True)
    
    DURACAO_CHOICES = (
        ('S', 'Segundos'),
        ('M', 'Minutos'),
        ('H', 'Horas'),
        ('D', 'Dias'),
    )
    duracao = models.CharField('Duração', max_length=1, choices=DURACAO_CHOICES, blank=True, null=True)
    
    # Exacerbada por
    exacerbada_frio = models.BooleanField('Exacerbada por Frio', default=False)
    exacerbada_quente = models.BooleanField('Exacerbada por Quente', default=False)
    exacerbada_doce = models.BooleanField('Exacerbada por Doce', default=False)
    exacerbada_mastigacao = models.BooleanField('Exacerbada por Mastigação', default=False)
    exacerbada_outro = models.CharField('Exacerbada por Outro', max_length=100, blank=True, null=True)
    
    # Aliviada por
    aliviada_ar = models.BooleanField('Aliviada por Ar', default=False)
    aliviada_analgesico = models.BooleanField('Aliviada por Analgésico', default=False)
    aliviada_decubito = models.BooleanField('Aliviada por Decúbito', default=False)
    aliviada_outro = models.CharField('Aliviada por Outro', max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Anamnese'
        verbose_name_plural = 'Anamneses'

class ExameClinico(models.Model):
    # Semiologia Extraoral
    assimetria_facial = models.BooleanField('Assimetria facial', default=False)
    tumefacao = models.BooleanField('Tumefação', default=False)
    fistula_cutanea = models.BooleanField('Fístula cutânea', default=False)
    enfartamento_ganglionar = models.BooleanField('Enfartamento Ganglionar', default=False)
    
    # Inspeção Intraoral - Tecidos Moles
    fistula = models.BooleanField('Fístula', default=False)
    ulceracao = models.BooleanField('Ulceração', default=False)
    alteracao_cor = models.BooleanField('Alteração de cor', default=False)
    tumefacao_apical = models.BooleanField('Tumefação apical', default=False)
    bolsa_periodontal = models.BooleanField('Bolsa Periodontal', default=False)
    
    # Inspeção Intraoral - Tecidos Duros
    carie = models.BooleanField('Cárie', default=False)
    
    RESTAURACAO_CHOICES = (
        ('N', 'Não possui'),
        ('M', 'Metálica'),
        ('R', 'Resina'),
        ('O', 'Outro'),
    )
    restauracao = models.CharField('Restauração', max_length=1, choices=RESTAURACAO_CHOICES, default='N')
    
    EXPOSICAO_PULPAR_CHOICES = (
        ('N', 'Não possui'),
        ('P', 'Patológica'),
        ('M', 'Mecânica'),
    )
    exposicao_pulpar = models.CharField('Exposição pulpar', max_length=1, choices=EXPOSICAO_PULPAR_CHOICES, default='N')
    
    alteracao_cor_coroa = models.BooleanField('Alteração de cor da coroa', default=False)
    mobilidade = models.BooleanField('Mobilidade', default=False)
    
    # Testes de Vitalidade Pulpar e Condição Apical
    RESPOSTA_TESTE_CHOICES = (
        ('N', 'Normal'),
        ('A', 'Ausente'),
        ('D', 'Diminuída'),
        ('E', 'Exacerbada'),
    )
    teste_frio = models.CharField('Teste Frio', max_length=1, choices=RESPOSTA_TESTE_CHOICES, blank=True, null=True)
    teste_quente = models.CharField('Teste Quente', max_length=1, choices=RESPOSTA_TESTE_CHOICES, blank=True, null=True)
    
    RESPOSTA_PERCUSSAO_CHOICES = (
        ('N', 'Negativa'),
        ('P', 'Positiva'),
    )
    percussao_vertical = models.CharField('Percussão Vertical', max_length=1, choices=RESPOSTA_PERCUSSAO_CHOICES, blank=True, null=True)
    percussao_horizontal = models.CharField('Percussão Horizontal', max_length=1, choices=RESPOSTA_PERCUSSAO_CHOICES, blank=True, null=True)
    palpacao_apical = models.CharField('Palpação Apico-Cervical', max_length=1, choices=RESPOSTA_PERCUSSAO_CHOICES, blank=True, null=True)
    
    # Exame Radiográfico
    CAMARA_PULPAR_CHOICES = (
        ('N', 'Normal'),
        ('C', 'Calcificada'),
        ('A', 'Alterada'),
    )
    camara_pulpar = models.CharField('Câmara Pulpar', max_length=1, choices=CAMARA_PULPAR_CHOICES, blank=True, null=True)
    
    CANAL_RADICULAR_CHOICES = (
        ('N', 'Normal'),
        ('A', 'Atresiados'),
        ('C', 'Calcificados'),
        ('D', 'Dilacerados'),
    )
    canal_radicular = models.CharField('Canal Radicular', max_length=1, choices=CANAL_RADICULAR_CHOICES, blank=True, null=True)
    
    PERICEMENTO_CHOICES = (
        ('N', 'Normal'),
        ('E', 'Espessado'),
    )
    pericemento = models.CharField('Pericemento', max_length=1, choices=PERICEMENTO_CHOICES, blank=True, null=True)
    
    rarefacao_ossea = models.BooleanField('Rarefação óssea', default=False)
    
    RAREFACAO_TIPO_CHOICES = (
        ('D', 'Difusa'),
        ('C', 'Circunscrita'),
    )
    rarefacao_tipo = models.CharField('Tipo de Rarefação', max_length=1, choices=RAREFACAO_TIPO_CHOICES, blank=True, null=True)
    
    nodulos = models.BooleanField('Nódulos', default=False)
    deformacao_assoalho = models.BooleanField('Deformação do assoalho', default=False)
    trepanacao = models.BooleanField('Trepanação', default=False)
    reabsorcao_interna = models.BooleanField('Reabsorção interna', default=False)
    reabsorcao_externa = models.BooleanField('Reabsorção externa', default=False)
    instrumento_fraturado = models.BooleanField('Instrumento fraturado', default=False)
    degrau_apical = models.BooleanField('Degrau apical', default=False)
    fratura_radicular = models.BooleanField('Fratura radicular', default=False)
    dilaceracao_apical = models.BooleanField('Dilaceração apical', default=False)
    rizogenese_incompleta = models.BooleanField('Rizogênese incompleta', default=False)
    osteite_condensante = models.BooleanField('Osteíte Condensante', default=False)
    hipercementose = models.BooleanField('Hipercementose', default=False)
    
    class Meta:
        verbose_name = 'Exame Clínico'
        verbose_name_plural = 'Exames Clínicos'

class Diagnostico(models.Model):
    diagnostico = models.TextField('Diagnóstico clínico radiográfico provável', blank=True, null=True)
    
    TRATAMENTO_CHOICES = (
        ('P', 'Pulpectomia'),
        ('N', 'Necropulpectomia'),
        ('R', 'Retratamento'),
        ('O', 'Outro'),
    )
    tratamento_indicado = models.CharField('Tratamento indicado', max_length=1, choices=TRATAMENTO_CHOICES, blank=True, null=True)
    
    acidentes_operatorios = models.TextField('Acidentes Operatórios', blank=True, null=True)
    pos_tratamento = models.TextField('Pós Tratamento', blank=True, null=True)
    
    PRESERVACAO_CHOICES = (
        ('1', '1 mês'),
        ('3', '3 meses'),
        ('6', '6 meses'),
        ('12', '12 meses'),
        ('24', '24 meses'),
    )
    preservacao = models.CharField('Preservação', max_length=2, choices=PRESERVACAO_CHOICES, blank=True, null=True)
    
    data_termino = models.DateField('Data término do tratamento', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'

class FichaClinica(models.Model):
    STATUS_CHOICES = (
        ('A', 'Aberta'),
        ('E', 'Em Andamento'),
        ('F', 'Finalizada'),
    )
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='fichas_clinicas')
    dente = models.CharField('Dente', max_length=10, blank=True, null=True, help_text='Número ou região do dente')
    data_abertura = models.DateField('Data de abertura', default=datetime.date.today)
    queixa_principal = models.TextField('Queixa principal')
    status = models.CharField('Status', max_length=1, choices=STATUS_CHOICES, default='A')
    
    # Relacionamentos com os novos modelos
    anamnese = models.OneToOneField(Anamnese, on_delete=models.CASCADE, related_name='ficha', null=True, blank=True)
    exame_clinico = models.OneToOneField(ExameClinico, on_delete=models.CASCADE, related_name='ficha', null=True, blank=True)
    diagnostico = models.OneToOneField(Diagnostico, on_delete=models.CASCADE, related_name='ficha', null=True, blank=True)
    
    # Campos de controle
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fichas_criadas')
    data_criacao = models.DateTimeField('Data de criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Data de atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Ficha Clínica'
        verbose_name_plural = 'Fichas Clínicas'
        ordering = ['-data_abertura']
    
    def __str__(self):
        return f'Ficha {self.id} - {self.paciente.nome} - Dente {self.dente or "N/A"}'
    
    def get_absolute_url(self):
        return reverse('ficha_detalhe', kwargs={'pk': self.pk})

class SessaoAtendimento(models.Model):
    ficha = models.ForeignKey(FichaClinica, on_delete=models.CASCADE, related_name='sessoes')
    data_sessao = models.DateField('Data da sessão')
    hora_sessao = models.TimeField('Horário da sessão', null=True, blank=True)
    procedimentos = models.TextField('Procedimentos realizados')
    observacoes = models.TextField('Observações', blank=True, null=True)
    materiais = models.TextField('Materiais utilizados', blank=True, null=True)
    realizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sessoes_realizadas')
    data_registro = models.DateTimeField('Data de registro', auto_now_add=True)
    
    TIPO_SESSAO_CHOICES = (
        ('Inicial', 'Consulta Inicial'),
        ('Retorno', 'Retorno'),
        ('Tratamento', 'Tratamento'),
        ('Finalização', 'Finalização'),
    )
    tipo_sessao = models.CharField('Tipo de sessão', max_length=20, choices=TIPO_SESSAO_CHOICES, blank=True, null=True)
    
    # Detalhes do Tratamento Endodôntico
    ctp = models.CharField('CTP (Comprimento de Trabalho Provisório)', max_length=10, blank=True, null=True)
    iaf = models.CharField('IAF (Lima Apical Inicial)', max_length=10, blank=True, null=True)
    crt = models.CharField('CRT (Comprimento Real de Trabalho)', max_length=10, blank=True, null=True)
    lai = models.CharField('LAI (Limite Apical de Instrumentação)', max_length=10, blank=True, null=True)
    im = models.CharField('IM (Instrumento de Memória)', max_length=10, blank=True, null=True)
    grampo = models.CharField('Grampo', max_length=10, blank=True, null=True)
    canal = models.CharField('Canal', max_length=50, blank=True, null=True)
    cad = models.CharField('CAD (Localizador Apical Eletrônico)', max_length=50, blank=True, null=True)
    solucao_irrigadora = models.CharField('Solução irrigadora', max_length=100, blank=True, null=True)
    curativo_demora = models.CharField('Curativo de demora', max_length=100, blank=True, null=True)
    material_obturador = models.CharField('Material Obturador', max_length=100, blank=True, null=True)
    medicacao_sistemica = models.CharField('Medicação Sistêmica', max_length=100, blank=True, null=True)
    
    # Campos para upload de imagens (radiografias)
    imagem = models.ImageField('Imagem/Radiografia', upload_to='sessoes/imagens/', blank=True, null=True)
    descricao_imagem = models.CharField('Descrição da imagem', max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Sessão de Atendimento'
        verbose_name_plural = 'Sessões de Atendimento'
        ordering = ['-data_sessao']
    
    def __str__(self):
        return f'Sessão {self.id} - {self.ficha.paciente.nome} - {self.data_sessao}'