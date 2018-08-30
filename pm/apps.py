from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MtasksConfig(AppConfig):
    name = 'pm'
    verbose_name = _('项目管理')
