from django.http import JsonResponse

from backend.models import UserArea, RoleUser

def get_city_by_country(request):

    ret = []
    country = request.GET.get('country', None)
    if country is not None or country != '' or country != '-' or country != 'None':

        try:

            cities = UserArea.objects.values('id', 'name').filter(type='city', parent__parent_id=country).\
                order_by('name')
            ret = list(cities)
        except UserArea.DoesNotExist:
            pass
    else:
        ret = {'error': 'Invalid parameter!'}

    return JsonResponse(ret, safe=False)


def get_user_by_role(request):

    ret = []
    role = request.GET.get('role', None)
    if role is not None or role != '' or role != '-' or role != 'None':

        try:

            cities = RoleUser.objects.values('user__id', 'user__first_name', 'user__last_name').filter(role_group_id=role, user__is_staff=True, user__is_active=True).order_by('user__first_name')
            ret = list(cities)
        except RoleUser.DoesNotExist:
            pass
    else:
        ret = {'error': 'Invalid parameter!'}

    return JsonResponse(ret, safe=False)