from rest_framework import serializers
from .models import Job, Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "body", "created_at"]


class JobListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            "id", "title", "company", "status", "location_type", "location",
            "salary_min", "salary_max", "currency", "source", "url",
            "applied_at", "next_action_at", "tags", "created_at", "updated_at"
        ]

    def get_tags(self, obj):
        return obj.tags


class JobDetailSerializer(JobListSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta(JobListSerializer.Meta):
        fields = JobListSerializer.Meta.fields + ["notes"]


class JobWriteSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Job
        fields = [
            "title", "company", "location_type", "location",
            "salary_min", "salary_max", "currency", "source", "url",
            "status", "applied_at", "next_action_at", "tags"
        ]

    def create(self, validated):
        tags = validated.pop("tags", [])
        job = Job.objects.create(**validated, tags_csv=",".join(tags))
        return job

    def update(self, instance, validated):
        tags = validated.pop("tags", None)
        for k, v in validated.items():
            setattr(instance, k, v)
        if tags is not None:
            instance.tags_csv = ",".join(tags)
        instance.save()
        return instance
