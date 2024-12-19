from rest_framework import viewsets
from .models import Organisation
from .serializers import OrganisationSerializers

class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializers