from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Job, Note
from .serializers import (
    JobListSerializer, JobDetailSerializer, JobWriteSerializer, NoteSerializer
)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by("-created_at")
    permission_classes = [AllowAny]
    filterset_fields = ["status", "location_type"]
    search_fields = ["title", "company", "tags_csv"]
    ordering_fields = [
        "created_at", "updated_at", "applied_at", "next_action_at"
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return JobListSerializer
        if self.action == "retrieve":
            return JobDetailSerializer
        return JobWriteSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("q")
        tag = self.request.query_params.get("tag")
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(company__icontains=q) |
                Q(tags_csv__icontains=q)
            )
        if tag:
            qs = qs.filter(tags_csv__iregex=rf"(^|,\s*){tag}(\s*,|$)")
        return qs

    @action(detail=True, methods=["post"])
    def notes(self, request, pk=None):
        job = self.get_object()
        ser = NoteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        note = Note.objects.create(job=job, **ser.validated_data)
        return Response(
            NoteSerializer(note).data,
            status=status.HTTP_201_CREATED
        )


class NoteViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]
