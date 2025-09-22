# wordle_helper_v1

A Python GUI application that helps solve Wordle puzzles by analyzing your guesses and suggesting possible words based on the color feedback.

## Features

- Interactive 6×5 grid mimicking the Wordle interface
- Click cells to cycle through colors (Black → Yellow → Green)
- Type letters directly into cells
- Real-time constraint satisfaction solving
- Scrollable list of possible remaining words
- Keyboard shortcuts for efficient input

## Requirements

- Python 3.x
- tkinter (usually included with Python)
- A `words.txt` file containing valid 5-letter words (one per line)

## Installation

1. Clone or download this repository
2. Ensure you have a `words.txt` file in the same directory
   - You can download a word list from various sources online
   - Each line should contain exactly one 5-letter word
3. Run the application:
   ```bash
   python wordle_helper.py
   ```

## How to Use

### Basic Workflow
1. Enter your Wordle guess by typing letters
2. Click each cell to set the color based on Wordle's feedback:
   - **Black/Gray**: Letter not in the word
   - **Yellow**: Letter in word but wrong position  
   - **Green**: Letter in correct position
3. Press `Space` or click "Submit" to get possible words
4. Use the suggestions for your next guess
5. Repeat until solved!

### Keyboard Controls
- **Type letters**: Automatically fills cells left to right
- **Backspace**: Delete previous letter
- **Enter**: Move to next row
- **Space**: Submit and analyze current guesses

### Mouse Controls
- **Click cell**: Cycle through colors (Black → Yellow → Green)
- **Click Submit**: Analyze guesses and show possible words

## Algorithm

The solver uses **Constraint Satisfaction** with the following logic:

1. **Constraint Collection**: Gathers all color-based constraints from your guesses
2. **Pattern Matching**: Builds a regex pattern for valid positions
3. **Filtering**: Eliminates words that violate any constraints:
   - Words containing "black" letters (unless also yellow/green elsewhere)
   - Words missing required "yellow/green" letters
   - Words not matching position constraints

## File Structure

```
wordle_helper.py    # Main application
words.txt          # Word list (you need to provide this)
README.md          # This file
```

## Example Usage

Say you guessed "CRANE" and got:
- C: Black
- R: Yellow  
- A: Black
- N: Green
- E: Black

1. Type "CRANE" in the first row
2. Click cells to set: Black, Yellow, Black, Green, Black
3. Press Space to see all words that:
   - Don't contain C, A, or E
   - Have R somewhere (but not position 2)
   - Have N in position 4

## Word List

This project uses a comprehensive dictionary of 5-letter words from [this GitHub gist](https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93) containing **14,000+ words**. 

**Note**: This extensive list includes many obscure and uncommon English 5-letter words, far beyond the ~2,300 words that can appear as official Wordle solutions. While this gives you maximum coverage and will help solve any Wordle puzzle, it may suggest some very uncommon words that wouldn't actually be Wordle answers.

To set up the word list:
1. Download the raw content from the gist above  
2. Save it as `words.txt` in the same directory as the Python script
3. Ensure each line contains exactly one 5-letter word in lowercase

Format: one word per line, all lowercase, exactly 5 letters each.

**Tip**: If you want fewer obscure suggestions, you could manually curate the list to remove uncommon words, but the comprehensive list ensures you won't miss any valid possibilities.

## Contributing

Feel free to submit issues or pull requests to improve the solver algorithm or user interface!

## License

This project is open source. Use and modify as needed.
