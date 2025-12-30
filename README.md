# Musical Note Flashcards Generator

A Python script that generates printable flashcards for learning musical notes on treble and bass clefs.

## Features

- **Professional Design**: Uses high-quality treble and bass clef background images
- **Complete Coverage**: 26 flashcards covering common notes on both clefs
  - 13 treble clef notes (C below the stave to A above)
  - 13 bass clef notes (E below the stave to C above)
- **Realistic Notation**: Musical notes include stems for authentic appearance
- **Optimized Layout**: All cards fit on a single landscape A4 sheet
- **Print-Ready**: Includes cut lines, fold lines, and proper margins
- **Smart Design**: Answer text is rotated 180° so it appears right-side up when the card is flipped

## Requirements

- Python 3.x
- PIL/Pillow library

Install dependencies:
```bash
pip install Pillow
```

## Files

- `generate_flashcards.py` - Main script to generate flashcards
- `treble.png` - Treble clef background image
- `bass-clef.png` - Bass clef background image
- `CLAUDE.md` - Project documentation and specifications

## Usage

1. **Generate the flashcards:**
   ```bash
   python3 generate_flashcards.py
   ```

2. **Print the output:**
   - Open `flashcards_sheet_1.png`
   - Print in **landscape orientation** on A4 paper
   - Use high-quality print settings for best results

3. **Assemble the cards:**
   - Cut along the black borders
   - Fold each card along the dashed center line
   - The musical note will be on one side, the answer on the other

## Specifications

| Property | Value |
|----------|-------|
| Card Size (unfolded) | 69mm × 27mm |
| Card Size (folded) | 34.5mm × 27mm |
| Page Orientation | Landscape A4 |
| Layout | 4 columns × 7 rows |
| Total Cards | 26 (fits on 1 page) |
| Print Margin | 10mm on all sides |
| Resolution | 300 DPI |
| Color | Black and white |

## Card Layout

Each flashcard has two sides separated by a fold line:

```
╭――――――――――――――――――――――┬―――――――――――――――――――――――╮
│                       │                       │
│   Musical Stave       │    Note Name          │
│   with Clef & Note    │    (rotated 180°)     │
│   (with stem)         │                       │
│                       │                       │
╰――――――――――――――――――――――┴―――――――――――――――――――――――╯
     Front                    Back (flipped)
```

## Customization

You can modify the following constants in `generate_flashcards.py`:

- `CARD_WIDTH_MM` / `CARD_HEIGHT_MM` - Card dimensions
- `MARGIN_MM` - Print margin size
- `TREBLE_NOTES` / `BASS_NOTES` - Which notes to include

## Output

Running the script generates:
- `flashcards_sheet_1.png` - Complete sheet with all 26 flashcards

## Tips

- Print on cardstock for more durable flashcards
- Consider laminating the cards for long-term use
- Use a paper cutter for straight, even cuts
- Score the fold line lightly before folding for a crisp crease

## License

This project is provided as-is for educational purposes.
