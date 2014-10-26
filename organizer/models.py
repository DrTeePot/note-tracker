from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    profile info:
    is this needed (only if social platform as well?) (maybe integrate app with google and facebook for auth)

    directory:
    folders
    notes

    created styles:
    inherit all default NoteStyles, SectionStyles,
    any user-created styles(can be created from anywhere, or imported)
    """

    # user profile info, expand as socials increase
    user = models.OneToOneField(User)

    # user directory, root /
    folders = models.ManyToManyField(Folder)
    notes = models.ManyToManyField(Note)

    # user and default created styles
    note_styles = models.ManyToManyField(NoteStyle)
    section_styles = models.ManyToManyField(SectionStyle)


class Folder(models.Model):
    """
    name

    parent
    children folders
    children notes

    default note-style
    """
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(UserProfile)

    parent = models.ForeignKey('self')
    children_notes = models.ManyToManyField('Note')

    default_note_style = models.ForeignKey(NoteStyle)


class Note(models.Model):
    """
    NoteStyle - defines styles that can be done in the note
    Page - Things that are in the note (notes are a collection of pages)
    UserProfile - owner

    People will create a note, with a defined style, and in order to write will create a page.
    Pages will correspond to a subject, date, etc (whatever they want)
    """

    owner = models.ForeignKey(UserProfile)
    note_style = models.ForeignKey(NoteStyle)
    pages = models.ManyToManyField(Page)


class NoteStyle(models.Model):
    """
    SectionStyles - defines sections that are creatable (multiple) (various defaults for math, english, etc)
    ElementStyles - defines elements that are creatable (multiple) (various defaults for math, english, etC)
    PageStyle - defines the page style (single) (user defined on note creation)

    Note appearance
    """
    section_types = models.ManyToManyField(SectionStyle)
    # element_types = models.ManyToManyField(ElementStyle) TODO see if necessary
    page_style = models.ForeignKey(PageStyle)


class Page(models.Model):
    """
    Pages contain sections

    Text - text with section markers and includes Element source
    text is parsed to show sections and elements (this is source)
    """
    text = models.TextField()


class PageStyle(models.Model):
    """
    What the page looks like (formatting)
    """
    pass


class Section(models.Model):
    """
    A section is a collection of fields, shown in a way defined by it's style

    allowed users - users who can see this
    section command used
    section name

    number of fields
    fields - collection of text elements
    """
    privacy = models.IntegerField(choices=(
        (0, 'Private'),
        (1, 'Shared'),
        (2, 'Public')
    ), default=0)
    allowed_users = models.ManyToManyField(UserProfile)  # will be only one user if public or private

    style = models.ForeignKey(SectionStyle)
    name = models.CharField(max_length=128)
    fields = models.ManyToManyField(Field)


class SectionStyle(models.Model):
    """
    A valid section that can be created
    command - the command used to create this section
    description - a description of what this section is used for
    fields - the fields that make up this section

    !!! TODO implement correctly !!!
    auto_name - if true, creates a first field that creates a
        numbered name in the format "text [page#].[section#]" on
        creation
    auto_name_text - the text for the above
    """
    command = models.CharField(max_length=32)
    description = models.CharField(max_length=512)
    fields = models.ManyToManyField(FieldStyle)
    # TODO implement correctly
    auto_name = models.BooleanField(default=False)
    auto_name_text = models.CharField(max_length=256)


class Field(models.Model):
    """
    Field information is stored here:

    descriptor - the formatting and other specs for this field
    text - the actual text in the field
    """
    descriptor = models.ForeignKey(FieldStyle)
    text = models.TextField()


class FieldStyle(models.Model):
    """
    Dictates what a certain field looks like. (describes the field)
    Fields will create a span element with inline css

    name - the name of this style
    description - what this field is used for
    styles - the styles that are applied to the span element
    """
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    styles = models.CharField(max_length=512)

# TODO check if this is necessary
# class ElementStyle(models.Model):
#     """
#     code that replaces source ie \E -> sum notation
#     used by interpreter to replace elements and make
#         pretty math stuff
#
#     command - the command used to specify an element
#     description - the description of what this element is
#     replacement - the things to replace the command
#     """
#     pass