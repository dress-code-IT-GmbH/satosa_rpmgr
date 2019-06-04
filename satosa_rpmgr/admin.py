from django.contrib import admin
from .models import Attribute, RelyingParty


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_display = ('friendly_name', 'uri_name', )

@admin.register(RelyingParty)
class RelyingPartyAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    readonly_fields = (
        'entity_fqdn',
        'created_at',
        'updated_at',
        'id',
    )
    list_display = (
        'entity_fqdn',
        'owner_cn',
        'status',
        'updated',
        '_get_zones',
    )
    list_display_links = ('entity_fqdn', 'status')
    list_filter = (
        'status',
        'zone_d',
        'zone_p',
        'zone_q',
        'zone_t',
    )
    search_fields = (
        'admin_note',
        'entityID',
        'owner_cn',
        'owner_name',
    )
    fieldsets = (
        ('Entity Deployment', {
            'fields': (
                'entityID',
                'attributes',
                'entity_fqdn',
                'zone_p',
                'zone_q',
                'zone_t',
                'zone_d',
                'status',
            )
        }),
        ('Administrative Attribute', {
            'fields': (
                'owner_cn',
                'owner_name',
                'admin_note',
                ('created_at', 'updated_at', ),
                'id',
            )
        }),
    )
    filter_horizontal = ('attributes',)

    def _get_zones(self, obj) -> str:
        zones = {
            'zone_p': 'Prod',
            'zone_q': 'QS',
            'zone_t': 'Test',
            'zone_d': 'Dev',
        }
        z_str = []
        for k, v in zones.items():
            if getattr(obj, k, False):
                z_str.append(v)
        return ', '.join(z_str)
    _get_zones.short_description = 'Zonen'

    # actions = ['delete_selected', ]
    actions = []
