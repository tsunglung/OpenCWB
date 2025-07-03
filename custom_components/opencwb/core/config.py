#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .commons.enums import SubscriptionTypeEnum

DEFAULT_CONFIG = {
    'subscription_type': SubscriptionTypeEnum.FREE,
    'language': 'en',
    'connection': {
        'use_ssl': True,
        'verify_ssl_certs': False,
        'use_proxy': False,
        'timeout_secs': 5
    },
    'proxies': {
        'http': 'http://user:pass@host:port',
        'https': 'socks5://user:pass@host:port'
    }
}
