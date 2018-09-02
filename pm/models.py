from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from multiselectfield import MultiSelectField



class Sale(models.Model):
    class Meta:
        verbose_name = _("销售列表")
        verbose_name_plural = _("销售")
    name = models.CharField(_("姓名"), max_length=200)
    dept = models.CharField(_("区域"), max_length=200)
    tel = models.CharField(_("电话"), max_length=20, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name


class Platform(models.Model):
    class Meta:
        verbose_name = _("测序平台")
        verbose_name_plural = _("测序平台")
    name = models.CharField("平台名称", max_length=200)
    name_long = models.CharField("平台全称", max_length=200)

    def __str__(self):
        return self.name

 
class Machine(models.Model):
    class Meta:
        verbose_name = _("测序仪")
        verbose_name_plural = _("测序仪")
    name = models.CharField(_("机器编号"), max_length=200)
    dept = models.CharField(_("部门"), max_length=200, null=True, blank=True)
    platform = models.ForeignKey(Platform, related_name='machine', verbose_name=_('测序平台'),
                               on_delete=models.PROTECT, null=True, blank=False)
    def __str__(self):
        return self.name

class Analysis_Type(models.Model):
    class Meta:
        verbose_name = _("分析类型")
        verbose_name_plural = _("分析类型")
    name=models.CharField("分析类型", max_length=50)

    def __str__(self):
        return self.name


class Custom(models.Model):
    class Meta:
        verbose_name = _("客户")
        verbose_name_plural = _("客户")
    name = models.CharField("客户名称", max_length=200)
    dept = models.CharField(_("客户单位"), max_length=200)
    tel = models.CharField(_("客户电话"), max_length=20, blank=True)
    addr = models.CharField(_("地址"), max_length=200, blank=True, null=True)
    country = models.CharField(_("国家"), max_length=20, blank=True, null=True)
    def __str__(self):
        return self.name


class Project(models.Model):
    class Meta:
        verbose_name = _("项目")
        verbose_name_plural = _("项目")

    STATUSES = (
        ('To Do', _('To Do')),
        ('In Progress', _('In Progress')),
        ('Blocked', _('Blocked')),
        ('Done', _('Done')),
        ('Dismissed', _('Dismissed'))
    )
   
    PRIORITIES = (
        ('Low', _('Low')),
        ('Normal', _('Normal')),
        ('Hign', _('High')),
        ('Critical', _('Critical')),
        ('Blocker', _('Blocker'))
    )


    
    PROJ_OWNER = (
   ('北京希望组', '北京希望组'),
   ('武汉希望组', '武汉希望组'),
   ('武汉未来组', '武汉未来组'),
)
    proj_id = models.CharField(_("合同号"), max_length=200)
    proj_name = models.CharField(_("合同名称"), max_length=200)
    proj_owner = models.CharField(_("项目归属"), max_length=200, choices=PROJ_OWNER, default='北京希望组')
    sample_amount = models.IntegerField(_("样本数目"), null=True, blank=True) 

    custom = models.ForeignKey(Custom, related_name='project_custom', verbose_name=_('客户名称'),
                               on_delete=models.PROTECT, null=True, blank=False)

    platform = models.ManyToManyField(Platform, verbose_name=_("测序平台"), blank=True )    
    analysis_type = models.ManyToManyField(Analysis_Type, verbose_name=_("分析类型"), blank=True)
    start = models.DateField(_("启动时间"), null=True, blank=True)
    deadline = models.DateField(_("截止日期"), null=True, blank=True)
    end = models.DateField(_("完成时间"), null=True, blank=True)
    sale = models.ForeignKey(Sale, related_name='project', verbose_name=_('销售'),
                                   on_delete=models.PROTECT, null=True, blank=True)

    contract_type = models.CharField(_("合同分类"),max_length=100, null=True, blank=True) 
    is_invoice = models.BooleanField ("是否开票", blank=True, default=False )
    invoice_id = models.CharField(_("票号"),max_length=100, null=True, blank=True) 
    is_pay = models.BooleanField("是否收款", blank=True, default=False)
    price = models.IntegerField(_("总额"), null=True, blank=True) 
    pay_money = models.IntegerField(_("已付款"), null=True, blank=True) 

    status = models.CharField(_("状态"), max_length=20, choices=STATUSES, default='to-do')
    priority = models.CharField(_("优先级"), max_length=20, choices=PRIORITIES, default='10_normal')
    description = models.TextField(_("备注"), max_length=2000, null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_created', verbose_name=_('created by'),
                                   on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True, editable=False)


    def __str__(self):
        return "%s-%s" % (self.proj_id, self.proj_name)


class Sample(models.Model):
    class Meta:
        verbose_name = _("样本")
        verbose_name_plural = _("样本")


    STATUSES = (
        ('未收样', _('未收样')),
        ('收样', _('收样')),
        ('提取', _('提取')),
        ('建库', _('建库')),
        ('上机测序', _('上机测序')),
        ('生信分析', _('生信分析')),
        ('报告解读', _('报告解读')),
        ('交付', _('交付'))
    )

    PRIORITIES = (
        ('Low', _('Low')),
        ('Normal', _('Normal')),
        ('Hign', _('High')),
        ('Critical', _('Critical')),
        ('Blocker', _('Blocker'))
    )

    project = models.ForeignKey(Project, related_name='sample', verbose_name=_('合同编号'),
                                   on_delete=models.PROTECT, null=True, blank=True)

    sample_id = models.CharField(_("样本编号"), max_length=200)
    sample_name = models.CharField(_("样本姓名"), max_length=200)
    sample_name2 = models.CharField(_("修正姓名"), max_length=200, null=True, blank=True)
    platform = models.ManyToManyField(Platform, verbose_name=_("测序平台"), blank=True )    
    analysis_type = models.ManyToManyField(Analysis_Type, verbose_name=_("分析类型"), blank=True)
    sample_type = models.CharField(_("样本类型"), max_length=20, null=True, blank=True)
    start = models.DateField(_("开始时间"), null=True, blank=True)
    end = models.DateTimeField(_("交付时间"), null=True, blank=True)
    deadline = models.DateField(_("截止时间"), null=True, blank=True)
    data_size = models.CharField(_("数据量"),max_length=500, null=True, blank=True)
    receive_start = models.DateTimeField(_("收样开始时间"), null=True, blank=True)
    extract_finish = models.BooleanField("提取完成", blank=True, default=False) 
    library_finish = models.BooleanField("建库完成", blank=True, default=False)
    sequence_finish = models.BooleanField("测序完成", blank=True, default=False) 
    bioinfo_finish = models.BooleanField("生信完成", blank=True, default=False)
    priority = models.CharField(_("优先级"), max_length=20, choices=PRIORITIES, default='10_normal')
    status = models.CharField(_("状态"), max_length=20, choices=STATUSES, default='to-do')
    description = models.TextField(_("备注"), max_length=2000, null=True, blank=True)
    
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("上次修改"), auto_now=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sample_created', verbose_name=_('created by'),
                                   on_delete=models.PROTECT, null=True)
    def __str__(self):
        return "[%s] %s" % (self.sample_id, self.sample_name)


