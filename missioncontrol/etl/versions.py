import requests
from django.core.cache import cache

from missioncontrol.settings import (FIREFOX_VERSION_CACHE_TIMEOUT,
                                     FIREFOX_VERSION_URL)


def get_firefox_versions():
    firefox_versions = cache.get('firefox_versions')
    if firefox_versions:
        return firefox_versions

    # map the version api's to telemetry channel names
    r = requests.get(FIREFOX_VERSION_URL)
    firefox_versions = r.json()
    mapped_versions = {
        'nightly': firefox_versions['FIREFOX_NIGHTLY'],
        'esr': firefox_versions['FIREFOX_ESR'],
        'beta': firefox_versions['LATEST_FIREFOX_DEVEL_VERSION'],
        'release': firefox_versions['LATEST_FIREFOX_VERSION']
    }
    cache.set('firefox_versions', mapped_versions, FIREFOX_VERSION_CACHE_TIMEOUT)

    return mapped_versions


def get_current_firefox_version(channel_name):
    return get_firefox_versions()[channel_name]
