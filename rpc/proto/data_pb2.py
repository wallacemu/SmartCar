# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='data.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\ndata.proto\"7\n\x07ReqData\x12\r\n\x05width\x18\x01 \x01(\x05\x12\x0e\n\x06height\x18\x02 \x01(\x05\x12\r\n\x05image\x18\x03 \x02(\x0c\"\x18\n\x07ResData\x12\r\n\x05logid\x18\x01 \x01(\x05')
)




_REQDATA = _descriptor.Descriptor(
  name='ReqData',
  full_name='ReqData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='width', full_name='ReqData.width', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='height', full_name='ReqData.height', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image', full_name='ReqData.image', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=14,
  serialized_end=69,
)


_RESDATA = _descriptor.Descriptor(
  name='ResData',
  full_name='ResData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='logid', full_name='ResData.logid', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=71,
  serialized_end=95,
)

DESCRIPTOR.message_types_by_name['ReqData'] = _REQDATA
DESCRIPTOR.message_types_by_name['ResData'] = _RESDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ReqData = _reflection.GeneratedProtocolMessageType('ReqData', (_message.Message,), dict(
  DESCRIPTOR = _REQDATA,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:ReqData)
  ))
_sym_db.RegisterMessage(ReqData)

ResData = _reflection.GeneratedProtocolMessageType('ResData', (_message.Message,), dict(
  DESCRIPTOR = _RESDATA,
  __module__ = 'data_pb2'
  # @@protoc_insertion_point(class_scope:ResData)
  ))
_sym_db.RegisterMessage(ResData)


# @@protoc_insertion_point(module_scope)
