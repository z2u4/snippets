import typing
import readchar as readchar


class TerminalSelection:
    """
    A class that provides a terminal selection user interface.
    It allows the user to select an option from a list of options.
    """

    def __init__(self, options: list, index=0):
        """
        Initializes a new instance of the TerminalSelection class.

        Args:
            options (list): A list of options to choose from.
            index (int, optional): The initial index of the selected option. Defaults to 0.
        """
        self.__options = options
        self.__index = index
        self.__dactionMarker = False
        self.clearScreenMethod: typing.Literal["clear", "movedown"] = "clear"
        self.printMethod = print

    @property
    def options(self):
        """
        Returns a copy of the list of options.

        Returns:
            list: A copy of the list of options.
        """
        return list(self.__options)

    @property
    def selected(self):
        """
        Returns the currently selected option.

        Returns:
            str: The currently selected option.
        """
        return self.__options[self.__index]

    def helpcommand(self):
        """
        Prints a help message explaining how to navigate and select options.
        No parameters.
        No return value.
        """
        self.printMethod("Arrow keys/WASD and Enter to select.")

    def clearScreen(self):
        """
        Clears the terminal screen.
        No parameters.
        No return value.
        """
        if self.clearScreenMethod == "clear":
            self.printMethod("\033[H\033[J")
        elif self.clearScreenMethod == "movedown":
            self.printMethod("\n" * 20)
            # focus on the current line
            self.printMethod("\x1b[1;1H")

    def run(self):
        """
        Runs the terminal selection user interface.
        No parameters.
        Returns:
            int: The index of the selected option or -1 if the user pressed "A".
        """
        self.helpcommand()
        while True:
            # Display options
            for i, option in enumerate(self.__options):
                prefix = "->" if i == self.__index else "  "
                self.printMethod(f"{prefix} {option}")

            if self.__dactionMarker:
                self.daction()
                self.__dactionMarker = False

            # Read key press
            key = readchar.readkey()

            # Up (W)
            if (key == "w" or key == "\x00H") and self.__index > 0:
                self.__index -= 1
            # Down (S)
            elif (key == "s" or key == "\x00P") and self.__index < len(
                self.options
            ) - 1:
                self.__index += 1
            elif key == "a" or key == "\x00K":
                return -1
            elif key == "d" or key == "\x00M":
                self.__dactionMarker = True

            # Enter to select
            elif key == readchar.key.ENTER:
                self.onComplete()
                break

            self.clearScreen()
        return 0

    def daction(self):
        """
        An action to be performed when the user presses the "D" key.
        No parameters.
        No return value.
        """
        pass

    @property
    def index(self):
        """
        Returns the index of the currently selected option.

        Returns:
            int: The index of the currently selected option.
        """
        return self.__index

    def onComplete(self):
        """
        Prints the selected option based on the current index.
        No parameters.
        No return value.
        """
        self.printMethod(f"You selected: {self.options[self.__index]}")


@pytest.fixture
def sample_data():
    return [
        {"id": "1", "name": "test_item"},
        {"id": 2, "name": "another_item"},
        {"id": "3", "name": "test_something"},
        {"id": 4, "name": "completely_different"},
    ]

def test_id_matching(sample_data):
    # Test integer ID
    result = DefaultQuery.match(2, sample_data)
    assert len(result) == 1
    assert result[0]["id"] == 2

    # Test string ID
    result = DefaultQuery.match("1", sample_data)
    assert len(result) == 1
    assert result[0]["id"] == "1"

def test_name_exact_match(sample_data):
    result = DefaultQuery.match("test_item", sample_data)
    assert len(result) == 1
    assert result[0]["name"] == "test_item"

def test_regex_name_matching(sample_data):
    # Test wildcard matching
    result = DefaultQuery.match("test_*", sample_data)
    assert len(result) == 2
    assert all("test_" in item["name"] for item in result)

    # Test alphanumeric exact matching
    result = DefaultQuery.match("test_item", sample_data)
    assert len(result) == 1
    assert result[0]["name"] == "test_item"

def test_eval_query(sample_data):
    # Test evaluation query
    result = DefaultQuery.match('?x["name"].startswith("test")', sample_data)
    assert len(result) == 2
    assert all(item["name"].startswith("test") for item in result)

def test_or_query(sample_data):
    # Test OR query with multiple conditions
    result = DefaultQuery.match(["test_item", 2], sample_data)
    assert len(result) == 2
    assert any(item["name"] == "test_item" for item in result)
    assert any(item["id"] == 2 for item in result)

def test_and_query(sample_data):
    # Test AND query
    result = DefaultQuery.match(('?x["name"].startswith("test")', '?x["name"].endswith("item")'), sample_data)
    assert len(result) == 1
    assert result[0]["name"] == "test_item"

def test_custom_query_model():
    # Test creating a custom query model
    custom_query = AdvancedQuery()
    
    @QueryModel.fromFunc(queryMatch=int)
    def custom_matcher(obj, query, original_obj):
        return [original_obj] if isinstance(obj, dict) and obj.get("value") == query else []

    custom_query.models.append(custom_matcher)
    
    test_data = [{"value": 42}, {"value": 24}]
    result = custom_query.match(42, test_data)
    assert len(result) == 1
    assert result[0]["value"] == 42

def test_invalid_queries(sample_data):
    # Test with invalid query types
    result = DefaultQuery.match(None, sample_data)
    assert len(result) == 0

    result = DefaultQuery.match({}, sample_data)
    assert len(result) == 0

def test_empty_data():
    # Test with empty data set
    result = DefaultQuery.match("test", [])
    assert len(result) == 0 