# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qqsim.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bqqsim.proto\x12\x08qqsim.v1\x1a\x1bgoogle/protobuf/empty.proto\"\x96\x01\n\x14\x43mQsimSimilarRequest\x12\x1a\n\x08\x61gent_id\x18\x01 \x01(\x05R\x08\x61gent_id\x12\x1a\n\x08trace_id\x18\x02 \x01(\tR\x08trace_id\x12\x1d\n\nrobot_name\x18\x03 \x01(\tR\tRobotName\x12\'\n\x05texts\x18\x04 \x03(\x0b\x32\x18.qqsim.v1.TextPairReqMsg\"c\n\x16\x43mQqSimSentenceRequest\x12\x10\n\x08\x61gent_id\x18\x01 \x01(\x05\x12\x10\n\x08trace_id\x18\x02 \x01(\t\x12\x12\n\nrobot_name\x18\x03 \x01(\t\x12\x11\n\ttext_list\x18\x04 \x03(\t\"y\n\x17\x43mQqSimSentenceResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0e\n\x06reason\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\x12/\n\x08metadata\x18\x04 \x01(\x0b\x32\x1d.qqsim.v1.QqSimSentenceResult\"\x95\x01\n\x13QqSimSentenceResult\x12\x11\n\tmodelType\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12<\n\nvectorList\x18\x03 \x03(\x0b\x32(.qqsim.v1.QqSimSentenceResult.VectorList\x1a\x1c\n\nVectorList\x12\x0e\n\x06vector\x18\x01 \x03(\x02\"h\n\x0eTextPairReqMsg\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x16\n\x06text_1\x18\x02 \x01(\tR\x06text_1\x12\x16\n\x06text_2\x18\x03 \x01(\tR\x06text_2\x12\x1a\n\x08\x65s_score\x18\x04 \x01(\x02R\x08\x65s_score\"u\n\x15\x43mQsimSimilarResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0e\n\x06reason\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\x12-\n\x08metadata\x18\x04 \x01(\x0b\x32\x1b.qqsim.v1.QsimSimilarResult\"b\n\x11QsimSimilarResult\x12\x11\n\tmodelType\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12)\n\x07\x61nswers\x18\x03 \x03(\x0b\x32\x18.qqsim.v1.TextPairRspMsg\"K\n\x0eTextPairRspMsg\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0e\n\x06text_1\x18\x02 \x01(\t\x12\x0e\n\x06text_2\x18\x03 \x01(\t\x12\r\n\x05score\x18\x04 \x01(\x02\"\"\n\x0fVersionResponse\x12\x0f\n\x07version\x18\x01 \x01(\t*[\n\tModelType\x12\x12\n\x0eMODEL_TYPE_768\x10\x00\x12\x12\n\x0eMODEL_TYPE_512\x10\x01\x12\x12\n\x0eMODEL_TYPE_256\x10\x02\x12\x12\n\x0eMODEL_TYPE_128\x10\x03\x32\x8b\x02\n\x0cQqsimService\x12S\n\x0e\x43mQqSimSimilar\x12\x1e.qqsim.v1.CmQsimSimilarRequest\x1a\x1f.qqsim.v1.CmQsimSimilarResponse\"\x00\x12^\n\x15\x43mQqSimSentenceEncode\x12 .qqsim.v1.CmQqSimSentenceRequest\x1a!.qqsim.v1.CmQqSimSentenceResponse\"\x00\x12\x46\n\x0fGetQqsimVersion\x12\x16.google.protobuf.Empty\x1a\x19.qqsim.v1.VersionResponse\"\x00\x42\"Z nlp-qqsim-server/api/qqsim/v1;v1b\x06proto3')

_MODELTYPE = DESCRIPTOR.enum_types_by_name['ModelType']
ModelType = enum_type_wrapper.EnumTypeWrapper(_MODELTYPE)
MODEL_TYPE_768 = 0
MODEL_TYPE_512 = 1
MODEL_TYPE_256 = 2
MODEL_TYPE_128 = 3


_CMQSIMSIMILARREQUEST = DESCRIPTOR.message_types_by_name['CmQsimSimilarRequest']
_CMQQSIMSENTENCEREQUEST = DESCRIPTOR.message_types_by_name['CmQqSimSentenceRequest']
_CMQQSIMSENTENCERESPONSE = DESCRIPTOR.message_types_by_name['CmQqSimSentenceResponse']
_QQSIMSENTENCERESULT = DESCRIPTOR.message_types_by_name['QqSimSentenceResult']
_QQSIMSENTENCERESULT_VECTORLIST = _QQSIMSENTENCERESULT.nested_types_by_name['VectorList']
_TEXTPAIRREQMSG = DESCRIPTOR.message_types_by_name['TextPairReqMsg']
_CMQSIMSIMILARRESPONSE = DESCRIPTOR.message_types_by_name['CmQsimSimilarResponse']
_QSIMSIMILARRESULT = DESCRIPTOR.message_types_by_name['QsimSimilarResult']
_TEXTPAIRRSPMSG = DESCRIPTOR.message_types_by_name['TextPairRspMsg']
_VERSIONRESPONSE = DESCRIPTOR.message_types_by_name['VersionResponse']
CmQsimSimilarRequest = _reflection.GeneratedProtocolMessageType('CmQsimSimilarRequest', (_message.Message,), {
  'DESCRIPTOR' : _CMQSIMSIMILARREQUEST,
  '__module__' : 'qqsim_pb2'
  # @@protoc_insertion_point(class_scope:qqsim.v1.CmQsimSimilarRequest)
  })
_sym_db.RegisterMessage(CmQsimSimilarRequest)

