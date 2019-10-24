import argparse
import yaml
from pathlib import Path

import django
django.setup()
from satosa_rpmgr.models import RelyingParty
from django.conf import settings


def main():
    yaml_str = _export_allowed_rp()
    _allowed_requesters_path().write_text(yaml_str)


def _export_allowed_rp():
    sp_entityids = []
    for rp in RelyingParty.objects.all():
        sp_entityids.append(rp.entityID)
    if len(sp_entityids) == 0:
        raise Exception('List of allowed requesters must not be empty. Add "*" to allow any SP.')
    yaml_str = allowed_requesters_config(sp_entityids)
    return(yaml.dump(yaml_str))


def _allowed_requesters_path() -> Path:
    return Path(settings.BASE_DIR, 'export', 'filter_requester.yaml')


def allowed_requesters_config(sp_entityids: list) -> dict:
    return {
        'config': {
            'allow': sp_entityids,
         },
         'module': 'satosa.micro_services.filter_requester.FilterRequester',
         'name': 'FilterRequester',

    }


if __name__ == '__main__':
    main()
