import grpc

from generated import session_pb2_grpc


class SessionServiceServicer(session_pb2_grpc.SessionServiceServicer):

    def CreateSession(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("CreateSession not implemented")
        raise NotImplementedError("CreateSession not implemented")

    def Heartbeat(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Heartbeat not implemented")
        raise NotImplementedError("Heartbeat not implemented")

    def EndSession(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("EndSession not implemented")
        raise NotImplementedError("EndSession not implemented")

    def GetSession(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("GetSession not implemented")
        raise NotImplementedError("GetSession not implemented")
