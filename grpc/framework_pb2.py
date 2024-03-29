# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: framework.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='framework.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0f\x66ramework.proto\"\x97\x01\n\nSerialRead\x12\r\n\x05lines\x18\x01 \x03(\t\x12\x11\n\tdevice_id\x18\x02 \x01(\t\x12\x13\n\x0bserial_port\x18\x03 \x01(\t\x12\x12\n\nsession_id\x18\x04 \x01(\t\x12\x14\n\x0chostagent_id\x18\x05 \x01(\t\x12\x11\n\terror_set\x18\x06 \x01(\x08\x12\x15\n\rerror_message\x18\x07 \x01(\t\"6\n\x0cSerialDevice\x12\x11\n\tdevice_id\x18\x01 \x01(\t\x12\x13\n\x0bserial_name\x18\x02 \x01(\t\":\n\x0bSerialWrite\x12\x1d\n\x06\x64\x65vice\x18\x01 \x01(\x0b\x32\r.SerialDevice\x12\x0c\n\x04line\x18\x02 \x01(\t\"\xc7\x01\n\tSerialCmd\x12\x1d\n\x06\x64\x65vice\x18\x01 \x01(\x0b\x32\r.SerialDevice\x12&\n\x07\x63ommand\x18\x02 \x01(\x0e\x32\x15.SerialCmd.SERIAL_CMD\x12\x0f\n\x07user_id\x18\x03 \x01(\t\"b\n\nSERIAL_CMD\x12\x12\n\x0eSERIAL_CONNECT\x10\x00\x12\x15\n\x11SERIAL_DISCONNECT\x10\x01\x12\x17\n\x13SERIAL_DEVICE_RESET\x10\x02\x12\x10\n\x0cSERIAL_RESET\x10\x03\"\xe5\x01\n\x0bSerialEvent\x12\x1d\n\x06\x64\x65vice\x18\x01 \x01(\x0b\x32\r.SerialDevice\x12(\n\x05\x65vent\x18\x02 \x01(\x0e\x32\x19.SerialEvent.SERIAL_EVENT\"\x8c\x01\n\x0cSERIAL_EVENT\x12\x18\n\x14SERIAL_NOT_AVAILABLE\x10\x00\x12\x14\n\x10SERIAL_CONNECTED\x10\x01\x12\x17\n\x13SERIAL_DISCONNECTED\x10\x02\x12\x15\n\x11SERIAL_RESET_DONE\x10\x03\x12\x1c\n\x18SERIAL_DEVICE_RESET_DONE\x10\x04\" \n\x0bSyncRequest\x12\x11\n\tdevice_id\x18\x01 \x03(\t\"|\n\nDeviceInfo\x12\x11\n\tdevice_id\x18\x01 \x01(\t\x12)\n\rdevice_status\x18\x03 \x01(\x0e\x32\x12.DeviceInfo.Status\"0\n\x06Status\x12\x10\n\x0c\x44\x45VICE_FOUND\x10\x00\x12\x14\n\x10\x44\x45VICE_NOT_FOUND\x10\x01\"B\n\x0cSyncResponse\x12\x14\n\x0chostagent_id\x18\x01 \x01(\t\x12\x1c\n\x07\x64\x65vices\x18\x02 \x03(\x0b\x32\x0b.DeviceInfo\"R\n\x0b\x44\x65viceImage\x12\x10\n\x08\x61gent_id\x18\x01 \x01(\t\x12\x11\n\tdevice_id\x18\x02 \x01(\t\x12\x0c\n\x04\x62lob\x18\x03 \x01(\x0c\x12\x10\n\x08\x63hecksum\x18\x04 \x01(\x0c\"\xe8\x01\n\x0eUploadResponse\x12\x11\n\tdevice_id\x18\x01 \x01(\t\x12\x37\n\x0f\x64ownload_status\x18\x02 \x01(\x0e\x32\x1e.UploadResponse.DownloadStatus\"\x89\x01\n\x0e\x44ownloadStatus\x12\x16\n\x12\x44OWNLOAD_COMPLETED\x10\x00\x12\x1d\n\x19\x44OWNLOAD_DEVICE_NOT_FOUND\x10\x01\x12%\n!DOWNLOAD_IMAGE_CHECKSUM_NOT_VALID\x10\x02\x12\x19\n\x15\x44OWNLOAD_DEVICE_ERROR\x10\x03\x32\x8d\x01\n\x0cRemoteSerial\x12)\n\treadLines\x12\r.SerialDevice\x1a\x0b.SerialRead\"\x00\x12(\n\tWriteLine\x12\x0c.SerialWrite\x1a\x0b.SerialRead\"\x00\x12(\n\x06Invoke\x12\n.SerialCmd\x1a\x0c.SerialEvent\"\x00(\x01\x30\x01\x32\x34\n\x0b\x44\x65viceAgent\x12%\n\x04sync\x12\x0c.SyncRequest\x1a\r.SyncResponse\"\x00\x32>\n\x11\x44\x65viceImageUpload\x12)\n\x06upload\x12\x0c.DeviceImage\x1a\x0f.UploadResponse\"\x00\x62\x06proto3')
)



