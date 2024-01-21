from uuid import uuid4


class ModelsUtil:
    def __init__(self):
        pass

    @staticmethod
    def generate_hash() -> str:
        hash_string = uuid4().hex[:20]

        return hash_string
