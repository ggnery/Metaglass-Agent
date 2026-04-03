import grpc

from generated import context_pb2_grpc


class ContextServiceServicer(context_pb2_grpc.ContextServiceServicer):

    def SemanticSearch(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("SemanticSearch not implemented")
        raise NotImplementedError("SemanticSearch not implemented")

    def PushContext(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("PushContext not implemented")
        raise NotImplementedError("PushContext not implemented")

    def GetSessionContext(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("GetSessionContext not implemented")
        raise NotImplementedError("GetSessionContext not implemented")