CmQqSimSentenceRequest = _reflection.GeneratedProtocolMessageType('CmQqSimSentenceRequest', (_message.Message,), {
  'DESCRIPTOR' : _CMQQSIMSENTENCEREQUEST,
  '__module__' : 'qqsim_pb2'
  # @@protoc_insertion_point(class_scope:qqsim.v1.CmQqSimSentenceRequest)
  })
_sym_db.RegisterMessage(CmQqSimSentenceRequest)

CmQqSimSentenceResponse = _reflection.GeneratedProtocolMessageType('CmQqSimSentenceResponse', (_message.Message,), {
  'DESCRIPTOR' : _CMQQSIMSENTENCERESPONSE,
  '__module__' : 'qqsim_pb2'
  # @@protoc_insertion_point(class_scope:qqsim.v1.CmQqSimSentenceResponse)
  })
_sym_db.RegisterMessage(CmQqSimSentenceResponse)

QqSimSentenceResult = _reflection.GeneratedProtocolMessageType('QqSimSentenceResult', (_message.Message,), {

  'VectorList' : _reflection.GeneratedProtocolMessageType('VectorList', (_message.Message,), {
    'DESCRIPTOR' : _QQSIMSENTENCERESULT_VECTORLIST,
    '__module__' : 'qqsim_pb2'
    # @@protoc_insertion_point(class_scope:qqsim.v1.QqSimSentenceResult.VectorList)
    })
  ,
  'DESCRIPTOR' : _QQSIMSENTENCERESULT,
  '__module__' : 'qqsim_pb2'
  # @@protoc_insertion_point(class_scope:qqsim.v1.QqSimSentenceResult)
  })
_sym_db.RegisterMessage(QqSimSentenceResult)
_sym_db.RegisterMessage(QqSimSentenceResult.VectorList)

TextPairReqMsg = _reflection.GeneratedProtocolMessageType('TextPairReqMsg', (_message.Message,), {
  'DESCRIPTOR' : _TEXTPAIRREQMSG,
  '__module__' : 'qqsim_pb2'
  # @@protoc_insertion_point(class_scope:qqsim.v1.TextPairReqMsg)
  })
_sym_db.RegisterMessage(TextPairReqMsg)

CmQsimSimilarResponse = _reflection.GeneratedProtocolMessageType('CmQsimSimilarResponse', (_message.Message,), {
  'DESCRIPTOR' : _CMQSIMSIMILARRESPONSE,
  '__module__' : 'qqsim_pb2'
  # @@protoc_insertion_point(class_scope:qqsim.v1.CmQsimSimilarResponse)
  })
_sym_db.RegisterMessage(CmQsimSimilarResponse)

QsimSimilarResult = _reflection.GeneratedProtocolMessageType('QsimSimilarResult', (_message.Message,), {
  'DESCRIPTOR' : _QSIMSIMILARRESULT,
  '__module__' : 'qqsim_pb2'
  # @@protoc_insertion_point(class_scope:qqsim.v1.QsimSimilarResult)
  })
_sym_db.RegisterMessage(QsimSimilarResult)

TextPairRspMsg = _reflection.GeneratedProtocolMessageType('TextPairRspMsg', (_message.Message,), {
  'DESCRIPTOR' : _TEXTPAIRRSPMSG,
  '__module__' : 'qqsim_pb2'
  # @@protoc_insertion_point(class_scope:qqsim.v1.TextPairRspMsg)
  })
_sym_db.RegisterMessage(TextPairRspMsg)

VersionResponse = _reflection.GeneratedProtocolMessageType('VersionResponse', (_message.Message,), {
  'DESCRIPTOR' : _VERSIONRESPONSE,
  '__module__' : 'qqsim_pb2'
  # @@protoc_insertion_point(class_scope:qqsim.v1.VersionResponse)
  })
_sym_db.RegisterMessage(VersionResponse)

_QQSIMSERVICE = DESCRIPTOR.services_by_name['QqsimService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z nlp-qqsim-server/api/qqsim/v1;v1'
  _MODELTYPE._serialized_start=1021
  _MODELTYPE._serialized_end=1112
  _CMQSIMSIMILARREQUEST._serialized_start=55
  _CMQSIMSIMILARREQUEST._serialized_end=205
  _CMQQSIMSENTENCEREQUEST._serialized_start=207
  _CMQQSIMSENTENCEREQUEST._serialized_end=306
  _CMQQSIMSENTENCERESPONSE._serialized_start=308
  _CMQQSIMSENTENCERESPONSE._serialized_end=429
  _QQSIMSENTENCERESULT._serialized_start=432
  _QQSIMSENTENCERESULT._serialized_end=581
  _QQSIMSENTENCERESULT_VECTORLIST._serialized_start=553
  _QQSIMSENTENCERESULT_VECTORLIST._serialized_end=581
  _TEXTPAIRREQMSG._serialized_start=583
  _TEXTPAIRREQMSG._serialized_end=687
  _CMQSIMSIMILARRESPONSE._serialized_start=689
  _CMQSIMSIMILARRESPONSE._serialized_end=806
  _QSIMSIMILARRESULT._serialized_start=808
  _QSIMSIMILARRESULT._serialized_end=906
  _TEXTPAIRRSPMSG._serialized_start=908
  _TEXTPAIRRSPMSG._serialized_end=983
  _VERSIONRESPONSE._serialized_start=985
  _VERSIONRESPONSE._serialized_end=1019
  _QQSIMSERVICE._serialized_start=1115
  _QQSIMSERVICE._serialized_end=1382
# @@protoc_insertion_point(module_scope)
