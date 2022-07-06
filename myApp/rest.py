from rest_framework.response import Response
from rest_framework.decorators import api_view
from myApp.models import Ticket

# For react native app

@api_view(['GET'])
def get_tickets(request):
    tickets = list(Ticket.objects.filter(deleted=False).values('id','issue_type','issue_sub_type','description'))
    return Response({'tickets':tickets})