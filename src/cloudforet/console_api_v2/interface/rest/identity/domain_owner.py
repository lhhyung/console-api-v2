import logging
from fastapi import Request, Depends, Body
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from spaceone.core.fastapi.api import BaseAPI, exception_handler
from cloudforet.console_api_v2.service.common.proxy_service import ProxyService

_LOGGER = logging.getLogger(__name__)
_AUTH_SCHEME = HTTPBearer()

router = InferringRouter()


@cbv(router)
class DomainOwner(BaseAPI):

    token: HTTPAuthorizationCredentials = Depends(_AUTH_SCHEME)
    service = 'console-api'

    @router.post('/update')
    @exception_handler
    async def update(self, request: Request, body: dict = Body(...)):
        params, metadata = await self.parse_request(request, self.token.credentials)

        with self.locator.get_service(ProxyService, metadata) as proxy_service:
            params['grpc_method'] = 'identity.DomainOwner.update'
            return proxy_service.dispatch_api(params)

    @router.post('/get')
    @exception_handler
    async def get(self, request: Request, body: dict = Body(...)):
        params, metadata = await self.parse_request(request, self.token.credentials)

        with self.locator.get_service(ProxyService, metadata) as proxy_service:
            params['grpc_method'] = 'identity.DomainOwner.get'
            return proxy_service.dispatch_api(params)
