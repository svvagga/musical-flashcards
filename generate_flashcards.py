#!/usr/bin/env python3
"""
Musical Note Flashcard Generator
Creates printable flashcards for learning treble and bass clef notes.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# Constants (all measurements in pixels at 300 DPI)
DPI = 300
MM_TO_INCH = 1 / 25.4

# Flashcard dimensions (unfolded)
# Sized to fit 4x7 = 28 cards on one landscape A4 sheet
CARD_WIDTH_MM = 69  # 34.5mm folded in half
CARD_HEIGHT_MM = 27
CARD_WIDTH = int(CARD_WIDTH_MM * MM_TO_INCH * DPI)
CARD_HEIGHT = int(CARD_HEIGHT_MM * MM_TO_INCH * DPI)

# A4 dimensions (landscape orientation)
A4_WIDTH = int(297 * MM_TO_INCH * DPI)  # 297mm wide (landscape)
A4_HEIGHT = int(210 * MM_TO_INCH * DPI)  # 210mm tall (landscape)

# Print margins (in mm)
MARGIN_MM = 10
MARGIN = int(MARGIN_MM * MM_TO_INCH * DPI)

# Load background images
TREBLE_BG = None
BASS_BG = None

def load_backgrounds():
    """Load and cache the background images."""
    global TREBLE_BG, BASS_BG

    treble_path = "treble.png"
    bass_path = "bass-clef.png"

    def load_and_convert(path):
        """Load image and properly convert to black and white RGB."""
        img = Image.open(path)

        # Handle transparency by compositing onto white background
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # Create white background
            background = Image.new('RGB', img.size, 'white')
            if img.mode == 'P':
                img = img.convert('RGBA')
            # Composite image onto white background
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        else:
            img = img.convert('RGB')

        return img

    if os.path.exists(treble_path):
        TREBLE_BG = load_and_convert(treble_path)
    else:
        print(f"Warning: {treble_path} not found")

    if os.path.exists(bass_path):
        BASS_BG = load_and_convert(bass_path)
    else:
        print(f"Warning: {bass_path} not found")


def get_stave_info(bg_image):
    """
    Analyze background image to find stave line positions.
    Returns the pixel positions of the 5 stave lines from top to bottom.
    """
    # The background images have staves with 5 lines
    # We need to detect these lines to properly position notes

    width, height = bg_image.size
    pixels = bg_image.load()

    # Scan vertically in the middle of the image to find black lines
    scan_x = width // 2
    lines = []
    in_line = False
    line_start = 0

    for y in range(height):
        pixel = pixels[scan_x, y]
        # Check if pixel is dark (black line)
        is_dark = sum(pixel[:3]) < 384  # Less than 128 average

        if is_dark and not in_line:
            in_line = True
            line_start = y
        elif not is_dark and in_line:
            in_line = False
            # Store the middle of the line
            lines.append((line_start + y) // 2)

    # We should have 5 lines
    if len(lines) >= 5:
        # Return the 5 most prominent lines
        return lines[:5]

    # Fallback: estimate line positions
    line_spacing = height // 6
    return [line_spacing * (i + 1) for i in range(5)]


def draw_note(draw, x, y, ledger_line=False):
    """Draw a note head (filled ellipse) and optionally a ledger line."""
    note_width = 38
    note_height = 28

    # Draw ledger line if needed
    if ledger_line:
        ledger_x_start = x - 25
        ledger_x_end = x + 25
        draw.line(
            [(ledger_x_start, y), (ledger_x_end, y)],
            fill='black',
            width=2
        )

    # Draw note head
    draw.ellipse(
        [(x - note_width//2, y - note_height//2),
         (x + note_width//2, y + note_height//2)],
        fill='black'
    )

    # Draw stem
    stem_y_start = y
    if(y>CARD_HEIGHT//2):
        stem_x = x + note_width//2
        stem_y_end = y - 80
    else:
        stem_x = x - note_width//2
        stem_y_end = y + 80
    draw.line(
        [(stem_x, stem_y_start), (stem_x, stem_y_end)],
        fill='black',
        width=6
    )


def create_flashcard(note_name, clef_type, position):
    """
    Create a single flashcard image.

    Args:
        note_name: Name of the note (e.g., "C", "D", "E")
        clef_type: "treble" or "bass"
        position: Vertical position (0 = bottom line, increases upward)
                 Negative values are below the stave, positive values above
    """
    img = Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), 'white')
    draw = ImageDraw.Draw(img)

    # Get the appropriate background image
    bg_image = TREBLE_BG if clef_type == "treble" else BASS_BG

    if bg_image:
        # Resize background to fit the left half of the card
        left_half_width = CARD_WIDTH // 2
        aspect_ratio = bg_image.height / bg_image.width
        new_height = int(left_half_width * aspect_ratio)

        # Center vertically
        if new_height > CARD_HEIGHT:
            new_height = CARD_HEIGHT
            new_width = int(new_height / aspect_ratio)
        else:
            new_width = left_half_width

        bg_resized = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Paste background centered on left half
        paste_x = (left_half_width - new_width) // 2
        paste_y = (CARD_HEIGHT - new_height) // 2
        img.paste(bg_resized, (paste_x, paste_y))

        # Get stave line positions from the resized background
        stave_lines = get_stave_info(bg_resized)

        if len(stave_lines) >= 5:
            # Calculate note position
            # Position 0 = bottom line (line 4, index 4)
            # Position increases going up
            # Even positions = on lines, odd = in spaces

            bottom_line_y = stave_lines[4] + paste_y
            line_spacing = (stave_lines[4] - stave_lines[0]) / 4

            # Calculate y position
            note_y = bottom_line_y - position * (line_spacing / 2)

            # Note x position (right side of stave)
            # note_x = paste_x + new_width - 60
            note_x = CARD_WIDTH / 3.5

            # Determine if we need ledger lines
            needs_ledger = position < -1 or position > 9

            draw_note(draw, note_x, int(note_y), needs_ledger)

    # Draw fold line in the middle (dashed)
    middle_x = CARD_WIDTH // 2
    dash_length = 10
    gap_length = 5
    y = 0
    while y < CARD_HEIGHT:
        draw.line(
            [(middle_x, y), (middle_x, min(y + dash_length, CARD_HEIGHT))],
            fill='gray',
            width=1
        )
        y += dash_length + gap_length

    # RIGHT SIDE: Answer (rotated 180 degrees for flip-over)
    try:
        # Try to use a nice font, fall back to default if not available
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        font = ImageFont.load_default()

    # Create text on a temporary image, then rotate it
    text = note_name
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Create temporary image for text
    text_img = Image.new('RGB', (text_width + 20, text_height + 20), 'white')
    text_draw = ImageDraw.Draw(text_img)
    text_draw.text((10, 10), text, fill='black', font=font)

    # Rotate 180 degrees
    text_img = text_img.rotate(180, expand=False)

    # Calculate position to center on right half
    text_x = middle_x + (CARD_WIDTH // 2 - text_img.width) // 2
    text_y = (CARD_HEIGHT - text_img.height) // 2

    # Paste the rotated text
    img.paste(text_img, (text_x, text_y))

    # Draw border (cut line) around the card
    draw.rectangle(
        [(0, 0), (CARD_WIDTH - 1, CARD_HEIGHT - 1)],
        outline='black',
        width=2
    )

    return img


# Note definitions
# Position values: 0 = bottom line, increases by 1 for each line/space going up
# Even numbers = lines, odd numbers = spaces

TREBLE_NOTES = [
    # Below stave
    ("C", -2),  # C below stave
    ("D", -1),  # D below stave
    # On stave
    ("E", 0),   # Bottom line
    ("F", 1),   # First space
    ("G", 2),   # Second line
    ("A", 3),   # Second space
    ("B", 4),   # Middle line
    ("C", 5),   # Third space
    ("D", 6),   # Fourth line
    ("E", 7),   # Fourth space
    ("F", 8),   # Top line
    # Above stave
    ("G", 9),   # Above stave
    ("A", 10),  # Above stave
]

BASS_NOTES = [
    # Below stave
    ("E", -2),  # E below stave
    ("F", -1),  # F below stave
    # On stave
    ("G", 0),   # Bottom line
    ("A", 1),   # First space
    ("B", 2),   # Second line
    ("C", 3),   # Second space
    ("D", 4),   # Middle line
    ("E", 5),   # Third space
    ("F", 6),   # Fourth line
    ("G", 7),   # Fourth space
    ("A", 8),   # Top line
    # Above stave
    ("B", 9),   # Above stave
    ("C", 10),  # Above stave
]


def arrange_on_a4(flashcards):
    """Arrange flashcards on A4 sheets with margins."""
    # Calculate printable area (after margins)
    printable_width = A4_WIDTH - (2 * MARGIN)
    printable_height = A4_HEIGHT - (2 * MARGIN)

    # Calculate how many cards fit on one sheet
    cards_per_row = printable_width // CARD_WIDTH
    cards_per_col = printable_height // CARD_HEIGHT
    cards_per_sheet = cards_per_row * cards_per_col

    print(f"Cards per sheet: {cards_per_sheet} ({cards_per_row} x {cards_per_col})")
    print(f"Print margin: {MARGIN_MM}mm on each side")

    sheets = []
    for sheet_num in range(0, len(flashcards), cards_per_sheet):
        sheet = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), 'white')

        cards_on_sheet = flashcards[sheet_num:sheet_num + cards_per_sheet]

        for idx, card in enumerate(cards_on_sheet):
            row = idx // cards_per_row
            col = idx % cards_per_row

            # Add margin offset to position
            x = MARGIN + (col * CARD_WIDTH)
            y = MARGIN + (row * CARD_HEIGHT)

            sheet.paste(card, (x, y))

        sheets.append(sheet)

    return sheets


def main():
    """Generate all flashcards and arrange them on A4 sheets."""
    print("Generating musical note flashcards...")

    # Load background images
    load_backgrounds()

    flashcards = []

    # Generate treble clef cards
    print(f"Creating {len(TREBLE_NOTES)} treble clef flashcards...")
    for note_name, position in TREBLE_NOTES:
        card = create_flashcard(note_name, "treble", position)
        flashcards.append(card)

    # Generate bass clef cards
    print(f"Creating {len(BASS_NOTES)} bass clef flashcards...")
    for note_name, position in BASS_NOTES:
        card = create_flashcard(note_name, "bass", position)
        flashcards.append(card)

    print(f"\nTotal flashcards: {len(flashcards)}")

    # Arrange on A4 sheets
    print("\nArranging flashcards on A4 sheets...")
    sheets = arrange_on_a4(flashcards)

    # Save sheets
    print(f"\nSaving {len(sheets)} A4 sheet(s)...")
    for idx, sheet in enumerate(sheets, 1):
        filename = f"flashcards_sheet_{idx}.png"
        sheet.save(filename, dpi=(DPI, DPI))
        print(f"Saved: {filename}")

    print("\nDone! Print the sheet(s) in landscape orientation and cut/fold each card along the center line.")
    print("Each card is 69mm x 27mm (folds to 34.5mm x 27mm).")


if __name__ == "__main__":
    main()
