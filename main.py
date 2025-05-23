from stats import count_words_book, count_characters_book, count_characters_sorted, get_random_sentence, generate_ascii_wordcloud, generate_book_cover
import sys
import argparse
import json

def get_book_text(bookpath):
    """
    Extracts the text from a book object.

    Args:
        book: The book file path to extract text from.

    Returns:
        str: The extracted text.
    """
    with open(bookpath) as f:
        book_text = f.read()

    # do something with f (the file) here
    return book_text



def output_word_count(book):
    num_words = count_words_book(book)
    print(f"{num_words}")

def output_char_count(book):
    num_characters = count_characters_book(book)
    sorted_characters = count_characters_sorted(num_characters)
    for char in sorted_characters:
        c = char["char"]
        n = char["num"]
        if c.isalpha():
            print(f"{c}: {n}")

def output_random_sentence(book):
    sentence = get_random_sentence(book)
    print(f'"{sentence}"')

def output_wordcloud(book):
    wordcloud = generate_ascii_wordcloud(book)
    print(wordcloud)

def output_book_cover(book):
    cover = generate_book_cover(book)
    print(cover)

def output_json(book, book_path):
    num_words = count_words_book(book)
    num_characters = count_characters_book(book)
    sorted_characters = count_characters_sorted(num_characters)
    random_sentence = get_random_sentence(book)
    
    # Filter to only alphabetical characters for JSON output
    char_frequencies = {}
    for char in sorted_characters:
        c = char["char"]
        n = char["num"]
        if c.isalpha():
            char_frequencies[c] = n
    
    result = {
        "file": book_path,
        "word_count": num_words,
        "character_frequencies": char_frequencies,
        "random_sentence": random_sentence
    }
    
    print(json.dumps(result, indent=2))

def output_all(book, book_path):
    num_words = count_words_book(book)
    num_characters = count_characters_book(book)
    sorted_characters = count_characters_sorted(num_characters)
    random_sentence = get_random_sentence(book)
    print("============ BOOKBOT ============")
    print(f"Analyzing book found at {book_path}...")
    print("----------- Word Count ----------")
    print(f"Found {num_words} total words")
    print("--------- Character Count -------")
    for char in sorted_characters:
        c = char["char"]
        n = char["num"]
        if c.isalpha():
            print(f"{c}: {n}")
    print("------- Random Sentence ---------")
    print(f'"{random_sentence}"')
    print("============= END ===============")

def main():
    parser = argparse.ArgumentParser(description="BookBot - Text analysis tool")
    parser.add_argument("file", help="Path to the text file to analyze")
    parser.add_argument("--word-count", action="store_true", help="Show word count only")
    parser.add_argument("--char-count", action="store_true", help="Show character frequency only")
    parser.add_argument("--random-sentence", action="store_true", help="Show random sentence only")
    parser.add_argument("--wordcloud", action="store_true", help="Generate ASCII art word cloud")
    parser.add_argument("--book-cover", action="store_true", help="Generate ASCII art book cover")
    parser.add_argument("--json", action="store_true", help="Output all analysis as JSON")
    parser.add_argument("--all", action="store_true", help="Show complete analysis (default)")
    
    args = parser.parse_args()
    
    try:
        book = get_book_text(args.file)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # If no specific flags are set, default to --all
    if not any([args.word_count, args.char_count, args.random_sentence, args.wordcloud, args.book_cover, args.json, args.all]):
        args.all = True
    
    if args.word_count:
        output_word_count(book)
    elif args.char_count:
        output_char_count(book)
    elif args.random_sentence:
        output_random_sentence(book)
    elif args.wordcloud:
        output_wordcloud(book)
    elif args.book_cover:
        output_book_cover(book)
    elif args.json:
        output_json(book, args.file)
    elif args.all:
        output_all(book, args.file)

if __name__ == "__main__":
    main()

