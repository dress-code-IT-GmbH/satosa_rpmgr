from pathlib import Path
import yaml

import django
django.setup()
from satosa_rpmgr.models import RelyingParty
from django.conf import settings


def export_allowed_rp(idp_entityid: str):
    sp_entityids = []
    for rp in RelyingParty.objects.all():
        sp_entityids.append(rp.entityID)
    yaml_str = allowed_requesters_config(idp_entityid, sp_entityids)
    return(yaml.dump(yaml_str))


def allowed_requesters_path() -> Path:
    return Path(settings.BASE_DIR, 'export', 'allowed_requesters.yaml')


def allowed_requesters_config(idp_entityid: str, sp_entityids: list) -> dict:
    return \
        {'module': 'satosa.micro_services.custom_routing.DecideIfRequesterIsAllowed',
            'name': 'RequesterDecider',
            'config': {
                'rules': {
                    idp_entityid: {
                        'allow': [sp_entityids],
                        'deny': ['*']
                    }
                }
            }
        }
