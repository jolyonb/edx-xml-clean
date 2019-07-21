"""
xml_exceptions.py

Contains exception definitions for XML loading
"""
from edx_xml_clean.exceptions import CourseError, ErrorLevel

class CourseXMLDoesNotExist(CourseError):
    """The supplied `course.xml` file does not exist (or could not be opened)."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self._description = f"The file '{filename}' does not exist."

class InvalidXML(CourseError):
    """The specified XML file has a syntax error."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - error, text describing the XML error
        """
        super().__init__(filename)
        self._description = kwargs['error']

class InvalidHTML(CourseError):
    """The specified HTML file has a syntax error"""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - error, text describing the XML error
        """
        super().__init__(filename)
        self._description = kwargs['error']

class CourseXMLName(CourseError):
    """The master file was not called `course.xml`."""
    _level = ErrorLevel.WARNING

    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self._description = f"The course file, {filename}, is not named course.xml"

class TagMismatch(CourseError):
    """A file purporting to contain a specific tag type (e.g., `problem` or `chapter`) instead contains a different tag."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag1
        - tag2
        """
        super().__init__(filename)
        self._description = (f"A file is of type <{kwargs['tag1']}> but "
                             f"opens with a <{kwargs['tag2']}> tag")

class EmptyTag(CourseError):
    """A tag was unexpectedly empty (e.g., a `chapter` tag had no children)."""
    _level = ErrorLevel.WARNING

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag
        - url_name
        """
        super().__init__(filename)
        if kwargs['url_name']:
            self._description = (f"The <{kwargs['tag']}> tag with url_name '{kwargs['url_name']}' "
                                 f"is unexpectedly empty")
        else:
            self._description = f"A <{kwargs['tag']}> tag with no url_name is unexpectedly empty"

class ExtraURLName(CourseError):
    """A tag that had been pointed to by `url_name` from another file has a `url_name` of its own."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag
        """
        super().__init__(filename)
        self._description = f"The opening <{kwargs['tag']}> tag shouldn't have a url_name attribute"

class InvalidPointer(CourseError):
    """This tag appears to be trying to point to another file, but contains unexpected attributes, and is hence not pointing."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag
        - url_name
        """
        super().__init__(filename)
        self._description = (f"The <{kwargs['tag']}> tag with url_name '{kwargs['url_name']}' "
                             f"looks like it is an invalid pointer tag")

class FileDoesNotExist(CourseError):
    """The file being pointed to does not exist."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag
        - url_name
        - new_file
        """
        super().__init__(filename)
        self._description = (f"The <{kwargs['tag']}> tag with url_name {kwargs['url_name']} points to "
                             f"the file {kwargs['new_file']} that does not exist")

class SelfPointer(CourseError):
    """A tag appears to be pointing to itself."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag
        - url_name
        """
        super().__init__(filename)
        self._description = (f"The tag <{kwargs['tag']}> with url_name {kwargs['url_name']} "
                             f"appears to be pointing to itself")

class UnexpectedTag(CourseError):
    """A tag was found in an inappropriate location (e.g., a `vertical` in a `chapter`), or the tag was not recognized."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag, the unexpected tag
        - parent, the parent tag
        - url_name, the parent tag url_name (or None)
        """
        super().__init__(filename)
        if kwargs['url_name']:
            self._description = (f"A <{kwargs['tag']}> tag was unexpectedly found inside the <{kwargs['parent']}> tag with "
                                 f"url_name {kwargs['url_name']}")
        else:
            self._description = (f"A <{kwargs['tag']}> tag was unexpectedly found inside a <{kwargs['parent']}> tag with "
                                 f"no url_name")

class PossiblePointer(CourseError):
    """This tag looks like it isn't a pointer tag, but a file exists that it could be trying to point to. (This file is thus orphaned, as no other tag can point to it due to `url_name` clashes.)"""
    _level = ErrorLevel.WARNING

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag
        - url_name
        - new_file
        """
        super().__init__(filename)
        self._description = (f"The <{kwargs['tag']}> tag with url_name '{kwargs['url_name']}' "
                             f"is not a pointer, but a file that it could point to exists ({kwargs['new_file']})")

class UnexpectedContent(CourseError):
    """A tag contains unexpected text content."""
    _level = ErrorLevel.ERROR

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag
        - url_name (or None)
        - text
        """
        super().__init__(filename)
        if kwargs['url_name']:
            self._description = f"The <{kwargs['tag']}> tag with url_name '{kwargs['url_name']}'"
        else:
            self._description = f"A <{kwargs['tag']}> tag with no url_name"
        self._description += f" should not contain any text ({kwargs['text'].strip()[:10]}...)"

class NonFlatURLName(CourseError):
    """A `url_name` pointer uses colon notation to point to a subdirectory. While partially supported, this is not recommended."""
    _level = ErrorLevel.WARNING

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - tag
        - url_name
        """
        super().__init__(filename)
        self._description = (f"The <{kwargs['tag']}> tag with url_name {kwargs['url_name']} "
                             f"uses obsolete colon notation in the url_name to point to a subdirectory")

class NonFlatFilename(CourseError):
    """A filename pointer for an HTML file uses colon notation to point to a subdirectory. While partially supported, this is not recommended."""
    _level = ErrorLevel.WARNING

    def __init__(self, filename, **kwargs):
        """
        Expects kwargs:
        - url_name
        """
        super().__init__(filename)
        if kwargs['url_name']:
            self._description = (f"The <html> tag with url_name {kwargs['url_name']} "
                                 f"uses obsolete colon notation to point to a subdirectory for filename {filename}")
        else:
            self._description = (f"An <html> tag with no url_name "
                                 f"uses obsolete colon notation to point to a subdirectory for filename {filename}")