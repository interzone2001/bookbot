# BookBot

BookBot is a flexible text analysis tool that counts words, analyzes character frequency, and provides random sentences from text files. This is my first [Boot.dev](https://www.boot.dev) project!

## Usage

### Basic Commands

```bash
# Show complete analysis (default)
python3 main.py book.txt
python3 main.py book.txt --all

# Show only word count
python3 main.py book.txt --word-count

# Show only character frequency
python3 main.py book.txt --char-count

# Show only a random sentence
python3 main.py book.txt --random-sentence

# Generate ASCII art word cloud
python3 main.py book.txt --wordcloud

# Generate ASCII art book cover
python3 main.py book.txt --book-cover

# Extract meaningful quotes for commonplace book
python3 main.py book.txt --quotes

# Get a random meaningful quote (perfect for daily inspiration)
python3 main.py book.txt --random-quote

# Output all analysis as JSON
python3 main.py book.txt --json

# Show help
python3 main.py --help
```

### Piping Examples

```bash
# Get just the word count for scripting
word_count=$(python3 main.py book.txt --word-count)

# Save character analysis to file
python3 main.py book.txt --char-count > char_analysis.txt

# Get random quote for daily inspiration
python3 main.py book.txt --random-sentence | cowsay

# Create visual word art
python3 main.py book.txt --wordcloud > word_art.txt

# Generate beautiful book covers for display
python3 main.py book.txt --book-cover > book_cover.txt

# Build your commonplace book with meaningful quotes
python3 main.py book.txt --quotes --theme=wisdom --count=5
python3 main.py book.txt --quotes --format=json | jq -r '.[].text'
python3 main.py book.txt --quotes --format=csv > quotes.csv

# Daily inspiration with random quotes
python3 main.py book.txt --random-quote --theme=hope
python3 main.py book.txt --random-quote | cowsay
echo "alias daily-wisdom='python3 main.py books/frankenstein.txt --random-quote'" >> ~/.bashrc

# Extract specific data with jq
python3 main.py book.txt --json | jq '.word_count'
python3 main.py book.txt --json | jq '.character_frequencies.e'

# Compare books using JSON output
python3 main.py book1.txt --json | jq '.word_count' > /tmp/count1
python3 main.py book2.txt --json | jq '.word_count' > /tmp/count2
paste /tmp/count1 /tmp/count2
```

## Features

- **Word Count**: Total number of words in the text
- **Character Frequency**: Alphabetical characters sorted by frequency 
- **Random Sentence**: A randomly selected sentence from the text
- **ASCII Word Cloud**: Visual representation of most frequent words as ASCII art
- **ASCII Book Cover**: Beautiful decorative book covers with metadata and themes
- **Smart Quote Extraction**: Meaningful passages perfect for commonplace books
- **Random Quote Generator**: Daily inspiration with intelligent quote selection
- **Theme Filtering**: Extract quotes by topic (love, death, wisdom, nature, etc.)
- **Multiple Output Formats**: Text, JSON, and CSV for maximum flexibility
- **JSON Output**: Complete analysis in JSON format for advanced scripting
- **Pipe-friendly**: Clean output perfect for scripting and automation
