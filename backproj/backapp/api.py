from ninja import NinjaAPI
from .schema import LoginSchema, SignupSchema, TokenSchema
from django.contrib.auth import authenticate
from .models import SpashtUser
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.errors import ValidationError
from rest_framework_simplejwt.views import TokenRefreshView
api = NinjaAPI()

@api.post("/signup", response=TokenSchema)
def signup(request, data:SignupSchema):
    if SpashtUser.objects.filter(username=data.username).exists():
        raise ValidationError([{"loc": ["username"], "msg": "Username already exists"}])
    if SpashtUser.objects.filter(email=data.email).exists():
        raise ValidationError([{"loc": ["email"], "msg": "Email already exists"}])
    user = SpashtUser.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        place= data.place, 
        date_of_birth = data.date_of_birth,
        profession= data.profession,
        mobile_number= data.mobile_number
    )
    user.save()
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

@api.post("/refresh")
def refresh(request):
    view = TokenRefreshView.as_view()
    return view(request._request)

@api.post("/login", response=TokenSchema)
def login(request, data:LoginSchema):
    user= authenticate(username=data.username, password=data.password)
    if user is None:
        return api.create_response(request, {"error": "Invalid credentials"}, status=401)
    refresh = RefreshToken.for_user(user)
    return { 
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

