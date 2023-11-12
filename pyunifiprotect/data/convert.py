"""UniFi Protect Data Conversion."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Type

from pyunifiprotect.data.devices import Bridge, Camera, Doorlock, Light, Sensor, Viewer
from pyunifiprotect.data.nvr import NVR, Event, Liveview
from pyunifiprotect.data.types import ModelType
from pyunifiprotect.data.user import CloudAccount, Group, User, UserLocation
from pyunifiprotect.exceptions import DataDecodeError

if TYPE_CHECKING:
    from pyunifiprotect.api import ProtectApiClient
    from pyunifiprotect.data.base import ProtectModel


MODEL_TO_CLASS: Dict[str, Type[ProtectModel]] = {
    ModelType.EVENT: Event,
    ModelType.GROUP: Group,
    ModelType.USER_LOCATION: UserLocation,
    ModelType.CLOUD_IDENTITY: CloudAccount,
    ModelType.USER: User,
    ModelType.NVR: NVR,
    ModelType.LIGHT: Light,
    ModelType.CAMERA: Camera,
    ModelType.LIVEVIEW: Liveview,
    ModelType.VIEWPORT: Viewer,
    ModelType.BRIDGE: Bridge,
    ModelType.SENSOR: Sensor,
    ModelType.DOORLOCK: Doorlock,
}


def get_klass_from_dict(data: Dict[str, Any]) -> Type[ProtectModel]:
    """
    Helper method to read the model key from a UFP JSON dict and get the correct Python class for conversion.
    Will raise `DataDecodeError` if the model key is for an unknown object.
    """

    if "modelkey" in data:
        modelkey = data["modelkey"]
    elif "modelKey" in data:
        modelkey = data["modelKey"]
    else:
        raise DataDecodeError("No model key")

    model = ModelType(modelkey)

    klass = MODEL_TO_CLASS.get(model)

    if klass is None:
        raise DataDecodeError("Unknown model key")

    return klass


def create_from_unifi_dict(
    data: Dict[str, Any], api: Optional[ProtectApiClient] = None, klass: Optional[Type[ProtectModel]] = None
) -> ProtectModel:
    """
    Helper method to read the model key from a UFP JSON dict and convert to currect Python class.
    Will raise `DataDecodeError` if the model key is for an unknown object.
    """

    if "modelkey" not in data and "modelKey" not in data:
        raise DataDecodeError("No model key")

    if klass is None:
        klass = get_klass_from_dict(data)

    return klass.from_unifi_dict(**data, api=api)
