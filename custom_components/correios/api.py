import hashlib
import datetime
import json
import logging
import requests
from homeassistant.core import HomeAssistant
from .const import DOMAIN,APP_CHECK_TOKEN,BASE_API,BASE_API_TOKEN
import jwt
import asyncio

_LOGGER = logging.getLogger(__name__)

class Api:
    def __init__(self,hass:HomeAssistant) -> None:
        self.hass = hass
        self.lock = asyncio.Lock()

    def __salvar_token__(self,token) -> None:
        self.hass.data[DOMAIN][APP_CHECK_TOKEN] = token

    def __pegar_token__(self) -> str:
        return self.hass.data[DOMAIN][APP_CHECK_TOKEN]

    def __token_eh_valido__(self) -> bool:
        try:
            jwt.decode(self.__pegar_token__(),options={"verify_signature": False,"verify_exp": True})
            return True
        except:
            _LOGGER.debug("Token expirado")
            return False

    async def async_create_token(self) -> None:
        if self.__pegar_token__() is not None and self.__token_eh_valido__():
            _LOGGER.debug("Token já existe e está válido")
            return

        def get():
            request_token = "TRGNOE/XSv2mcEzJIuh+eXjFWv1LjOLcNKzL5ICRWp47LRFomeLTVPU3wbdBrBb5QL0bkVdJq0ioQeR1lQsrD4jA0fbgJX34p6RbShNNAZp2JiCLcnmHxrCM6z8hl6+Xgx9RwcwQMZMnACyKzY4xr45soDZAgbyLSJOxX/AEXkOMTfEWtVP+8DwU0DQZWxrlvhyzc0nQ2g7cjj9l/9a+WdFAwMRfUKwiHzUOkx8zLOSFFhqEmyRi45sMtKwCLaaV/yr9vVZ6A/4MzSc7TSRwnvQEB510SM/f6Xi9VHL77wQVUGNzRBc/D7yQmtw6/StdwNgOt3oZNUDniUj+6kQUpQ=="
            data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            hash_object = hashlib.md5()
            hash_object.update(f"requestToken{request_token}data{data}".encode())
            sign = hash_object.hexdigest()

            json_data = {
                "sign": sign,
                "data": data,
                "requestToken": request_token
            }

            headers = {"Content-type": "application/json","User-Agent": "Dart/2.18 (dart:io)"}
            response = requests.post(BASE_API_TOKEN,data=json.dumps(json_data),headers=headers)

            return json.loads(response.text)["token"]

        _LOGGER.debug("Gerando token")

        response = await self.hass.async_add_executor_job(get)
        self.__salvar_token__(response)

    async def rastrear(self,codigo_rastreio: str) -> any:
        async with self.lock:
            await self.async_create_token()

        def get():
            headers = {"Content-type": "application/json","User-Agent": "Dart/2.18 (dart:io)"}
            headers[APP_CHECK_TOKEN] = self.__pegar_token__()

            response = requests.get(f"{BASE_API}{codigo_rastreio}",headers=headers)

            data = json.loads(response.text)

            return data

        _LOGGER.debug(f"Pesquisando código de rastreio ==> {codigo_rastreio}")

        response = await self.hass.async_add_executor_job(get)

        return response