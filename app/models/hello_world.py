
class HelloWorld(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, message, description):
        self.message = message
        self.description = description


class HelloWorldSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ('id', 'message', 'description')


# Init the schema
hello_world_schema = HelloWorldSchema()
hello_worlds_schema = HelloWorldSchema(many=True)
