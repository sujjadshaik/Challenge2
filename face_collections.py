import boto3
from pathlib import Path
from pprint import pprint
# note for my Cloud Computing students,
# image_loaders.py is the new name for image_helpers.py
from botocore.exceptions import ClientError

from Image_helper import get_image
from typing import List


def delete_collection(collection_id):
    print('Attempting to delete collection ' + collection_id)
    client = boto3.client('rekognition', region_name='eu-west-1')
    status_code = 0
    try:
        response = client.delete_collection(CollectionId=collection_id)
        status_code = response['StatusCode']

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print('The collection ' + collection_id + ' was not found ')
        else:
            print('Error other than Not Found occurred: ' + e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
    return (status_code)





def list_collections() -> List[str]:
    """
    Returns a list of the names of the existing collections
    :return: a list of the names of the existing collections
    """
    # lightly edited version of
    # https://docs.aws.amazon.com/rekognition/latest/dg/list-collection-procedure.html,
    # last access 3/5/2019

    client = boto3.client('rekognition', region_name='eu-west-1')
    response = client.list_collections()
    result = []
    while True:
        collections = response['CollectionIds']
        result.extend(collections)

        # if more results than maxresults
        if 'NextToken' in response:
            next_token = response['NextToken']
            response = client.list_collections(NextToken=next_token)
            pprint(response)
        else:
            break
    return result


def collection_exists(coll_name: str) -> bool:
    """
    Checks to see if the collection exists
    :param coll_name: the name of the collection to check
    :return: true iff the collection already exists
    """
    return coll_name in list_collections()


def create_collection(coll_name: str):
    """
    Creates a collection with the specified name, if it does not already exist
    :param coll_name: the name of the collection to create
    """
    # lightly edited version of
    # https://docs.aws.amazon.com/rekognition/latest/dg/create-collection-procedure.html,
    # last access 3/5/2019

    client = boto3.client('rekognition', region_name='eu-west-1')
    if not collection_exists(coll_name):
        response = client.create_collection(CollectionId=coll_name)
        if response['StatusCode'] != 200:
            raise 'Could not create collection, ' + coll_name \
                  + ', status code: ' + str(response['StatusCode'])


def list_faces(coll_name: str) -> List[dict]:
    """
    Return a list of faces in the specified collection.
    :param coll_name: the collection.
    :return: a list of faces in the specified collection.
    """
    # lightly edited version of
    # https://docs.aws.amazon.com/rekognition/latest/dg/list-faces-in-collection-procedure.html
    # last access 3/5/2019

    client = boto3.client('rekognition', region_name='eu-west-1')
    response = client.list_faces(CollectionId=coll_name)
    tokens = True
    result = []

    while tokens:

        faces = response['Faces']
        result.extend(faces)

        if 'NextToken' in response:
            next_token = response['NextToken']
            response = client.list_faces(CollectionId=coll_name,
                                         NextToken=next_token)
        else:
            tokens = False

    return result


def add_face(coll_name: str, image: str):
    """
    Adds the specified face image to the specified collection.
    :param coll_name: the collection to add the face to
    :param image: the face image (either filename or URL)
    """

    # lightly edited version of
    # https://docs.aws.amazon.com/rekognition/latest/dg/add-faces-to-collection-procedure.html
    # last access 3/5/2019

    # nested function
    def extract_filename(fname_or_url: str) -> str:
        """
        Returns the last component of file path or URL.
        :param fname_or_url: the filename or url.
        :return: the last component of file path or URL.
        """
        import re
        return re.split('[\\\/]', fname_or_url)[-1]

    # rest of the body of add_face
    client = boto3.client('rekognition', region_name='eu-west-1')
    rekresp = client.index_faces(CollectionId=coll_name,
                                 Image={'Bytes': get_image(image)},
                                 ExternalImageId=extract_filename(image))

    if rekresp['FaceRecords'] == []:
        raise Exception('No face found in the image')


def find_face_id(coll_name: str, ext_img_id: str) -> str:
    """
    Find the face_id for the specified image in the collection.
    :param coll_name: the name of the collection.
    :param ext_img_id: the ExternalImageId set for the image
    :return: the ImageId if found, or the emtpy string otherwise
    """
    face = [face for face in list_faces(coll_name) if face['ExternalImageId'] == ext_img_id]
    if face != []:
        return face[0]['FaceId']
    else:
        return ''

def find_external_img_id(coll_name,face_id):
    face = [face for face in list_faces(coll_name) if face['FaceId'] == face_id]
    if face != []:
        return face[0]['ExternalImageId']
    else:
        return ''




def delete_face(coll_name: str, face_ids: List[str]) -> str:
    """
    Deletes the specified faces from the collection.
    :param coll_name: the name of the collection
    :param face_ids: a list of face ids (see FaceId) field in collection
    :return: returns a list of the face ids that were deleted
    """
    # lightly edited version of
    # https://docs.aws.amazon.com/rekognition/latest/dg/delete-faces-procedure.html
    # last access 3/5/2019

    client = boto3.client('rekognition', region_name='eu-west-1')
    response = client.delete_faces(CollectionId=coll_name,
                                   FaceIds=face_ids)
    return response['DeletedFaces']


def find_face(coll_name: str, face_to_find: str) -> List[dict]:
    """
    Searches for the specified face in the collection.
    :param face_to_find: a string that is either the filename or URL to the image containing the face to search for.
    :return: a list of face info dictionaries
    """
    # lightly edited version of
    # https://docs.aws.amazon.com/rekognition/latest/dg/search-face-with-image-procedure.html
    # last access 3/5/2019
    client = boto3.client('rekognition', region_name='eu-west-1')

    rekresp = client.search_faces_by_image(CollectionId=coll_name,
                                           Image={'Bytes': get_image(face_to_find)})

    return rekresp['FaceMatches']


def find_face_by_faceID(coll_name, face_id):
    client = boto3.client('rekognition', region_name='eu-west-1')
    # rekresp = client.search_faces_by_image(CollectionId=coll_name,
    #                                        Image={'Bytes': get_image(face_to_find)})
    rekresp = client.search_faces(CollectionId=coll_name, FaceId=face_id, FaceMatchThreshold=90,
                                  MaxFaces=2)
    face_matches = rekresp['FaceMatches']
    for match in face_matches:
        print('FaceId:' + match['Face']['FaceId'])
        print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print

    return len(face_matches)


def search_face_in_collection(face_id, collection_id):
    threshold = 90
    max_faces = 2
    client = boto3.client('rekognition', region_name='eu-west-1')

    response = client.search_faces(CollectionId=collection_id,
                                   FaceId=face_id,
                                   FaceMatchThreshold=threshold,
                                   MaxFaces=max_faces)

    face_matches = response['FaceMatches']
    print('Matching faces')
    for match in face_matches:
        print('FaceId:' + match['Face']['FaceId'])
        print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        print
    return len(face_matches)
