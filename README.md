# pre-commit add header

A [pre-commit](https://pre-commit.com) hook to automatically add or update a header of a text file with the appropriate comment style for your source code.

## Why does this exist?

This exists so that you can include a license (or any other piece of text) at the top of a lot of different files, and it can automatically update them all at once.

There are already other pre-commit hooks that do this (such as [Lucas-C/pre-commit-hooks](https://github.com/Lucas-C/pre-commit-hooks)), how does this one differ?

This pre-commit hook

- Always keeps your header up to date when you change the header text.
  - It does not rely on an fuzzy string matching or require you to remove all the old headers with a separate command before applying the new header.
  - Instead, it looks for the end of the comment or a custom string that you set to identify the end of the header.
- Has the ability to wrap long text onto a new line. This is not as useful for just pasting a license at the top of a file that is already formatted with newlines, but quite useful if the block of text is just a long single line.

## How to use?

This is how to set up the pre-commit hook. You may consider running the hook multiple times for different file extensions. Related, you should change the files regex and name (to help better identify each check) appropriately. And you can pass any of the [below options](#options) in the `args` section.

```yaml
repos:
  - repo: https://github.com/sayari-analytics/pre-commit-add-header
    rev: v1.0.0
    hooks:
      - id: add-header
        name: Add or update header for Python files
        args:
          - --header-filepath
          - path/to/header.txt
          # put optional arguments here
        files: \.py$
```

## Options

These are the options that the script accepts. This is mostly copied from the output of the `--help` option.

One thing to note is that the filepaths you want this script to run on are passed as positional arguments. In a pre-commit hook, this is handled automatically. Something to keep note of if you are using this outside of pre-commit.

- `--header-filepath` (required, string) - The filepath to the header file.
- `--comment-style` (optional, string) - A single comment prefix or a triplet separated by vertical bars (`<comment-start>|<comment-prefix>|<comment-end>`). E.g., a Java comment block would be: `/*| *| */`. Defaults to `#`.
- `--newline-after-comment-start` (optional, boolean flag) - Adds a newline after the comment start.
- `--newline-before-comment-end` (optional, boolean flag) - Adds a newline before the comment end.
- `--start-header-after` (optional, string) - A string to search for to start the header afterwards. Helpful if you want to add a header to a shell script.
- `--ignore-below-string` (optional, string) - A string to search for to determine where the header stops and the rest of the content starts (typically in a comment). Defaults to `ignore below`.
- `--stop-at-ignore-below` (optional, boolean flag) - Stops adding the header when the ignore-below-string is found.
- `--max-line-length` (optional, integer) - Splits lines by word tokens that are longer than the specified length.
- `--fail-on-fix` (optional, boolean flag) - Exits with a non-zero status if any files were modified. No need to pass this when using as a pre-commit hook since pre-commit will fail if any files have been modified.

## Other ways to install

If you prefer to use this tool without pre-commit, you can install the standalone Python package.

```bash
pip install add-header
```

After installing the package, you can use the cli tool by typing:

```bash
# with the installed console script entry point
add-header -h
# or through the Python module
python -m add_header -h
```

## Examples

Here are some examples demonstrating this pre-commit hook's ability. Additionally, you might find it helpful to look at our [test cases](./tests/) for more examples.

### Markdown with entirely different header

The command to run:

```bash
add-header \
  --header-filepath path/to/header.txt \
  --comment-style "<!--||-->" \
  filepath1.md filepath2.md
```

If the existing header is like this:

```markdown
<!-- There are no comment text between this old header and the new one -->
# Hello World
```

Outputs a header like this (there is no fuzzy string matching or running a separate command to remove the old header required):

```markdown
<!-- This is the header comment -->
# Hello World
```

### Java with max line length and newline before comment end

The command to run:

```bash
add-header \
  --header-filepath path/to/header.txt \
  --comment-style "/*| *| */" \
  --newline-before-comment-end \
  --max-line-length 110 \
  filepath1.java filepath2.java
```

Outputs a header like this:

```java
/* This is a really long comment that should get split after 110 characters. This is a really long comment
 * that should get split after 110 characters.
 */
public class HelloWorld {}
```

### Java without max line length and without newline before comment end

The command to run:

```bash
add-header \
  --header-filepath path/to/header.txt \
  --comment-style "/*| *| */" \
  filepath1.java filepath2.java
```

Outputs a header like this:

```java
/* This is a really long comment that does not get get split. This is a really long comment that does not get get split. */
public class HelloWorld {}
```

### Bash

The command to run:

```bash
add-header \
  --header-filepath path/to/header.txt \
  --start-header-after "#!/bin/bash" \
  filepath1.sh filepath2.sh
```

Outputs a header like this:

```bash
#!/bin/bash
# this is the header comment
echo hi
```

### JavaScript

The command to run:

```bash
add-header \
  --header-filepath path/to/header.txt \
  --comment-style "//" \
  filepath1.js filepath2.js
```

Outputs a header like this:

```js
// this is the header comment
console.log('hi')
```

### Python with additional file specific custom header

The command to run:

```bash
add-header \
  --header-filepath path/to/header.txt \
  --stop-at-ignore-below \
  filepath1.py filepath2.py
```

Outputs a header like this:

```py
# this is the header comment
# this is another line of the header comment
# header ends here, ignore below
# This is a custom comment at the top of the file that is not modified by the pre-commit hook
import os
```
