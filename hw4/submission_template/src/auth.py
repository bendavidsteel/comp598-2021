import tornado
from tornado.web import RequestHandler


# could define get_user_async instead
def get_user(request_handler):
    return request_handler.get_cookie("user")

login_url = "/"

# optional login page for login_url
class LoginHandler(RequestHandler):

    def check_permission(self, username, password):
        if username == "nyc" and password == "iheartnyc":
            return True
        return False

    def get(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.check_permission(username, password)
        if auth:
            self.set_current_user(username)
            self.redirect("/nyc_dash")
        else:
            error_msg = "?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(login_url + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")
