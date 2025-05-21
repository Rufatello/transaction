from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from transaction.models import User
from transaction.serializers import UserSerializers


class UserStatsAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)

            serializer = UserSerializers(data={
                'user_id': user_id,
                'from_date': request.query_params.get('from_date'),
                'to_date': request.query_params.get('to_date'),
            })
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)

        except ObjectDoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
