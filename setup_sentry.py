import os
import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


def setup_sentry():
    """Устанавливает соединение с SDK Sentry
    """
    if os.getenv('SENTRY_DSN'):
        sentry_sdk.init(
            dsn=os.getenv('SENTRY_DSN'),
            release=os.getenv('RELEASE', '1'),
            environment=os.getenv('ENVIRONMENT', 'debug'),
            integrations=[
                LoggingIntegration(
                    level=logging.ERROR
                )
            ],
            max_breadcrumbs=os.getenv('MAX_BREADCRUMBS', 10)
        )
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag('thumbnail_extractor', 'tg_bot')
