"""
Home Assistant platform that provides information about the tracking of objects in the post office in Brazil.
https://github.com/luyzfernando08/ha-correios
"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import Api

from .const import PLATFORMS,DOMAIN,APP_CHECK_TOKEN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    if APP_CHECK_TOKEN not in hass.data[DOMAIN]:
        hass.data[DOMAIN] = {APP_CHECK_TOKEN: None, "Api" : Api(hass=hass)}
        # hass.data[DOMAIN]["API"] = Api(hass=hass)

    # hass.data[DOMAIN]["Api"].async_create_token()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True