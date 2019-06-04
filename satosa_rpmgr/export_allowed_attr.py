import argparse
import yaml
from typing import List
from pathlib import Path

import django
django.setup()
from satosa_rpmgr.models import RelyingParty
from django.conf import settings


def export_allowed_attr(idp_entityid: str):
    sp_entityids = []
    for rp in RelyingParty.objects.all():
        sp_entityids.append(rp.entityID)
    yaml_str = allowed_requesters_config(idp_entityid, sp_entityids)
    return(yaml.dump(yaml_str))


def allowed_requesters_path() -> Path:
    return Path(settings.BASE_DIR, 'export', 'attribute_authz.yaml')


def allowed_requesters_config(idp_entityid: str, sp_entity_attr: List[str]) -> dict:
    return {
        'module': 'satosa.micro_services.attribute_authorization.AttributeAuthorization',
        'name': 'AttributeAuthorization',
        'config': {
            'attribute_allow': {
                idp_entityid:
                    sp_entity_attr
            }
        }
    }


def main():
    parser = argparse.ArgumentParser(description='Export allowed attributes per RP (basedir/export/attribute_authz.yaml')
    parser.add_argument('--entityid', type=str, help='Backend IDP entityID')
    args = parser.parse_args()
    yaml_str = export_allowed_attr(args.entityid)
    allowed_requesters_path().write_text(yaml_str)


if __name__ == '__main__':
    main()