_SERIALCMD_SERIAL_CMD = _descriptor.EnumDescriptor(
  name='SERIAL_CMD',
  full_name='SerialCmd.SERIAL_CMD',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SERIAL_CONNECT', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERIAL_DISCONNECT', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERIAL_DEVICE_RESET', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERIAL_RESET', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=391,
  serialized_end=489,
)
_sym_db.RegisterEnumDescriptor(_SERIALCMD_SERIAL_CMD)

_SERIALEVENT_SERIAL_EVENT = _descriptor.EnumDescriptor(
  name='SERIAL_EVENT',
  full_name='SerialEvent.SERIAL_EVENT',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SERIAL_NOT_AVAILABLE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERIAL_CONNECTED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERIAL_DISCONNECTED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERIAL_RESET_DONE', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SERIAL_DEVICE_RESET_DONE', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=581,
  serialized_end=721,
)
_sym_db.RegisterEnumDescriptor(_SERIALEVENT_SERIAL_EVENT)

_DEVICEINFO_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='DeviceInfo.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DEVICE_FOUND', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_NOT_FOUND', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=833,
  serialized_end=881,
)
_sym_db.RegisterEnumDescriptor(_DEVICEINFO_STATUS)

_UPLOADRESPONSE_DOWNLOADSTATUS = _descriptor.EnumDescriptor(
  name='DownloadStatus',
  full_name='UploadResponse.DownloadStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DOWNLOAD_COMPLETED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOWNLOAD_DEVICE_NOT_FOUND', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOWNLOAD_IMAGE_CHECKSUM_NOT_VALID', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOWNLOAD_DEVICE_ERROR', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1131,
  serialized_end=1268,
)
_sym_db.RegisterEnumDescriptor(_UPLOADRESPONSE_DOWNLOADSTATUS)


_SERIALREAD = _descriptor.Descriptor(
  name='SerialRead',
  full_name='SerialRead',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lines', full_name='SerialRead.lines', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_id', full_name='SerialRead.device_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='serial_port', full_name='SerialRead.serial_port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='session_id', full_name='SerialRead.session_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hostagent_id', full_name='SerialRead.hostagent_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error_set', full_name='SerialRead.error_set', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error_message', full_name='SerialRead.error_message', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=171,
)


_SERIALDEVICE = _descriptor.Descriptor(
  name='SerialDevice',
  full_name='SerialDevice',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_id', full_name='SerialDevice.device_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='serial_name', full_name='SerialDevice.serial_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=173,
  serialized_end=227,
)


_SERIALWRITE = _descriptor.Descriptor(
  name='SerialWrite',
  full_name='SerialWrite',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device', full_name='SerialWrite.device', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='line', full_name='SerialWrite.line', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=229,
  serialized_end=287,
)


_SERIALCMD = _descriptor.Descriptor(
  name='SerialCmd',
  full_name='SerialCmd',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device', full_name='SerialCmd.device', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='command', full_name='SerialCmd.command', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='SerialCmd.user_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SERIALCMD_SERIAL_CMD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=290,
  serialized_end=489,
)


_SERIALEVENT = _descriptor.Descriptor(
  name='SerialEvent',
  full_name='SerialEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device', full_name='SerialEvent.device', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='event', full_name='SerialEvent.event', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SERIALEVENT_SERIAL_EVENT,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=492,
  serialized_end=721,
)


_SYNCREQUEST = _descriptor.Descriptor(
  name='SyncRequest',
  full_name='SyncRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_id', full_name='SyncRequest.device_id', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=723,
  serialized_end=755,
)


