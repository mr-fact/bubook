from .models import Profile, BaseUser


def get_profile(user: BaseUser) -> Profile:
    return Profile.objects.get(user=user)


def get_user(id: int = None, phone: str = None, email: str = None) -> BaseUser:
    if id:
        return BaseUser.objects.get(id=id)
    elif phone:
        return BaseUser.objects.get(phone=phone)
    elif email:
        return BaseUser.objects.get(email=email)
