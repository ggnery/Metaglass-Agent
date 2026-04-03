import grpc

from generated import orchestrator_pb2_grpc


class OrchestratorServiceServicer(orchestrator_pb2_grpc.OrchestratorServiceServicer):

    def Query(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Query not implemented")
        raise NotImplementedError("Query not implemented")

    def QueryStream(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("QueryStream not implemented")
        raise NotImplementedError("QueryStream not implemented")
