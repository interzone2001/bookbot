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

def count_words_book(book):
    words_list=[]
    words_list=book.split()
    return len(words_list)


def main():
    frankenstein_book=get_book_text("/home/workspace/github.com/interzone2001/bookbot/books/frankenstein.txt")
    num_words=count_words_book(frankenstein_book)
    print(f"{num_words} words found in the document")

main()

