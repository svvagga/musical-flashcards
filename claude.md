### Objective

Create a series of flashcards to help me memorise musical notes on treble and bass clefs.


### Implementation

Created a Python script (`generate_flashcards.py`) that generates professional musical note flashcards using PIL.

**Features:**
- Uses professional treble and bass clef background images (`treble.png` and `bass-clef.png`)
- Generates 26 flashcards total:
  - 13 treble clef notes (C below stave to A above)
  - 13 bass clef notes (E below stave to C above)
- Musical notes include stems for realistic appearance
- Black and white only

**Card Layout:**
```
╭―――――――――――――――――――――――┬―――――――――――――――――――――――╮
│                       │                       │
│   Stave with note     │    Answer (upside     │
│   (treble/bass clef)  │    down - rotated     │
│   with stem           │    180°)              │
│                       │                       │
╰―――――――――――――――――――――――┴―――――――――――――――――――――――╯
```

**Specifications:**
- Card size: 69mm × 27mm (folds to 34.5mm × 27mm)
- Page layout: Landscape A4 with 4 columns × 7 rows (28 spaces, 26 cards)
- Print margin: 10mm on all sides
- Black borders around each card (cut lines)
- Dashed gray fold line down the center
- Answer text rotated 180° so it's right-side up when card is flipped over
- All cards fit on one landscape A4 sheet

**Usage:**
1. Run: `python3 generate_flashcards.py`
2. Print `flashcards_sheet_1.png` in landscape orientation
3. Cut along black borders
4. Fold each card along the dashed center line
5. Flip the card over to see the answer right-side up

