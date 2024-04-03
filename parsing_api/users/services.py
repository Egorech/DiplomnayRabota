from rest_framework.exceptions import PermissionDenied

from users.models import CustomUser


class BalanceService:
    @staticmethod
    def write_off_units(user: CustomUser, units: int) -> None:
        if user.units < units:
            raise PermissionDenied('Your limit has been used up (not enough checks)')
        user.units -= units
        user.save()
