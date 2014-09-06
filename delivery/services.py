from delivery.models import Request

def get_request(request_id):
    request = Request.objects.get(id=request_id)
    return request