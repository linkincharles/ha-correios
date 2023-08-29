"""Constants for the Correios integration."""
from typing import Final

from homeassistant.const import Platform

APP_CHECK_TOKEN:Final = "app-check-token"
DOMAIN: Final = "correios"
PLATFORMS: Final = [Platform.SENSOR]

DEFAULT_NAME: Final = "Rastreamento Correios"

CONF_TRACKING = "track"
CONF_DESCRIPTION = "description"
DEFAULT_DESCRIPTION: Final = "Encomenda"

ICON = "mdi:box-variant-closed"
BASE_API = "https://proxyapp.correios.com.br/v1/sro-rastro/"
BASE_API_TOKEN = "https://proxyapp.correios.com.br/v3/app-validation"
