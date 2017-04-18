class State(object):
    """Represents a state in the missionaries and cannibals problem

    Attributes:

        missionaries_right (int): Number of missionaries on the right bank
        cannibals_right (int): Number of cannibals on the right bank

        missionaries_left (int): Number of missionaries on the left bank
        cannibals_left (int): Number of cannibals on the left bank

        boat_location (string): Whether boat is on `left` or `right` bank

    """

    def __init__(self, data_string):
        right_bank = data_string.split("\n")[0].split(",")
        left_bank = data_string.split("\n")[1].split(",")

        self.missionaries_right = int(right_bank[0])
        self.cannibals_right = int(right_bank[1])

        self.missionaries_left = int(left_bank[0])
        self.cannibals_left = int(left_bank[1])

        if int(right_bank[2]) == 1:
            self.boat_location = "right"
        else:
            self.boat_location = "left"

    def __repr__(self):
        return "{0},{1},{2}\n{3},{4},{5}".format(
            self.missionaries_right,
            self.cannibals_right,
            1 if self.boat_location == "right" else 0,
            self.missionaries_left,
            self.cannibals_left,
            1 if self.boat_location == "left" else 0)
