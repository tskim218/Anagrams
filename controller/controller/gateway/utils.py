import os

from nameko.standalone.rpc import ServiceRpcProxy
from flask import current_app

def rpcProxy(service):
    config = {'AMQP_URI': current_app.config['AMQP_URI']}

    return ServiceRpcProxy(service, config)