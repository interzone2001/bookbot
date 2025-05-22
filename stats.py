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

def get_top_words(book, count=20):
    import re
    # Convert to lowercase and extract words (letters only)
    words = re.findall(r'\b[a-zA-Z]+\b', book.lower())
    
    # Common stop words to filter out
    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'their', 'our', 'its', 'as', 'so', 'if', 'when', 'where', 'why', 'how', 'what', 'who', 'which', 'than', 'then', 'now', 'here', 'there', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'once', 'more', 'most', 'other', 'some', 'any', 'each', 'every', 'all', 'both', 'few', 'many', 'much', 'several', 'such', 'no', 'not', 'only', 'own', 'same', 'very', 'just', 'even', 'also', 'still', 'well', 'first', 'last', 'long', 'little', 'good', 'great', 'large', 'small', 'right', 'left', 'new', 'old', 'high', 'low', 'next', 'early', 'late', 'much', 'many', 'few', 'little', 'more', 'most', 'less', 'least', 'enough', 'quite', 'rather', 'too', 'very', 'really', 'almost', 'already', 'always', 'never', 'sometimes', 'often', 'usually', 'probably', 'perhaps', 'maybe', 'certainly', 'surely', 'definitely', 'absolutely'}
    
    # Filter meaningful words and count them
    word_count = {}
    for word in words:
        if word not in stop_words and len(word) > 2:  # Skip short words
            word_count[word] = word_count.get(word, 0) + 1
    
    # Sort by frequency and return top words
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:count]

def generate_ascii_wordcloud(book, width=90, height=25):
    import random
    import math
    
    # Get more words for a richer cloud
    top_words = get_top_words(book, 25)
    if not top_words:
        return "No meaningful words found."
    
    # Create empty canvas
    canvas = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Scale word sizes based on frequency (like a real word cloud)
    max_freq = top_words[0][1]
    min_freq = top_words[-1][1] if len(top_words) > 1 else max_freq
    
    def get_font_size(freq, rank):
        if max_freq == min_freq:
            return 2
        # Scale from 1 to 5 based on frequency
        normalized = (freq - min_freq) / (max_freq - min_freq)
        base_size = int(normalized * 4) + 1
        
        # Ensure top 3 words are clearly largest
        if rank == 0:
            return 5
        elif rank <= 2:
            return max(4, base_size)
        else:
            return base_size
    
    def create_word_art(word, font_size):
        word_upper = word.upper()
        
        if font_size >= 5:  # Extra large - bold with heavy borders
            padding = "█" * (len(word_upper) + 6)
            middle_padding = "██" + " " * (len(word_upper) + 2) + "██"
            return [
                padding,
                "██ " + word_upper + " ██",
                middle_padding,
                padding
            ]
            
        elif font_size >= 4:  # Large - thick borders
            return [
                "▓▓▓" + "▓" * len(word_upper) + "▓▓▓",
                "▓▓ " + word_upper + " ▓▓",
                "▓▓▓" + "▓" * len(word_upper) + "▓▓▓"
            ]
            
        elif font_size >= 3:  # Medium-large - double border
            return [
                "██" + "█" * len(word_upper) + "██",
                "█ " + word_upper + " █",
                "██" + "█" * len(word_upper) + "██"
            ]
            
        elif font_size >= 2:  # Medium - stylish border
            return [
                "╔═" + "═" * len(word_upper) + "═╗",
                "║ " + word_upper + " ║",
                "╚═" + "═" * len(word_upper) + "═╝"
            ]
            
        else:  # Small - minimal
            return [word_upper]
    
    # Place words on canvas (like real word cloud placement)
    placed_words = []
    
    for i, (word, freq) in enumerate(top_words):
        font_size = get_font_size(freq, i)
        word_art = create_word_art(word, font_size)
        
        if not word_art:
            continue
            
        word_width = len(max(word_art, key=len))
        word_height = len(word_art)
        
        # Try to place the word (many attempts for good placement)
        placed = False
        for attempt in range(200):  # More attempts for better placement
            # Bias placement toward center for important words, random for others
            if i < 3:  # Top 3 words near center
                center_x, center_y = width // 2, height // 2
                x = center_x + random.randint(-width//3, width//3) - word_width//2
                y = center_y + random.randint(-height//3, height//3) - word_height//2
            elif i < 8:  # Medium importance words in middle area
                x = random.randint(width//6, 5*width//6 - word_width)
                y = random.randint(height//6, 5*height//6 - word_height)
            else:  # Other words anywhere with more spread
                x = random.randint(1, width - word_width - 1)
                y = random.randint(1, height - word_height - 1)
            
            # Ensure word fits in canvas
            if x < 0 or y < 0 or x + word_width >= width or y + word_height >= height:
                continue
            
            # Check for overlaps with proper spacing buffer
            can_place = True
            buffer = 2  # Minimum space between words
            for dy in range(-buffer, word_height + buffer):
                for dx in range(-buffer, word_width + buffer):
                    check_y, check_x = y + dy, x + dx
                    if 0 <= check_y < height and 0 <= check_x < width:
                        if canvas[check_y][check_x] != ' ':
                            can_place = False
                            break
                if not can_place:
                    break
            
            if can_place:
                # Place the word
                for dy, line in enumerate(word_art):
                    for dx, char in enumerate(line):
                        if dx < len(line) and char != ' ':
                            if y + dy < height and x + dx < width:
                                canvas[y + dy][x + dx] = char
                placed_words.append((word, freq, font_size))
                placed = True
                break
        
        # If we couldn't place it, that's ok - word clouds often can't fit everything
    
    # Convert canvas to string
    result = []
    
    # Add header
    result.append("╔" + "═" * (width-2) + "╗")
    result.append("║" + " ASCII WORD CLOUD ".center(width-2) + "║")
    result.append("╚" + "═" * (width-2) + "╝")
    result.append("")
    
    # Add canvas
    for row in canvas:
        line = ''.join(row).rstrip()
        result.append(line)
    
    # Add footer with stats
    result.append("")
    result.append("─" * width)
    result.append(f"Words displayed: {len(placed_words)} | Most frequent: {top_words[0][0].upper()} ({top_words[0][1]}x)".center(width))
    result.append("─" * width)
    
    return '\n'.join(result)

