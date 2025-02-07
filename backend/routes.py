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
    # Make a loop to run through the dictionaries and return each of the url's
    picture_urls = [picture['pic_url'] for picture in data]
    return jsonify(picture_urls), 200


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
    picture_url = request.json.get('pic_url')

    #Check if the picture URL is provided
    if not picture_url:
        return jsonify({"message": "URL is required"}), 400
    
    #Check if the picture URL already exists
    for picture in data:
        if picture['pic_url'] == picture_url:
            return jsonify({"message": "Picture with this URL already exists"}), 201
            break

    # Generate a new ID for the picture
    #new_id = len(data) + 1  # Example of generating a new ID

    # Add the new picture entry to the data structure
    new_picture = {"id": (len(data) + 1), "pic_url": picture_url}
    data.append(new_picture)

    # Return a success message with the new picture entry
    return jsonify(new_picture), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Finds the picture url when a specific id is given and can update it if it already exists
    """
    # Extract the picture from the request data:
    if id in data:
        new_data = request.get_json()
        picture[id].update(new_data)
        return jsonify({"message": "Picture updated successfully", "pic_url": new_data[id]}), 200
    else:
        return jsonify({"message": "Picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if id in data:
        del data [id]
        return '', 204 #HTTP_204_NO_CONTENT
    else:
        return jsonify ({"message": "Picture not found"}), 404

