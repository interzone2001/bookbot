from stats import count_words_book, count_characters_book, count_characters_sorted
import sys

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



def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)
    book_path=sys.argv[1]
    book=get_book_text(book_path)
    num_words=count_words_book(book)
    num_characters=count_characters_book(book)
    sorted_characters=count_characters_sorted(num_characters)
    print("============ BOOKBOT ============")
    print(f"Analyzing book found at {book_path}...")
    print("----------- Word Count ----------")
    print(f"Found {num_words} total words")
    print("--------- Character Count -------")
    for char in sorted_characters:
        c=char["char"]
        n=char["num"]
        if c.isalpha():
            print(f"{c}: {n}")
    print("============= END ===============")    
            
main()

