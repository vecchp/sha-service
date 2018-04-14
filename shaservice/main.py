#!/usr/bin/env python3
from gevent import monkey
monkey.patch_all()

import os
import logging

import connexion
from connexion.resolver import RestyResolver

logging.basicConfig(level=logging.INFO)

app = connexion.FlaskApp(
    __name__,
    specification_dir='swagger/'
)

app.add_api(
    'message.yaml',
    resolver=RestyResolver('shaservice.api'),
    strict_validation=True
)


if __name__ == '__main__':
    app.run(server='gevent', host='0.0.0.0')
