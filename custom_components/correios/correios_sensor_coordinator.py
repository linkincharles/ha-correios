from datetime import timedelta
from random import randrange
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import logging

from .api import Api
from .const import DOMAIN,CONF_TRACKING

_LOGGER = logging.getLogger(__name__)


class CorreiosSensorCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        self.api = hass.data[DOMAIN]["Api"] # Api(hass=hass)
        self.codigo_rastreio = config_entry.data.get(CONF_TRACKING)
        update_interval = timedelta(minutes=randrange(30,45))
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def _async_update_data(self) -> dict:
        return await self.api.rastrear(self.codigo_rastreio)
