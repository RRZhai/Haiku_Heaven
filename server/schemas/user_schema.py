from .__init__ import (
    fields, 
    validate, 
    validates, 
    ValidationError, 
    ma, 
    User
)

# from .post_schema import PostSchema
from .comment_schema import CommentSchema
from models.user import User
import re

class UserSchema(ma.SQLAlchemySchema):
    class Meta(): 
        model = User
        load_instance = True
        ordered = True
        fields = ("id", "username", "name", "bio", "profile_pic_num", 
                "public_acct", "posts", "comments", "followers", "url")

    username = fields.String(required=True, \
                            validate=validate.Length(min=5, max=20, \
                            error="Username must be between 5 and 20 chars"))
    name = fields.String(validate=validate.Length(min=5, max=50, \
                        error="Display name must be between 5 and 50 chars"),
                        allow_none=True)
    bio = fields.String(validate=validate.Length(max=250, \
                        error="Bio must be less than 250 chars"),
                        allow_none=True)
    posts = fields.Nested("PostSchema", only=("id", "content", "post_likes", "user", "url"), many=True)
    comments = fields.Nested(CommentSchema, only=("id", "url"), many=True)
    followers = fields.Nested("UserSchema", 
                            only=("id", "username", "url"), many=True)

    url = ma.Hyperlinks(
        {
            "self": ma.URLFor(
                "userbyid",
                values=dict(id="<id>")
            ),
            "collection": ma.URLFor("users")
        }
    )

    @validates("username")
    def validates_username(self, username):
        if user := User.query.filter(User.username == username).first():
            if not user.id:
                raise ValidationError("That username is taken")
        if not re.match(r"^[A-z0-9]+$", username):
            raise ValidationError("Username may only contain letters and digits")