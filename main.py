import os
from flask import (
    jsonify,
    request,
    abort,
)
from dotenv import (
    load_dotenv,
)
from app import (
    app,
    db,
)
from models import (
    Users,
)

load_dotenv()


@app.route("/")
def index():
    """The index route."""
    return "Is this working? xd"


@app.route(
    "/signup",
    methods=["POST"],
)
def signup():
    """The signup route."""
    data = request.get_json()
    if data["API_KEY"] == os.environ["API_KEY"]:
        new_user = Users(**data)
        db.session.add(new_user)
        db.session.commit()
        return (
            jsonify({"message": "User created successfully."}),
            201,
        )
    abort(
        403,
        description="You don't have permission to access this resource.",
    )


@app.route(
    "/signin",
    methods=["POST"],
)
def signin():
    """The signin route."""
    data = request.get_json()
    if data["API_KEY"] == os.environ["API_KEY"]:
        users = Users.query.filter_by(email=data["email"]).all()
        output = []

        for user in users:
            output.append(
                {
                    "user": user.email,
                    "password": user.password,
                    "id": user.id,
                }
            )

        return jsonify({"users": output})
    abort(
        403,
        description="You don't have permission to access this resource.",
    )


if __name__ == "__main__":
    app.run(
        port=7000,
        debug=True,
        use_reloader=False,
    )
