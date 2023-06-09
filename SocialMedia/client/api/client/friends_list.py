from .imports import *


class FriendsList(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(responses={200: FriendsViewDto(many=True)})
    def get(self, request):
        context = {}
        context['friends'] = UserSafeSerializer(User.get_friends(request), many=True).data
        context['msg'] = 'دریافت شد'
        status_code = HTTP_200_OK
        return Response(context, status=status_code)

