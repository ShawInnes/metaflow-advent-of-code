from metaflow import FlowSpec, step, card, IncludeFile, Parameter


def script_path(filename):
    """
    A convenience function to get the absolute path to a file in this
    tutorial's directory. This allows the tutorial to be launched from any
    directory.

    """
    import os

    filepath = os.path.join(os.path.dirname(__file__))
    return os.path.join(filepath, filename)


class PlayListFlow(FlowSpec):

    input_data = IncludeFile(
        "input_data",
        help="The path to a movie metadata file.",
        default=script_path("day01.txt"),
    )

    @card
    @step
    def start(self):
        """
        Parse the input file and load the values into a dictionary of lists.

        """
        # For this example, we only need the movie title and the genres.

        # Parse the CSV header.
        self.data_blocks = self.input_data.split("\n\n")

        # Compute genre-specific movies and a bonus movie in parallel.
        self.next(self.part1)

    @card
    @step
    def part1(self):
        """
        This step parses the input.

        """

        calories_per_elf = [map(int, line.splitlines()) for line in self.data_blocks]
        self.total_calories_per_elf = [sum(elf) for elf in calories_per_elf]
        self.part1_answer = max(self.total_calories_per_elf)

        self.next(self.part2)

    @card
    @step
    def part2(self):
        """
        This step parses the input.

        """

        self.total_calories_per_elf.sort(reverse=True)
        self.part2_answer = sum(self.total_calories_per_elf[:3])

        self.next(self.end)

    @step
    def end(self):
        """
        Print out the playlist and bonus movie.

        """
        print("Answer 1: %d" % self.part1_answer)
        print("Answer 2: %d" % self.part2_answer)

if __name__ == "__main__":
    PlayListFlow()
