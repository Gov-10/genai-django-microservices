from ninja import Schema
class LoginSchema(Schema):
    username :str
    password:str

class TokenSchema(Schema):
    access: str
    refresh : str

class SignupSchema(Schema):
    username : str
    password : str
    email : str
    place : str = None
    date_of_birth : str = None
    profession : str = None
    mobile_number : str = None