class ReactionZone:
    """
    Store a block of 9 reactions.
    """

    def __init__(self, indexes, reactions_array):
        self.reactions_array = reactions_array
        self.contained_indexes = indexes

    def getFields(self):
        list_of_fields = []

        for index in self.contained_indexes:
            list_of_fields.append(self.reactions_array[index])

        return list_of_fields
