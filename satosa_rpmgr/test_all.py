from pathlib import Path
import pytest
import django
from satosa_rpmgr.export_allowed_rp import export_allowed_rp
from satosa_rpmgr.models import RelyingParty

django.setup()

@pytest.fixture(scope='session')
# pettern: https://pytest-django.readthedocs.io/en/latest/database.html#populate-the-database-with-initial-test-data
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        fixture_path = Path('fixtures/wpv_test_init.json')
        assert fixture_path.is_file(), f"could not find file {fixture_path}"
        django.core.management.call_command('loaddata', fixture_path)


@pytest.mark.django_db
def test_model_query(django_db_setup):
    q = RelyingParty.objects.all()
    assert len(q) == 4


@pytest.mark.django_db
def test_export_allowed_rp(django_db_setup):
    yaml_str = export_allowed_rp('https://idp1.test.wpv.portalverbund.at/idp/shibboleth')
    expected_result_path = Path('testresults/allowed_requesters.yaml')
    assert yaml_str == expected_result_path.read_text()


