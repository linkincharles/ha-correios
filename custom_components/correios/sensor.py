"""
A platform that provides information about the tracking of objects in the post office in Brazil
For more details about this component, please refer to the documentation at
https://github.com/luyzfernando08/ha-correios
"""

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.typing import UndefinedType

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .correios_sensor_coordinator import CorreiosSensorCoordinator

from .const import (
    CONF_TRACKING,
    CONF_DESCRIPTION,
    DOMAIN,
    ICON,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Correios sensor"""
    track = entry.data[CONF_TRACKING]
    nome_objeto = entry.data[CONF_DESCRIPTION]
    coordinator = CorreiosSensorCoordinator(hass=hass,config_entry=entry)
    async_add_entities([CorreiosSensor(coordinator,hass,track,nome_objeto)],True,)


class CorreiosSensor(CoordinatorEntity[CorreiosSensorCoordinator], SensorEntity):
    def __init__(
        self,
        coordinator: CorreiosSensorCoordinator,
        hass: HomeAssistant,
        track: str,
        nome_objeto: str
    ):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.hass = hass
        self.track = track
        self._name = f"Correios - {nome_objeto}"
        self.nome_objeto = nome_objeto

    def __objeto_existe__(self) -> bool:
        return "mensagem" not in self.__get_objeto__()

    def __get_objeto__(self) -> dict:
        return self.coordinator.data["objetos"][0]

    def __get_eventos__(self) -> list:
        return self.__get_objeto__()["eventos"]

    def __get_ultimo_evento__(self) -> dict:
        return self.__get_eventos__()[0]

    def __get_ultimo_evento_com_parametro__(self,parametro: str) -> dict:
        return self.__get_ultimo_evento__()[parametro]

    @property
    def name(self) -> str | UndefinedType | None:
        return self._name

    @property
    def unique_id(self) -> str:
        return f"correios_{self.track}"

    @property
    def entity_picture(self):
        return "https://rastreamento.correios.com.br/static/rastreamento-internet/imgs/correios-sf.png" #self._image

    @property
    def state(self):
        if self.__objeto_existe__():
            return self.__get_ultimo_evento_com_parametro__("descricao")
        else:
            return self.__get_objeto__()["mensagem"]

    @property
    def icon(self):
        return ICON

    @property
    def extra_state_attributes(self):
        if self.__objeto_existe__():
             origem = "-"
             destino = "-"

             if "nome" in self.__get_ultimo_evento_com_parametro__("unidade"):
                 origem =  self.__get_ultimo_evento_com_parametro__("unidade")["nome"]

             if "unidadeDestino" in self.__get_ultimo_evento__():
                if "nome" in self.__get_ultimo_evento_com_parametro__("unidadeDestino"):
                    destino =  self.__get_ultimo_evento_com_parametro__("unidadeDestino")["nome"]


             return {
                "Nome": self.nome_objeto,
                "Status": self.__get_ultimo_evento_com_parametro__("descricao"),
                "Código Objeto": self.track,
                "Origem": origem,
                "Destino": destino,
                "Última Movimentação": self.__get_ultimo_evento_com_parametro__("dtHrCriado"),
                "Tipo Postal": self.__get_objeto__()["tipoPostal"]["categoria"],
                # "Movimentações": self.trackings,
            }
        else:
            return {}


    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(
            entry_type=dr.DeviceEntryType.SERVICE,
            connections=None,
            identifiers={(DOMAIN,)},
            manufacturer="Correios",
            name=self.track,
            model="Não aplicável",
            sw_version=None,
            hw_version=None,
        )
