from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetLocationsBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IDENTIFIER: _ClassVar[GetLocationsBy]
    INTERVAL: _ClassVar[GetLocationsBy]
    N_RECENT: _ClassVar[GetLocationsBy]
    ALL: _ClassVar[GetLocationsBy]
IDENTIFIER: GetLocationsBy
INTERVAL: GetLocationsBy
N_RECENT: GetLocationsBy
ALL: GetLocationsBy

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LogMeasurementRequest(_message.Message):
    __slots__ = ("aid", "imsi", "timestamp", "signal_strength")
    AID_FIELD_NUMBER: _ClassVar[int]
    IMSI_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    aid: int
    imsi: int
    timestamp: float
    signal_strength: float
    def __init__(self, aid: _Optional[int] = ..., imsi: _Optional[int] = ..., timestamp: _Optional[float] = ..., signal_strength: _Optional[float] = ...) -> None: ...

class RegisterAntennaRequest(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class RegisterAntennaResponse(_message.Message):
    __slots__ = ("aid",)
    AID_FIELD_NUMBER: _ClassVar[int]
    aid: int
    def __init__(self, aid: _Optional[int] = ...) -> None: ...

class Antenna(_message.Message):
    __slots__ = ("aid", "x", "y")
    AID_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    aid: int
    x: int
    y: int
    def __init__(self, aid: _Optional[int] = ..., x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class GetAntennasResponse(_message.Message):
    __slots__ = ("antenna",)
    ANTENNA_FIELD_NUMBER: _ClassVar[int]
    antenna: _containers.RepeatedCompositeFieldContainer[Antenna]
    def __init__(self, antenna: _Optional[_Iterable[_Union[Antenna, _Mapping]]] = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ("identifier", "calctime", "x", "y")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CALCTIME_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    identifier: int
    calctime: float
    x: int
    y: int
    def __init__(self, identifier: _Optional[int] = ..., calctime: _Optional[float] = ..., x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class GetLocationsRequest(_message.Message):
    __slots__ = ("method", "identifier", "timeinterval", "n_recent")
    METHOD_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TIMEINTERVAL_FIELD_NUMBER: _ClassVar[int]
    N_RECENT_FIELD_NUMBER: _ClassVar[int]
    method: GetLocationsBy
    identifier: int
    timeinterval: float
    n_recent: int
    def __init__(self, method: _Optional[_Union[GetLocationsBy, str]] = ..., identifier: _Optional[int] = ..., timeinterval: _Optional[float] = ..., n_recent: _Optional[int] = ...) -> None: ...

class GetLocationsResponse(_message.Message):
    __slots__ = ("location",)
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: _containers.RepeatedCompositeFieldContainer[Location]
    def __init__(self, location: _Optional[_Iterable[_Union[Location, _Mapping]]] = ...) -> None: ...

class Measurement(_message.Message):
    __slots__ = ("mid", "aid", "timestamp", "signal_strength")
    MID_FIELD_NUMBER: _ClassVar[int]
    AID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    mid: int
    aid: int
    timestamp: float
    signal_strength: float
    def __init__(self, mid: _Optional[int] = ..., aid: _Optional[int] = ..., timestamp: _Optional[float] = ..., signal_strength: _Optional[float] = ...) -> None: ...

class LocationMeasurementsRequest(_message.Message):
    __slots__ = ("identifier", "calctime")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CALCTIME_FIELD_NUMBER: _ClassVar[int]
    identifier: int
    calctime: float
    def __init__(self, identifier: _Optional[int] = ..., calctime: _Optional[float] = ...) -> None: ...

class LocationMeasurementsResponse(_message.Message):
    __slots__ = ("measurement",)
    MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    measurement: _containers.RepeatedCompositeFieldContainer[Measurement]
    def __init__(self, measurement: _Optional[_Iterable[_Union[Measurement, _Mapping]]] = ...) -> None: ...
