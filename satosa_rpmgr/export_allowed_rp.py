import argparse
import yaml
from pathlib import Path

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
    return Path(settings.BASE_DIR, 'export', 'custom_routing_DecideIfRequesterIsAllowed.yaml')


def allowed_requesters_config(idp_entityid: str, sp_entityids: list) -> dict:
    return \
        {'module': 'satosa.micro_services.custom_routing.DecideIfRequesterIsAllowed',
            'name': 'RequesterDecider',
            'config': {
                'rules': {
                    idp_entityid: {
                        'allow': sp_entityids,
                        'deny': ['*']
                    }
                }
            }
        }


def main():
    parser = argparse.ArgumentParser(description='Export allowed RP (basedir/export/custom_routing_DecideIfRequesterIsAllowed.yaml')
    parser.add_argument('--entityid', type=str, help='Backend IDP entityID')
    args = parser.parse_args()
    yaml_str = export_allowed_rp(args.entityid)
    allowed_requesters_path().write_text(yaml_str)


if __name__ == '__main__':
    main()
