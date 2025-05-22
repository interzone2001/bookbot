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

def count_characters_sorted(character_count):
    char_list=[]
    for k,v in character_count.items():
	    char_list.append({"char":k,"num":v})
    char_list.sort(key=lambda x: x["num"], reverse=True)
    return char_list

def get_random_sentence(book):
    import random
    import re
    sentences = re.split(r'[.!?]+', book)
    sentences = [s.strip() for s in sentences if s.strip()]
    if sentences:
        return random.choice(sentences)
    return "No sentences found."

