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
            request_token = "WoAH5n3OQui/naI7zBWVOEOLbYx7xlm/yvA9QPGEBW4g2Z9IcshdF7dD7NlPRTrpi6tgZZ88kOQTm6ZE6Q0Wk5LTprrXP2jatpIAr8/1nKWRbwvv9+iSbpTFo18pqLow89197siHy39XrYJDPZj34t0pUx7rFiTEUxAvkbA8GhPDkcB42oaJE9YL8kNezlgzW1Zn7LGEnYQ95uDpm6V69At7Vh/tqrIaLlCPwlMFFoIfvhSF2Etxo4+6EOSjMSubEN7FW378d29UCE6BpRdUnz1viQCyZ4LbIHijtAtczNl+SF0GGpivEi0x6aeFQbq9GGJXdEMiLW/68dT+M3Rx0A=="
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