class Extraction(models.Model):

    class Meta:
        verbose_name = _("提取")
        verbose_name_plural = _("提取")

    PROJ_TYPE = (
    ('科研', '科研'),
    ('临床', '临床')
)
    order_id = models.CharField(_("下单编号"), max_length=200, null=True, blank=True)
    order_date = models.DateTimeField(_("下单时间"), auto_now_add=True, editable=False)
    sample = models.ForeignKey(Sample, related_name='extraction', verbose_name=_('样本编号'),
                                   on_delete=models.PROTECT, null=True, blank=True)

    proj_type = models.CharField(_("项目类型"), max_length=50,choices=PROJ_TYPE, null=True, blank=True)
    bct_id = models.CharField(_("采血管编号"), max_length=500, null=True, blank=True) # 采血管blood collection tube
    bct_amount = models.IntegerField(_("管数"), null=True, blank=True)
    sample_type = models.CharField(_("样本类型"), max_length=20, null=True, blank=True)
    method = models.CharField(_("提取方法"), max_length=20, null=True, blank=True) 
    is_finish = models.BooleanField("是否完成", blank=True, default=False) 
    finish_date = models.DateTimeField(_("完成时间"), editable=True, null=True, blank=True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='extraction', verbose_name=_('提取人员'),
                                   on_delete=models.PROTECT, null=True, blank=True)
    
    description = models.TextField(_("备注"), max_length=2000, null=True, blank=True)

    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("上次修改"), auto_now=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='extract_created', verbose_name=_('created by'),
                                   on_delete=models.PROTECT, null=True)

    def __str__(self):
        return 'Extraction:%s' % self.sample

