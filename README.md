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
- **JSON Output**: Complete analysis in JSON format for advanced scripting
- **Pipe-friendly**: Clean output perfect for scripting and automation
