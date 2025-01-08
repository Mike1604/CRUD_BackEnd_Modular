
#Todo: Add JWT logic here
def verify_password(input_password: str, stored_password: str) -> bool:
    return input_password == stored_password