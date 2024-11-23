"""Adds or updates header to files."""

from typing import List


def add_header(
    filepaths: List[str],
    header_filepath: str,
    comment_style: str,
    newline_after_comment_start: bool,
    newline_before_comment_end: bool,
    start_header_after: str,
    ignore_below_string: str,
    stop_at_ignore_below: bool,
    max_line_length: int,
    fail_on_fix: bool,
):
    """Adds header to files.

    Args:
        filepaths: The markdown filepaths to add the header to
        header_filepath: The filepath to the header file
        comment_style: The comment style to use for the header
        newline_after_comment_start: If True, adds a newline after the comment start
        newline_before_comment_end: If True, adds a newline before the comment end
        start_header_after: A string to search for to start the header afterwards. Helpful if you want to add a header
            to a shell script
        ignore_below_string: A string to search for to determine where the header stops and the rest of the content
            starts (typically in a comment)
        stop_at_ignore_below: If True, stops adding the header when the ignore_below_string is found
        max_line_length: Splits lines by word tokens that are longer than the specified length
        fail_on_fix: If True, exits with a non-zero status if any files were modified
    """
    with open(header_filepath) as f:
        header = f.read()

    # checks the comment style and initializes variables
    if "|" in comment_style:
        is_triplet = True
        comment_start, comment_prefix, comment_end = comment_style.split("|")
        comment_start_check = comment_start
        cleaned_comment_end = comment_end if comment_end[0] == " " else " " + comment_end
    else:
        is_triplet = False
        comment_start = None
        comment_prefix = comment_style
        comment_end = None
        cleaned_comment_end = None
        comment_start_check = comment_prefix

    def split_long_lines(line: str, with_comment_start: bool = False) -> str:
        """Splits long lines into multiple lines."""
        if max_line_length:
            words = line.split(" ")
            lines = []
            line_prefix = comment_prefix + " " if comment_prefix else ""
            current_line = line_prefix if not with_comment_start else ""
            for word in words:
                if len(current_line) + len(word) + 1 <= max_line_length:
                    current_line += word + " "
                else:
                    lines.append(current_line.rstrip())
                    current_line = line_prefix + word + " "
            lines.append(current_line.rstrip())
            return "\n".join(lines)
        else:
            line_prefix = comment_prefix + " " if comment_prefix else ""
            return line_prefix + line

    # creates header comment string
    header_comment = ""
    header_lines = header.splitlines()
    header_num_of_lines = len(header_lines)
    for i, line in enumerate(header_lines):
        if i == 0 and is_triplet:
            tmp_line = line
            if header_num_of_lines == 1:
                if newline_before_comment_end:
                    tmp_line += "\n"
                    tmp_line += comment_end
                else:
                    tmp_line += cleaned_comment_end

            if newline_after_comment_start:
                header_comment += comment_start
                header_comment += "\n"
                header_comment += split_long_lines(tmp_line)
            else:
                header_comment += split_long_lines(comment_start + " " + tmp_line, with_comment_start=True)
        elif i == header_num_of_lines - 1 and is_triplet:
            if newline_before_comment_end:
                header_comment += split_long_lines(line)
                header_comment += "\n"
                header_comment += comment_end
            else:
                header_comment += split_long_lines(line + cleaned_comment_end)
        else:
            header_comment += split_long_lines(line)

        header_comment += "\n"

    # iterates through the filepaths and adds the header if needed
    for filepath in filepaths:
        with open(filepath, "r+") as f:
            content = ""
            before_header = ""

            # if the start_header_after string is set and is found in the file, it sets the content to the the lines
            # following the string identifier
            # otherwise, it sets the content to the entire file
            if start_header_after:
                start_header_flag = False
                for line in f.readlines():
                    if start_header_flag:
                        content += line
                    elif start_header_after in line:
                        start_header_flag = True
                        before_header += line
                    else:
                        before_header += line

                if not content and not start_header_flag:
                    content = before_header
                    before_header = ""
            else:
                content = f.read()
            f.seek(0)

            if not content.startswith(comment_start_check):
                # if the file does not have a header, add it
                if before_header:
                    f.write(before_header)
                f.write(header_comment)
                f.write(content)
                if fail_on_fix:
                    exit(1)
            elif not content.startswith(header_comment):
                # if the file has a header but it is not the same, replace it
                rest_of_content_flag = False
                rest_of_content = ""

                lines = f.readlines()

                for i, line in enumerate(lines):
                    if rest_of_content_flag:
                        rest_of_content += line
                    elif stop_at_ignore_below and ignore_below_string in line:
                        rest_of_content += line
                        rest_of_content_flag = True
                    elif (is_triplet and (line.startswith(comment_end) or line.rstrip().endswith(comment_end))) or (
                        not is_triplet
                        and line.startswith(comment_prefix)
                        and i + 1 < len(lines)
                        and not lines[i + 1].startswith(comment_prefix)
                    ):
                        rest_of_content_flag = True

                f.seek(0)
                if before_header:
                    f.write(before_header)
                f.write(header_comment)
                f.write(rest_of_content)
                f.truncate()
                if fail_on_fix:
                    exit(1)


def main():
    """Main program to run with command line options."""
    import argparse

    parser = argparse.ArgumentParser(prog="Adds or updates header")
    parser.add_argument("filepaths", nargs="+", help="The filepath to add the header to")
    parser.add_argument("--header-filepath", help="The filepath to the header file", required=True)
    parser.add_argument(
        "--comment-style",
        help=(
            "A single comment prefix or a triplet separated by vertical bars ("
            "<comment-start>|<comment-prefix>|<comment-end>). "
            "E.g., a Java comment block would be: /*| *| */. Defaults to %(default)s"
        ),
        default="#",
    )
    parser.add_argument(
        "--newline-after-comment-start",
        help="Adds a newline after the comment start",
        action="store_true",
    )
    parser.add_argument(
        "--newline-before-comment-end",
        help="Adds a newline before the comment end",
        action="store_true",
    )
    parser.add_argument(
        "--start-header-after",
        help="A string to search for to start the header afterwards. Helpful if you want to add a header to a shell script",
    )
    parser.add_argument(
        "--ignore-below-string",
        help="A string to search for to determine where the header stops and the rest of the content starts (typically in a comment). Defaults to '%(default)s'",
        default="ignore below",
    )
    parser.add_argument(
        "--stop-at-ignore-below",
        help="Stops adding the header when the ignore-below-string is found",
        action="store_true",
    )
    parser.add_argument(
        "--max-line-length",
        help="Splits lines by word tokens that are longer than the specified length",
        type=int,
    )
    parser.add_argument(
        "--fail-on-fix",
        help="Exits with a non-zero status if any files were modified",
        action="store_true",
    )

    args = parser.parse_args()

    add_header(**vars(args))


if __name__ == "__main__":
    main()
