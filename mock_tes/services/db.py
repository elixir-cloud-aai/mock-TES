from bson.objectid import ObjectId


class PyMongoUtils:
    """
    utility functions for PyMongo
    """

    def find_one_by_id(collection,object_id):
        """
        :param object_id:
        :return: A single object by object id, stripped of object id, or None if object not found
        """
        return collection.find_one({'_id': ObjectId(object_id)}, {'_id': False})
