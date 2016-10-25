class Field:
    """
    Store data related to one filed of the reaction table.
    """

    def __init__(self, index, initial_value, max_value, min_value):
        self.current_value = initial_value
        self.dummy_value = initial_value
        self.max = max_value
        self.min = min_value
        self.checked_mid = False
        self.checked_top = False
        self.checked_bot = False
        self.related_index = index

    def setNewValue(self, new_value):
        self.current_value = new_value

    def getCurrentValue(self):
        return self.current_value

    def getNextValue(self):
        if not self.checked_bot:
            self.checked_bot = True
            self.dummy_value = self.current_value - 1

            if self.dummy_value < self.min:
                self.dummy_value = self.min

            return self.dummy_value

        elif not self.checked_mid:
            self.checked_mid = True
            self.dummy_value = self.current_value
            return self.dummy_value

        elif not self.checked_top:
            self.checked_top = True
            self.dummy_value = self.current_value + 1

            if self.dummy_value > self.max:
                self.dummy_value = self.max

            return self.dummy_value

    def allChecked(self):
        if self.checked_bot and self.checked_mid and self.checked_top:
            return True
        else:
            return False

    def resetCheckFlags(self):
        self.checked_bot = False
        self.checked_mid = False
        self.checked_top = False
