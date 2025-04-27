import jwt
import datetime
token = jwt.encode({
                'username': "admin",
                'role': "admin",
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
            }, "secops")
print(token)