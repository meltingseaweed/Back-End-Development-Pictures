from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """ Return the url's of all the pictures.
    """
    return jsonify(data)


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Finds the picture url when a specific id is given
    """
    # Search for the picture by id
    for person in data:
        if person["id"] == int(id):
            return jsonify(person), 200
    # If not found, return a 404 status with a message
    return jsonify({"message": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route('/picture', methods=["POST"])
def create_picture():
    """ Post a picture to to the dataset when it is given in the URL
    """
    # Extract the picture URL from the request data
    picture_in = request.json
    print(picture_in)

    #Check if the picture URL already exists
    for picture in data:
        if picture_in['id'] == picture["id"]:
            return {"Message": f"picture with id {picture_in['id']} already present"
            }, 302
    data.append(picture_in)

    # Return a success message with the new picture entry
    return jsonify(picture_in), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Finds the picture url when a specific id is given and can update it if it already exists
    """
    # Extract the picture from the request data:
    picture_in = request.json

    for index, picture in enumerate(data):
        if picture["id"] == id:
            data[index] = picture_in
            return picture, 201
    
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204

    else:
        return jsonify ({"message": "Picture not found"}), 404