class Sequence(models.Model):
    class Meta:
        verbose_name = _("上机测序")
        verbose_name_plural = _("上机测序")
    Sample_Type = (
    ('DNA', _('DNA')),
    ('RNA', _('RNA'))
)
    Machine_ID = (
    ('G01', _('GridION_1')),
    ('G02', _('GridION_2')),
    ('G03', _('GridION_3')),
    ('G04', _('GridION_4')),
    ('P01', _('PromethION_1'))
) 
    #Machine_ID = Machine.objects.all().values_list('name')
    #Machine_ID = [(x[0], x[0]) for x in Machine_ID]
        
    order_id = models.CharField(_("下单编号"), max_length=200, null=True, blank=True)
    order_date = models.DateTimeField(_("下单时间"), auto_now_add=True, editable=False)
    sample = models.ForeignKey(Sample, related_name='sequence', verbose_name=_('样本编号'),
                                   on_delete=models.PROTECT, null=True, blank=True)
    library_require = models.CharField(_("建库要求"), max_length=500, null=True, blank=True)
    library_start = models.DateTimeField(_("建库时间"), editable=True, null=True, blank=True)
    sample_type = models.CharField(_("样本类型"), max_length=20, choices=Sample_Type, default='DNA', null=True, blank=True)
    library_id = models.CharField(_("文库编号"), max_length=50, null=True, blank=True)
    library_size = models.CharField(_("建库大小"), max_length=50, null=True, blank=True)
    library_kit = models.CharField(_("建库试剂盒"), max_length=50, null=True, blank=True)
    machine = models.ForeignKey(Machine, related_name='sequence', verbose_name=_('机器编号'),
                                   on_delete=models.PROTECT, null=True, blank=True)
    cell_pos = models.CharField(_("上机位置"), max_length=50, null=True, blank=True)
    sequence_start = models.DateTimeField(_("测序开始时间"), null=True, blank=True)
    sequence_end = models.DateTimeField(_("测序结束时间"), null=True, blank=True)
    #is_finish = BooleanField("是否完成", null=True, blank=True) 
    yield_data = models.FloatField(_("产量"), null=True, blank=True)
    ap_total = models.IntegerField(_("Total"), null=True, blank=True)
    ap_muxscan = models.IntegerField(_("Muxscan"), null=True, blank=True)
    ap_g1 = models.IntegerField(_("Active Pore G1"), null=True, blank=True)
    ap_g2 = models.IntegerField(_("Active Pore G2"), null=True, blank=True)
    ap_g3 = models.IntegerField(_("Active Pore G3"), null=True, blank=True)
    ap_g4 = models.IntegerField(_("Active Pore G4"), null=True, blank=True)

    total_bases = models.BigIntegerField(_('原始数据量'), null=True, blank=True) 
    total_reads = models.PositiveIntegerField(_('原始reads数目'), null=True, blank=True)

    pass_bases = models.BigIntegerField(_('过滤数据量'), null=True, blank=True) 
    pass_total_reads = models.PositiveIntegerField(_('过滤reads数目'),null=True, blank=True)
    pass_reads_avg =  models.PositiveIntegerField(_('Reads平均长度'),null=True, blank=True)
    pass_reads_n50 =  models.PositiveIntegerField(_('Reads N50长度'), null=True, blank=True)
    pass_reads_median =  models.PositiveIntegerField(_('Reads中位数长度'), null=True, blank=True)
    pass_reads_avg_score = models.PositiveSmallIntegerField(_('平均质量值'), null=True, blank=True)

    mapped_reads = models.PositiveIntegerField(_('过滤reads数目'), null=True, blank=True)
    mapped_bases = models.BigIntegerField(_('过滤数据量'), null=True, blank=True)
    raw_dir = models.CharField(_("Raw data 路径"), max_length=200, null=True, blank=True)
    pass_dir = models.CharField(_("Pass data 路径"), max_length=200, null=True, blank=True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sequence', verbose_name=_('测序人员'),
                                   on_delete=models.PROTECT, null=True, blank=True)

    description = models.TextField(_("备注"), max_length=2000, null=True, blank=True)
    
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("上次修改"), auto_now=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sequence_created', verbose_name=_('创建人'),
                                   on_delete=models.PROTECT, null=True)

    def __str__(self):
        return 'Sequence %s' % self.sample

class Bioinfo(models.Model):
    class Meta:
        verbose_name = _("生信分析")
        verbose_name_plural = _("生信分析")

    sample = models.ForeignKey(Sample, related_name='Bioinfo', verbose_name=_('样本编号'),
                                   on_delete=models.PROTECT, null=True, blank=True)
   
    re = models.IntegerField(_("DEL数目"), null=True, blank=True)
    del_amount = models.IntegerField(_("DEL数目"), null=True, blank=True)
    ins_amount = models.IntegerField(_("INS数目"), null=True, blank=True)
    inv_amount = models.IntegerField(_("INV数目"), null=True, blank=True)
    dup_amount = models.IntegerField(_("DUP数目"), null=True, blank=True)
    tra_amount = models.IntegerField(_("TRA数目"), null=True, blank=True)
    
    bioinfo_start = models.DateTimeField(_("生信分析开始时间"), null=True, blank=True)
    bioinfo_end = models.DateTimeField(_("生信分析结束时间"), null=True, blank=True)
    report_end = models.DateTimeField(_("报告解读结束时间"), null=True, blank=True)
    analysis_dir = models.CharField(_("分析目录"), max_length=200, null=True, blank=True)
    
    description = models.TextField(_("备注"), max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("上次修改"), auto_now=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bioinfo_created', verbose_name=_('created by'),
                                   on_delete=models.PROTECT, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bioinfo', verbose_name=_('分析人员'),
                                   on_delete=models.PROTECT, null=True, blank=True)
