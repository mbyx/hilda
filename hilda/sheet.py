from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Sheet:
    """A stylesheet of sorts that can define formatting for strings.

    The format for a sheet is as follows:
    @commandName:
        Formatting, in Markdown.
        Multiline!

    @nextCommand:
        Hello, {author}!

    @invalidCommand: Text not allowed on the same line.

    Anything inside {} is seen as a placeholder for actual data. This
    is populated by the audit function. The placeholders allowed are:
    - amt: The number of messages.
    - author: The user who gave the command.
    - members: The members to use.
    - channel: The channel that the command was invoked in.
    - guild: The guild that the command was invoked in.
    - content: The content of some message, if any.
    - date: The date a message was written at.
    - new_channel: A channel besides the current one.
    """

    _inner: dict[str, str]

    @staticmethod
    def from_file(path: str) -> "Sheet":
        """Load a format sheet from a file."""
        with open(path, "r") as f:
            lines: list[str] = f.readlines()

        name: str = ""
        sheet: dict[str, str] = defaultdict(str)
        for line in map(str.strip, lines):
            if line.startswith("@") and line.endswith(":"):
                name = line[1:-1]
                continue
            sheet[name] += line + "\n"

        return Sheet({k: v.strip() for k, v in sheet.items()})

    def __getitem__(self, key: str) -> str:
        return self._inner[key]
