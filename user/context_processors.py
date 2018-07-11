from user.models import Prof
from django.contrib.auth.models import User

# def view_prof(request):
#     try:
#         prof = Prof.objects.get(pk=request.pk)
#     except:
#         print(request)
#         prof = None
#     return {'view_prof': prof}


def log_prof(request):
    try:
        uzer = Prof.objects.get(pk=request.session['user_id'])
    except:
        uzer = None
    return {'log_prof': uzer}