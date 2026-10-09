# Environment, Section 14.7 figures

Chapter 14 (Digitalisation), Section 14.7, IPCC WGIII AR7 First Order Draft.
`env/` is shared at chapter level, so these files name the section they belong
to and sit beside any other author's files.

## Python packages

```
pip install -r requirements_sec14.7.txt
```

Interpreter: Python 3.12.3. The pinned versions are the ones that
produced and verified the committed renders.

## Fonts, a system dependency pip cannot satisfy

The scripts require the Arial and Arial Narrow TrueType families. `code/ar7_style.py` finds
them through matplotlib's system font list, so no font directory is hard-coded.
If the families live outside the system font path, set the `AR7_FONT_DIR`
environment variable to the folder holding them; registration fails with a
message naming the missing family when neither source provides it.

`ar7_style.py` also renames the Arial Narrow entries in matplotlib's font
manager, because their name tables report the family as Arial with a condensed
stretch, which would otherwise make the family unselectable by name.

Every figure script self-checks that all rendered text resolves to an
Arial-family font file, and exits non-zero otherwise.

Uberhand Pro, the AR7 style guide's annotation font, is not installed on the
render machine. Annotations render in Arial Italic instead, recorded in
`ar7_style.ANNOTATION_FONT`. This substitution is an open question with the TSU.

## Reproduction

Byte-identical PNG reproduction is expected on this pinned stack with these
fonts. Different font files or library versions may shift glyph metrics and
produce output that looks the same but differs byte for byte.