_DEVICEINFO = _descriptor.Descriptor(
  name='DeviceInfo',
  full_name='DeviceInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_id', full_name='DeviceInfo.device_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_status', full_name='DeviceInfo.device_status', index=1,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DEVICEINFO_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=757,
  serialized_end=881,
)


_SYNCRESPONSE = _descriptor.Descriptor(
  name='SyncResponse',
  full_name='SyncResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='hostagent_id', full_name='SyncResponse.hostagent_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='devices', full_name='SyncResponse.devices', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=883,
  serialized_end=949,
)


_DEVICEIMAGE = _descriptor.Descriptor(
  name='DeviceImage',
  full_name='DeviceImage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='agent_id', full_name='DeviceImage.agent_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_id', full_name='DeviceImage.device_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='blob', full_name='DeviceImage.blob', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='checksum', full_name='DeviceImage.checksum', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=951,
  serialized_end=1033,
)


_UPLOADRESPONSE = _descriptor.Descriptor(
  name='UploadResponse',
  full_name='UploadResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_id', full_name='UploadResponse.device_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='download_status', full_name='UploadResponse.download_status', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _UPLOADRESPONSE_DOWNLOADSTATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1036,
  serialized_end=1268,
)

_SERIALWRITE.fields_by_name['device'].message_type = _SERIALDEVICE
_SERIALCMD.fields_by_name['device'].message_type = _SERIALDEVICE
_SERIALCMD.fields_by_name['command'].enum_type = _SERIALCMD_SERIAL_CMD
_SERIALCMD_SERIAL_CMD.containing_type = _SERIALCMD
_SERIALEVENT.fields_by_name['device'].message_type = _SERIALDEVICE
_SERIALEVENT.fields_by_name['event'].enum_type = _SERIALEVENT_SERIAL_EVENT
_SERIALEVENT_SERIAL_EVENT.containing_type = _SERIALEVENT
_DEVICEINFO.fields_by_name['device_status'].enum_type = _DEVICEINFO_STATUS
_DEVICEINFO_STATUS.containing_type = _DEVICEINFO
_SYNCRESPONSE.fields_by_name['devices'].message_type = _DEVICEINFO
_UPLOADRESPONSE.fields_by_name['download_status'].enum_type = _UPLOADRESPONSE_DOWNLOADSTATUS
_UPLOADRESPONSE_DOWNLOADSTATUS.containing_type = _UPLOADRESPONSE
DESCRIPTOR.message_types_by_name['SerialRead'] = _SERIALREAD
DESCRIPTOR.message_types_by_name['SerialDevice'] = _SERIALDEVICE
DESCRIPTOR.message_types_by_name['SerialWrite'] = _SERIALWRITE
DESCRIPTOR.message_types_by_name['SerialCmd'] = _SERIALCMD
DESCRIPTOR.message_types_by_name['SerialEvent'] = _SERIALEVENT
DESCRIPTOR.message_types_by_name['SyncRequest'] = _SYNCREQUEST
DESCRIPTOR.message_types_by_name['DeviceInfo'] = _DEVICEINFO
DESCRIPTOR.message_types_by_name['SyncResponse'] = _SYNCRESPONSE
DESCRIPTOR.message_types_by_name['DeviceImage'] = _DEVICEIMAGE
DESCRIPTOR.message_types_by_name['UploadResponse'] = _UPLOADRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SerialRead = _reflection.GeneratedProtocolMessageType('SerialRead', (_message.Message,), dict(
  DESCRIPTOR = _SERIALREAD,
  __module__ = 'framework_pb2'
  # @@protoc_insertion_point(class_scope:SerialRead)
  ))
_sym_db.RegisterMessage(SerialRead)

SerialDevice = _reflection.GeneratedProtocolMessageType('SerialDevice', (_message.Message,), dict(
  DESCRIPTOR = _SERIALDEVICE,
  __module__ = 'framework_pb2'
  # @@protoc_insertion_point(class_scope:SerialDevice)
  ))
_sym_db.RegisterMessage(SerialDevice)

SerialWrite = _reflection.GeneratedProtocolMessageType('SerialWrite', (_message.Message,), dict(
  DESCRIPTOR = _SERIALWRITE,
  __module__ = 'framework_pb2'
  # @@protoc_insertion_point(class_scope:SerialWrite)
  ))
_sym_db.RegisterMessage(SerialWrite)

SerialCmd = _reflection.GeneratedProtocolMessageType('SerialCmd', (_message.Message,), dict(
  DESCRIPTOR = _SERIALCMD,
  __module__ = 'framework_pb2'
  # @@protoc_insertion_point(class_scope:SerialCmd)
  ))
