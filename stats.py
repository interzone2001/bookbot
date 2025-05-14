def count_words_book(book):
    words_list=[]
    words_list=book.split()
    return len(words_list)

def count_characters_book(book):
    book=book.lower()
    character_count = {}
    for char in book:
        character_count[char] = character_count.get(char, 0) + 1
    return character_count

    
