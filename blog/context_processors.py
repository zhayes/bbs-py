
def user(request):
    """
    渲染用户上下文
    """
    user_name = request.session.get('user_name')
    user_id = request.session.get('user_id')
    user_avatar = request.session.get('user_avatar')

    user = {}

    if(user_id):
        user = {
            "user_name": user_name,
            "user_id": user_id,
            "user_avatar": user_avatar
        }
    return user