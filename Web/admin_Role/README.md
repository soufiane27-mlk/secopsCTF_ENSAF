# 🛡️ Challenge Writeup — Admin Password
---

## 📜 Challenge Description

Do what ever you want just find the flag 

---

## 🔗 Connection Details

- Host: `http://ensafacademia.ddns.net:5010`
 
> **Author:** s0ufm3l
---

![login form](images/image.png)

the source code of the `/login`

![default creds in source code](images/image-1.png)

We log in using the default credentials, and then we see that JWT is used as the authentication/authorization mechanism.

![jwt for authentication](images/image-2.png)

use token.dev to decode the jwt token.
our current user has a role *user*, we need to change it to *admin*

![deocding jwt token](images/image-3.png)

However, we need the signing key to modify the user and role to perform privilege escalation. We use jwt-crack to retrieve the key..

![cracker the signing key](images/image-4.png)

Use the following Python code to generate a JWT token with the modified parameters and properly sign it with the key `secops`. (I encountered issues using other online tools like token.dev and jwt.io, so generating it manually is more reliable.)

```python
import jwt
import datetime
token = jwt.encode({
                'username': "admin",
                'role': "admin",
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, "secops")
print(token)
```

we get a new token:

```less
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzQ1Nzg3MjE2fQ.msIhPHYWDoMvd8FABf0Dxa4tdQH6S6uDbRuhrdpGhM0
```

![admin token](images/image-5.png)

after modifying the token we get the admin dashboard, with a link to the admin pannel `/admin`

![admin dashboard](images/image-6.png)

The admin panel

![admin panel](images/image-7.png)

The site is under development, but there is a field that fetches some data without any visible parameters in the source code. We use `arjun` to fuzz for hidden parameters (don't forget to add the `Cookie: token=JWT_TOKEN` header; otherwise, you will be redirected to the login form).

![fuzzing for params](images/image-8.png)

we found a param with the name `fetch`.

![fetch testing](images/image-9.png)

the application only fetchs url with localhost (127.0.0.1 or localhost), because the application is running on port 5000, we fetch the url http://127.0.0.1:5000

![file params](images/image-10.png)
We need to specify the file parameter (as revealed by the application's error handling). The flag.txt file contains only a fake flag. To find the real one, we need to explore more of the application's logic. The most important file is `app.py`, which is the main file of the Python web application. By analyzing it, we discover that the correct flag is actually the `admin password`.

![the flag as the admin password](images/image-11.png)

> **flag:** SECOPS{SSrF_JwT_H4cK3d_MbrOuk#lik}