class State(object):
    """Represents a state in the missionaries and cannibals problem

    Attributes:

        missionaries_right (int): Number of missionaries on the right bank
        cannibals_right (int): Number of cannibals on the right bank

        missionaries_left (int): Number of missionaries on the left bank
        cannibals_left (int): Number of cannibals on the left bank

        boat_location (string): Whether boat is on `left` or `right` bank

    """

    def __init__(self, m_right, c_right, m_left, c_left, boat_loc):
        self.missionaries_right = m_right
        self.cannibals_right = c_right

        self.missionaries_left = m_left
        self.cannibals_left = c_left

        if boat_loc == "left" or boat_loc == "right":
            self.boat_location = boat_loc
        else:
            raise ValueError("boat location must be left or right")


    @staticmethod
    def from_string(data_string):
        right_bank = data_string.split("\n")[0].split(",")
        left_bank = data_string.split("\n")[1].split(",")

        m_right = int(right_bank[0])
        c_right = int(right_bank[1])
        m_left = int(left_bank[0])
        c_left = int(left_bank[1])
        boat_loc = "right" if int(right_bank[2]) == 1 else "left"

        return State(m_right, c_right, m_left, c_left, boat_loc)


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self):
        return "{},{},{}\n{},{},{}".format(
            self.missionaries_right,
            self.cannibals_right,
            1 if self.boat_location == "right" else 0,
            self.missionaries_left,
            self.cannibals_left,
            1 if self.boat_location == "left" else 0)