_sym_db.RegisterMessage(SerialCmd)

SerialEvent = _reflection.GeneratedProtocolMessageType('SerialEvent', (_message.Message,), dict(
  DESCRIPTOR = _SERIALEVENT,
  __module__ = 'framework_pb2'
  # @@protoc_insertion_point(class_scope:SerialEvent)
  ))
_sym_db.RegisterMessage(SerialEvent)

SyncRequest = _reflection.GeneratedProtocolMessageType('SyncRequest', (_message.Message,), dict(
  DESCRIPTOR = _SYNCREQUEST,
  __module__ = 'framework_pb2'
  # @@protoc_insertion_point(class_scope:SyncRequest)
  ))
_sym_db.RegisterMessage(SyncRequest)

DeviceInfo = _reflection.GeneratedProtocolMessageType('DeviceInfo', (_message.Message,), dict(
  DESCRIPTOR = _DEVICEINFO,
  __module__ = 'framework_pb2'
  # @@protoc_insertion_point(class_scope:DeviceInfo)
  ))
_sym_db.RegisterMessage(DeviceInfo)

SyncResponse = _reflection.GeneratedProtocolMessageType('SyncResponse', (_message.Message,), dict(
  DESCRIPTOR = _SYNCRESPONSE,
  __module__ = 'framework_pb2'
  # @@protoc_insertion_point(class_scope:SyncResponse)
  ))
_sym_db.RegisterMessage(SyncResponse)

DeviceImage = _reflection.GeneratedProtocolMessageType('DeviceImage', (_message.Message,), dict(
  DESCRIPTOR = _DEVICEIMAGE,
  __module__ = 'framework_pb2'
  # @@protoc_insertion_point(class_scope:DeviceImage)
  ))
_sym_db.RegisterMessage(DeviceImage)

UploadResponse = _reflection.GeneratedProtocolMessageType('UploadResponse', (_message.Message,), dict(
  DESCRIPTOR = _UPLOADRESPONSE,
  __module__ = 'framework_pb2'
  # @@protoc_insertion_point(class_scope:UploadResponse)
  ))
_sym_db.RegisterMessage(UploadResponse)



_REMOTESERIAL = _descriptor.ServiceDescriptor(
  name='RemoteSerial',
  full_name='RemoteSerial',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1271,
  serialized_end=1412,
  methods=[
  _descriptor.MethodDescriptor(
    name='readLines',
    full_name='RemoteSerial.readLines',
    index=0,
    containing_service=None,
    input_type=_SERIALDEVICE,
    output_type=_SERIALREAD,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='WriteLine',
    full_name='RemoteSerial.WriteLine',
    index=1,
    containing_service=None,
    input_type=_SERIALWRITE,
    output_type=_SERIALREAD,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Invoke',
    full_name='RemoteSerial.Invoke',
    index=2,
    containing_service=None,
    input_type=_SERIALCMD,
    output_type=_SERIALEVENT,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_REMOTESERIAL)

DESCRIPTOR.services_by_name['RemoteSerial'] = _REMOTESERIAL


_DEVICEAGENT = _descriptor.ServiceDescriptor(
  name='DeviceAgent',
  full_name='DeviceAgent',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=1414,
  serialized_end=1466,
  methods=[
  _descriptor.MethodDescriptor(
    name='sync',
    full_name='DeviceAgent.sync',
    index=0,
    containing_service=None,
    input_type=_SYNCREQUEST,
    output_type=_SYNCRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_DEVICEAGENT)

DESCRIPTOR.services_by_name['DeviceAgent'] = _DEVICEAGENT


_DEVICEIMAGEUPLOAD = _descriptor.ServiceDescriptor(
  name='DeviceImageUpload',
  full_name='DeviceImageUpload',
  file=DESCRIPTOR,
  index=2,
  serialized_options=None,
  serialized_start=1468,
  serialized_end=1530,
  methods=[
  _descriptor.MethodDescriptor(
    name='upload',
    full_name='DeviceImageUpload.upload',
    index=0,
    containing_service=None,
    input_type=_DEVICEIMAGE,
    output_type=_UPLOADRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_DEVICEIMAGEUPLOAD)

DESCRIPTOR.services_by_name['DeviceImageUpload'] = _DEVICEIMAGEUPLOAD

# @@protoc_insertion_point(module_scope)
