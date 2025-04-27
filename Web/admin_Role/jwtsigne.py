import jwt
import datetime
token = jwt.encode({
                'username': "admin",
                'role': "admin",
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, "secops")
print(token)