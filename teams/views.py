from datetime import datetime
from rest_framework.views import APIView, Response, Request, status
from utils import data_processing
from .models import Team
from django.forms.models import model_to_dict


class TeamView(APIView):
    def get(self, request: Request) -> Response:
        teams = Team.objects.all()

        teams_list = []

        for team in teams:
            team_dict = model_to_dict(team)
            teams_list.append(team_dict)

        return Response(teams_list, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        test_data = data_processing(**request.data)

        if test_data:
            return Response(test_data, status.HTTP_400_BAD_REQUEST)

        team = Team.objects.create(**request.data)
        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_201_CREATED)


class TeamsDetailView(APIView):
    def get(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)

        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def patch(self, request, team_id):
        team = Team.objects.filter(id=team_id)

        if not team:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team.update(**request.data)

        team_updated = model_to_dict(Team.objects.get(id=team_id))

        return Response(team_updated, status.HTTP_200_OK)

    def delete(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)

        except:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team.delete()

        return Response(None, status.HTTP_204_NO_CONTENT)