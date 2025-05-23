from stats import count_words_book, count_characters_book, count_characters_sorted, get_random_sentence, generate_ascii_wordcloud, generate_book_cover, extract_smart_quotes, format_quote_for_display, get_random_meaningful_quote
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

def output_quotes(book, args):
    quotes = extract_smart_quotes(
        book, 
        min_words=args.min_words,
        max_words=args.max_words,
        count=args.count,
        theme_filter=args.theme
    )
    
    if args.format == 'json':
        print(json.dumps(quotes, indent=2))
    elif args.format == 'csv':
        print("text,score,word_count,themes,context")
        for quote in quotes:
            themes_str = "|".join(quote['themes'])
            # Escape quotes in text for CSV
            text = quote['text'].replace('"', '""')
            print(f'"{text}",{quote["score"]:.3f},{quote["word_count"]},"{themes_str}",{quote["context"]}')
    else:
        # Default: clean text format perfect for piping with proper formatting
        for i, quote in enumerate(quotes, 1):
            if args.show_metadata:
                themes_str = ", ".join(quote['themes'])
                print(f"[{i}] Score: {quote['score']:.2f} | Themes: {themes_str} | Context: {quote['context']}")
                print()  # Add space before quote
            
            # Format quote with proper line breaks and word wrapping
            formatted_quote = format_quote_for_display(quote['text'], width=80)
            print(formatted_quote)
            
            if i < len(quotes):
                print()  # Add spacing between quotes

def output_random_quote(book, args):
    quote = get_random_meaningful_quote(
        book,
        min_words=args.min_words,
        max_words=args.max_words,
        theme_filter=args.theme
    )
    
    if not quote:
        print("No meaningful quotes found with the specified criteria.")
        return
    
    if args.format == 'json':
        print(json.dumps(quote, indent=2))
    elif args.format == 'csv':
        themes_str = "|".join(quote['themes'])
        text = quote['text'].replace('"', '""')
        print("text,score,word_count,themes,context")
        print(f'"{text}",{quote["score"]:.3f},{quote["word_count"]},"{themes_str}",{quote["context"]}')
    else:
        # Default: beautiful formatted display
        if args.show_metadata:
            themes_str = ", ".join(quote['themes'])
            print(f"💫 Random Quote | Score: {quote['score']:.2f} | Themes: {themes_str} | Context: {quote['context']}")
            print()
        
        # Format quote with proper line breaks
        formatted_quote = format_quote_for_display(quote['text'], width=80)
        print(formatted_quote)

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
    parser.add_argument("--quotes", action="store_true", help="Extract meaningful quotes for commonplace book")
    parser.add_argument("--random-quote", action="store_true", help="Get a single random meaningful quote (perfect for daily inspiration)")
    parser.add_argument("--json", action="store_true", help="Output all analysis as JSON")
    
    # Quote-specific options
    parser.add_argument("--count", type=int, default=10, help="Number of quotes to extract (default: 10)")
    parser.add_argument("--min-words", type=int, default=8, help="Minimum words per quote (default: 8)")
    parser.add_argument("--max-words", type=int, default=50, help="Maximum words per quote (default: 50)")
    parser.add_argument("--theme", type=str, help="Filter quotes by theme (love, death, wisdom, nature, power, freedom, justice, hope, fear, beauty)")
    parser.add_argument("--format", choices=['text', 'json', 'csv'], default='text', help="Output format (default: text)")
    parser.add_argument("--show-metadata", action="store_true", help="Include scores and themes in text output")
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
    if not any([args.word_count, args.char_count, args.random_sentence, args.wordcloud, args.book_cover, args.quotes, args.random_quote, args.json, args.all]):
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
    elif args.quotes:
        output_quotes(book, args)
    elif args.random_quote:
        output_random_quote(book, args)
    elif args.json:
        output_json(book, args.file)
    elif args.all:
        output_all(book, args.file)

if __name__ == "__main__":
    main()

