import json
from urllib.parse import urlparse
from django.db import models


class RelyingParty(models.Model):
    class Meta:
        ordering = ['entity_fqdn']
        verbose_name_plural = 'RelyingParties'

    owner_cn = models.CharField(
        blank=True, null=True,
        verbose_name='Auftragg. kurz',
        max_length=10)
    owner_name = models.CharField(
        blank=True, null=True,
        verbose_name='Auftraggeber lang',
        max_length=120)
    entityID = models.CharField(
        unique=True,
        blank=True, null=True, default='',
        max_length=101)
    zone_p = models.BooleanField(
        default=False,
        verbose_name='Zone-Prod',
    )
    zone_q = models.BooleanField(
        default=False,
        verbose_name='Zone-QS',
    )
    zone_t = models.BooleanField(
        default=False,
        verbose_name='Zone-Test',
    )
    zone_d = models.BooleanField(
        default=False,
        verbose_name='Zone-Dev',
    )
    entity_fqdn = models.CharField(
        blank=True, null=True,
        verbose_name='Entity FQDN',
        max_length=115)
    admin_note = models.TextField(
        blank=True, null=True,
        verbose_name='Admin Notiz',
        max_length=1000)
    status = models.BooleanField(
        default=False,
        verbose_name='aktiv',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum', )

    @property
    def updated(self):
        return self.updated_at.strftime("%Y%m%d %H:%M")

# -------
    def serialize_json(self) -> str:
        """ serialize stable values """
        dictfilt = lambda d, filter: dict([(k, d[k]) for k in d if k in set(filter)])
        wanted_keys = (
            'admin_note',
            'created_at',
            'entity_fqdn',
            'entityID',
            'owner_cn',
            'owner_name',
            'status',
            'updated_at',
            'zone_d',
            'zone_p',
            'zone_q',
            'zone_t',
        )
        self_dict = dictfilt(self.__dict__, wanted_keys)
        return json.dumps(self_dict, sort_keys=True, indent=2)

    def __str__(self):
        s = (self.entityID or self._get_make_blank_entityid_unique() or '')
        return s

    def __repr__(self):
        r = f"{self.entityID} {self.statusgroup} {self._get_make_blank_entityid_unique()}"
        return r

    def save(self, *args, **kwargs):
        uri_components = urlparse(self.entityID)
        self.entity_fqdn = uri_components.netloc or uri_components.path
        super().save(*args, **kwargs)
