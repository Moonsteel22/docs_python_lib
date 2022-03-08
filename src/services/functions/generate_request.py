from docs_python_lib.src.services.types.base import DocumentRequest


def generate_request(request: DocumentRequest):
    request_type: str = type(request).__name__
    return {request_type[0].lower() + request_type[1:]: request._to_dict()}
