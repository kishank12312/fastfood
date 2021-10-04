from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponse


def PriceList(SeparateOrders):
    result = []
    for order in SeparateOrders:
        currentPrice = 0
        for obj in order:
            currentPrice += obj.ItemPrice * obj.Qty
        result.append(currentPrice)
    
    return result


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        u = sociallogin.user
        # Optionally, set as staff now as well.
        # This is useful if you are using this for the Django Admin login.
        # Be careful with the staff setting, as some providers don't verify
        # email address, so that could be considered a security flaw.
        u.is_staff = False
        if not u.email.split('@')[1] == "hyderabad.bits-pilani.ac.in":
            raise ImmediateHttpResponse(response=HttpResponse('You Can Login With Only BITS Mail Account!'))
        return super(CustomSocialAccountAdapter, self).is_open_for_signup(request, sociallogin)