import json
import pymongo
from pymongo import MongoClient

if __name__ == '__main__':
    print('Please, run the main program file.')
    input()
    exit()


class DataBase:
    def __init__(self, name: str):
        with open('auth.json') as file:
            auth = json.load(file)

        db_name = auth['questionnaire'][name]
        user = auth['user']
        password = auth['password']

        appeal = f'mongodb+srv://{user}:{password}@cluster0.sonqc.mongodb.net/{db_name}?retryWrites=true&w=majority'

        self.db = MongoClient(appeal)['questionnaire'][db_name]
        self.__lambda_fun()

    def add(self, data: str, question_id: int = None):
        """
        Add data to data base.
        :param data: Post data.
        :param question_id: If data is the answer to the question, then the question ID is indicated.
        """

        last_id = self._get_last_id()

        post = {'_id': last_id + 1, 'string': data}
        if question_id is not None:
            post['question_id'] = question_id

        self.db.insert_one(post)

    def __lambda_fun(self):
        """
        Create self lambda functions for class.
        """
        self._get_last_id = lambda: len(list(self.db.find())) - 1
