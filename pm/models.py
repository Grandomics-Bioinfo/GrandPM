from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from multiselectfield import MultiSelectField
from .forms import ProjectForm


class Sale(models.Model):
    class Meta:
        verbose_name = _("销售列表")
        verbose_name_plural = _("销售")
    name = models.CharField(_("姓名"), max_length=200)
    dept = models.CharField(_("区域"), max_length=200)
    tel = models.CharField(_("电话"), max_length=20, null=True, blank=True)
    

class Analysis_Type(models.Model):
    class Meta:
        verbose_name = _("分析类型")
        verbose_name_plural = _("分析类型")
    name=models.CharField("分析类型", max_length=50)

    def __str__(self):
        return '%s' % self.name


class Custom(models.Model):
    class Meta:
        verbose_name = _("Custom")
        verbose_name_plural = _("Custom")
    custom_name = models.CharField("客户名称", max_length=200)
    custom_dept = models.CharField(_("客户单位"), max_length=200)
    tel = models.CharField(_("客户电话"), max_length=20)
    def __str__(self):
        return '%s_%s' %(self.custom_name, self.custom_dept)

class Project(models.Model):
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Project")

    Platform = (
    ('pb', _('Pacbio')),
    ('ont', _('Nanopore')),
    ('bionano', _('Bionano')),
   ('ngs', _('NGS'))
)
    Analysis_Types = (
        ('met', _('甲基化')),
        ('sv', _('结构变异')),
        ('str', _('串联重复')),
        ('tumor', _('肿瘤')),
        ('haplotype', _('单体型'))
    )
    analysis_type_list = Analysis_Type.objects.all().values_list('name')
    analysis_type_list = [(x[0], x[0]) for x in analysis_type_list]
    print(analysis_type_list)

   
    STATUSES = (
        ('to-do', _('To Do')),
        ('in_progress', _('In Progress')),
        ('blocked', _('Blocked')),
        ('done', _('Done')),
        ('dismissed', _('Dismissed'))
    )

    PRIORITIES = (
        ('00_low', _('Low')),
        ('10_normal', _('Normal')),
        ('20_high', _('High')),
        ('30_critical', _('Critical')),
        ('40_blocker', _('Blocker'))
    )

    proj_id = models.CharField(_("proj_id"), max_length=200)
    proj_name = models.CharField(_("proj_name"), max_length=200)
    custom = models.ForeignKey(Custom, related_name='project_custom', on_delete=models.SET_NULL, null=True, blank=False)
    platform = models.CharField(_("platform"), max_length=20, choices=Platform, default='ont')
    analysis_type = MultiSelectField(_("analysis_type"), max_length=20, choices=analysis_type_list, default='sv')
    start = models.DateField(_("start"), null=True, blank=True)
    deadline = models.DateField(_("deadline"), null=True, blank=True)
    sale = models.ForeignKey(Sale, related_name='project', verbose_name=_('销售'),
                                   on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(_("state"), max_length=20, choices=STATUSES, default='to-do')
    priority = models.CharField(_("priority"), max_length=20, choices=PRIORITIES, default='10_normal')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True, editable=False)

    description = models.TextField(_("description"), max_length=2000, null=True, blank=True)
    def __str__(self):
        return "[%s] %s" % (self.id, self.proj_id)


class Sample(models.Model):
    class Meta:
        verbose_name = _("Sample")
        verbose_name_plural = _("Sample")
    Platform = (
    ('pb', _('Pacbio')),
    ('ont', _('Nanopore')),
    ('bionano', _('Bionano')),
   ('ngs', _('NGS'))
)
    Analysis_Type = (
        ('Met', _('甲基化')),
        ('SV', _('结构变异')),
        ('STR', _('串联重复')),
        ('Tumor', _('肿瘤')),
        ('Haplotype', _('单体型'))
    )


    STATUSES = (
        ('weishouyang', _('未收样')),
        ('shouyang', _('收样')),
        ('tiqu', _('提取')),
        ('jianku', _('建库')),
        ('shangji', _('上机测序')),
        ('fenxi', _('生信分析')),
        ('jiedu', _('报告解读')),
        ('jiaofu', _('交付'))
    )

    PRIORITIES = (
        ('00_low', _('Low')),
        ('10_normal', _('Normal')),
        ('20_high', _('High')),
        ('30_critical', _('Critical')),
        ('40_blocker', _('Blocker'))
    )


    sample_id = models.CharField(_("样本编号"), max_length=200)
    sample_name = models.CharField(_("样本姓名"), max_length=200)
    platform = models.CharField(_("测序平台"), max_length=20, choices=Platform, default='ont')
    analysis_type = models.CharField(_("分析类型"), max_length=20, choices=Analysis_Type, default='sv')
    start = models.DateField(_("开始时间"), null=True, blank=True)
    deadline = models.DateField(_("截止时间"), null=True, blank=True)
    priority = models.CharField(_("优先级"), max_length=20, choices=PRIORITIES, default='10_normal')
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("上次修改"), auto_now=True, editable=False) 
    state = models.CharField(_("状态"), max_length=20, choices=STATUSES, default='to-do')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sample_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)


class Sequence(models.Model):
    class Meta:
        verbose_name = _("Sequence")
        verbose_name_plural = _("Sequence")
    Sample_Type = (
    ('dna', _('DNA')),
    ('rna', _('RNA'))
)
    Machine_ID = (
    ('G01', _('GridION_1')),
    ('G02', _('GridION_2')),
    ('G03', _('GridION_3')),
    ('G04', _('GridION_4')),
    ('P01', _('PromethION_1'))
)
    jianku_date = models.DateTimeField(_("jianku_date"), editable=True)
    sample_type = models.CharField(_("sample_type"), max_length=20, choices=Sample_Type, default='dna')
    library_id = models.CharField(_("library_id"), max_length=200)
    machine_id = models.CharField(_("machine_id"), max_length=200,  choices=Machine_ID)
    cell_id = models.CharField(_("cell_id"), max_length=200)
    sequence_time = models.DateTimeField(_("sequence_time"))
    yield_data = models.FloatField(_("yield_data"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sequence_user', verbose_name=_('测序人员'),
                                   on_delete=models.SET_NULL, null=True, blank=True)



