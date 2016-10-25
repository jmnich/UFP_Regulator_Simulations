import copy

class ReactionsGenerator:

    def __init__(self, reactions_array, zones):
        self.reactions = reactions_array        # stores field objects
        self.zones = zones
        self.stack_of_fields = []
        self.current_zone = 0
        self.zones_processed = 0
        self.iterations_done = 0

        # init stack of fields
        for field in self.zones[self.current_zone].getFields:
            self.stack_of_fields.append(field)

    def nextSetOfReactions(self, last_set_of_reactions, current_best_set_of_reactions):
        """
        Returns next set of reactions for testing. Automatically switches zones and fields. During single iteration
        algorithm generates all combinations of fields incremented by 1, preserved and decremented by -1 for a single
        zone and then switches to a next one.
        :return: array of 81 reactions
        """

        next_array_of_reactions = copy.deepcopy(last_set_of_reactions)
        support_stack = []
        next_zone = False

        # check peek
        peek_field = self.stack_of_fields[0]

        while peek_field.allChecked():              # move all fully checked fields to support stack and reset them
            support_stack.insert(0, self.stack_of_fields.remove(0))
            support_stack[0].resetCheckFlags()

            if len(self.stack_of_fields) == 0:      # zone checked, switch to next
                support_stack.clear()

                self.zones_processed += 1

                self.current_zone += 1
                if self.current_zone > 8:           # loop (9 zones are present in the array)
                    self.current_zone = 0

                for i in range(81):                 # update fields after zone is switched
                    self.reactions[i].setNewValue(current_best_set_of_reactions[i])

                for field in self.zones[self.current_zone].getFields():
                    self.stack_of_fields.append(field)

                peek_field = self.stack_of_fields[0]

                next_array_of_reactions = copy.deepcopy(current_best_set_of_reactions)
            else:
                peek_field = self.stack_of_fields[0]

        if len(support_stack) > 0:
            while len(support_stack) > 0:  # move all filed back from support to main stack, update values
                self.stack_of_fields.insert(0, support_stack.remove(0))
                next_array_of_reactions[self.stack_of_fields[0].related_index] = self.stack_of_fields[0].getNextValue()
        else:   # if no fields were moved to support stack update value on peek field in main stack
            next_array_of_reactions[peek_field.related_index] = peek_field.getNextValue()

        self.iterations_done += 1

        return next_array_of_reactions






