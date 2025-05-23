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
    
    # Comprehensive stop words list for thematic analysis
    # Basic function words
    basic_stop_words = {
        'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 
        'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 
        'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall', 'this', 
        'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 
        'her', 'us', 'them', 'my', 'your', 'his', 'their', 'our', 'its', 'as', 'so', 'if', 
        'when', 'where', 'why', 'how', 'what', 'who', 'which', 'than', 'then', 'now', 'here', 
        'there', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further', 'once', 
        'more', 'most', 'other', 'some', 'any', 'each', 'every', 'all', 'both', 'few', 'many', 
        'much', 'several', 'such', 'no', 'not', 'only', 'own', 'same', 'very', 'just', 'even', 
        'also', 'still', 'well', 'first', 'last', 'long', 'little', 'good', 'great', 'large', 
        'small', 'right', 'left', 'new', 'old', 'high', 'low', 'next', 'early', 'late', 'much', 
        'many', 'few', 'little', 'more', 'most', 'less', 'least', 'enough', 'quite', 'rather', 
        'too', 'very', 'really', 'almost', 'already', 'always', 'never', 'sometimes', 'often', 
        'usually', 'probably', 'perhaps', 'maybe', 'certainly', 'surely', 'definitely', 'absolutely'
    }
    
    # Book-specific and literary stop words
    book_stop_words = {
        'chapter', 'page', 'book', 'story', 'tale', 'text', 'author', 'writer', 'novel', 'volume',
        'part', 'section', 'paragraph', 'line', 'verse', 'passage', 'excerpt', 'quote', 'said', 
        'says', 'tell', 'told', 'asked', 'replied', 'answered', 'spoke', 'voice', 'word', 'words',
        'look', 'looked', 'see', 'saw', 'seen', 'eyes', 'face', 'hand', 'hands', 'head', 'way',
        'time', 'day', 'night', 'year', 'moment', 'place', 'room', 'house', 'door', 'window',
        'came', 'come', 'go', 'went', 'gone', 'get', 'got', 'give', 'gave', 'take', 'took', 'taken',
        'know', 'knew', 'think', 'thought', 'feel', 'felt', 'hear', 'heard', 'find', 'found',
        'turn', 'turned', 'walk', 'walked', 'run', 'ran', 'stand', 'stood', 'sit', 'sat',
        'put', 'set', 'let', 'made', 'make', 'call', 'called', 'keep', 'kept', 'leave', 'left'
    }
    
    # Combine all stop words
    stop_words = basic_stop_words | book_stop_words
    
    # Filter meaningful words and count them
    word_count = {}
    for word in words:
        # Enhanced filtering for thematic relevance
        if (word not in stop_words and 
            len(word) > 2 and  # Skip short words
            not word.isdigit() and  # Skip pure numbers
            not (len(word) == 3 and word.endswith('ing')) and  # Skip short -ing words
            word not in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']):  # Skip number words
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

def generate_book_cover(book, width=80, height=30):
    """Generate an ASCII art book cover with decorative borders and metadata"""
    import re
    from textwrap import wrap
    
    # Extract metadata from Project Gutenberg header
    metadata = extract_book_metadata(book)
    
    lines = []
    
    # Top decorative border
    lines.append("╔" + "═" * (width-2) + "╗")
    lines.append("║" + "░" * (width-2) + "║")
    
    # Title section with double borders
    title = metadata.get('title', 'Unknown Title')
    subtitle = metadata.get('subtitle', '')
    
    # Title processing - handle long titles
    title_lines = wrap_text_for_width(title.upper(), width - 6)
    
    lines.append("║" + " " * (width-2) + "║")
    for title_line in title_lines:
        lines.append("║" + title_line.center(width-2) + "║")
    
    if subtitle:
        lines.append("║" + " " * (width-2) + "║")
        subtitle_lines = wrap_text_for_width(subtitle.upper(), width - 6)
        for sub_line in subtitle_lines:
            lines.append("║" + sub_line.center(width-2) + "║")
    
    # Decorative separator
    lines.append("║" + " " * (width-2) + "║")
    lines.append("║" + "▓" * (width-2) + "║")
    lines.append("║" + " " * (width-2) + "║")
    
    # Author section
    author = metadata.get('author', 'Unknown Author')
    lines.append("║" + f"BY {author.upper()}".center(width-2) + "║")
    
    # Middle decorative section with thematic elements
    lines.append("║" + " " * (width-2) + "║")
    
    # Add thematic ASCII art based on key words from the book
    themes = get_book_themes(book)
    if themes:
        # Add label for thematic elements
        lines.append("║" + "~ KEY THEMES ~".center(width-2) + "║")
        lines.append("║" + " " * (width-2) + "║")
    
    thematic_art = generate_thematic_ascii_art(themes, width-4)
    for art_line in thematic_art:
        lines.append("║ " + art_line + " ║")
    
    # Publication info
    lines.append("║" + " " * (width-2) + "║")
    pub_year = metadata.get('year', '')
    if pub_year:
        lines.append("║" + f"PUBLISHED {pub_year}".center(width-2) + "║")
    
    # Bottom decorative border
    lines.append("║" + "░" * (width-2) + "║")
    lines.append("╚" + "═" * (width-2) + "╝")
    
    # Add ornamental corners and flourishes
    result = []
    for i, line in enumerate(lines):
        if i == 0 or i == len(lines) - 1:
            # Top and bottom get extra decoration
            result.append("  " + line + "  ")
        else:
            result.append("  " + line + "  ")
    
    return '\n'.join(result)

def extract_smart_quotes(book, min_words=8, max_words=50, count=10, theme_filter=None):
    """Extract meaningful quotes perfect for a commonplace book"""
    import re
    from collections import Counter
    
    # Clean the book text (remove Project Gutenberg boilerplate)
    clean_book = clean_gutenberg_text(book)
    
    # Split into sentences with better parsing
    sentences = extract_sentences(clean_book)
    
    # Score each sentence for meaningfulness
    scored_quotes = []
    for sentence in sentences:
        score = score_quote_quality(sentence, clean_book, theme_filter)
        word_count = len(sentence.split())
        
        if (min_words <= word_count <= max_words and 
            score > 0.3 and  # Minimum quality threshold
            not is_dialogue_or_mundane(sentence)):
            
            scored_quotes.append({
                'text': sentence.strip(),
                'score': score,
                'word_count': word_count,
                'themes': detect_quote_themes(sentence),
                'context': get_quote_context(sentence, clean_book)
            })
    
    # Sort by score and return top quotes
    scored_quotes.sort(key=lambda x: x['score'], reverse=True)
    return scored_quotes[:count]

def clean_gutenberg_text(book):
    """Remove Project Gutenberg boilerplate and clean text"""
    import re
    
    # Remove boilerplate
    start_pattern = r'\*\*\*\s*START OF.*?\*\*\*'
    end_pattern = r'\*\*\*\s*END OF.*'
    start_match = re.search(start_pattern, book, re.IGNORECASE | re.DOTALL)
    end_match = re.search(end_pattern, book, re.IGNORECASE | re.DOTALL)
    
    if start_match:
        book = book[start_match.end():]
    if end_match:
        book = book[:end_match.start()]
    
    # Remove chapter headers and numbering
    book = re.sub(r'\n\s*CHAPTER [IVXLC\d]+.*?\n', '\n', book, flags=re.IGNORECASE)
    book = re.sub(r'\n\s*Chapter [IVXLC\d]+.*?\n', '\n', book, flags=re.IGNORECASE)
    
    return book

def extract_sentences(text):
    """Extract sentences with intelligent parsing and paragraph preservation"""
    import re
    
    # Split on sentence endings but preserve quoted speech and paragraph breaks
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    
    # Clean and filter sentences
    cleaned = []
    for sentence in sentences:
        # Preserve paragraph breaks by normalizing to double newlines
        sentence = re.sub(r'\n\s*\n', ' ¶ ', sentence)  # Mark paragraph breaks
        # Remove excessive whitespace but preserve paragraph markers
        sentence = re.sub(r'(?<!¶)\s+', ' ', sentence).strip()
        
        # Skip very short or empty sentences
        if len(sentence) > 20 and len(sentence.split()) >= 4:
            cleaned.append(sentence)
    
    return cleaned

def score_quote_quality(sentence, full_text, theme_filter=None):
    """Score a sentence for quotability and philosophical depth"""
    import re
    from collections import Counter
    
    score = 0.0
    words = sentence.lower().split()
    
    # Philosophical/inspirational indicators
    wisdom_words = {
        'life', 'death', 'love', 'truth', 'beauty', 'wisdom', 'knowledge', 'power',
        'freedom', 'justice', 'honor', 'courage', 'hope', 'faith', 'destiny', 'fate',
        'soul', 'heart', 'mind', 'spirit', 'nature', 'human', 'humanity', 'mankind',
        'virtue', 'vice', 'good', 'evil', 'right', 'wrong', 'joy', 'sorrow', 'pain',
        'pleasure', 'happiness', 'misery', 'glory', 'shame', 'pride', 'humility',
        'passion', 'reason', 'emotion', 'feeling', 'thought', 'dream', 'vision',
        'purpose', 'meaning', 'existence', 'reality', 'imagination', 'memory'
    }
    
    # Memorable/quotable patterns
    memorable_patterns = [
        r'\b(never|always|all|every|nothing|everything)\b',  # Absolutes
        r'\b(if .+, then .+|when .+, .+)\b',  # Conditional wisdom
        r'\b(not .+ but .+|more .+ than .+)\b',  # Contrasts
        r'\b(the .+ of .+)\b',  # Definitive statements
        r'\b(it is .+|there is .+)\b'  # Declarations
    ]
    
    # Score wisdom words
    wisdom_count = sum(1 for word in words if word in wisdom_words)
    score += wisdom_count * 0.3
    
    # Score memorable patterns
    for pattern in memorable_patterns:
        if re.search(pattern, sentence, re.IGNORECASE):
            score += 0.4
    
    # Bonus for metaphorical language
    metaphor_indicators = ['like', 'as', 'seems', 'appears', 'resembles', 'mirror', 'echo']
    if any(word in words for word in metaphor_indicators):
        score += 0.2
    
    # Bonus for emotional depth
    emotion_words = {
        'fear', 'terror', 'horror', 'dread', 'anxiety', 'despair', 'anguish', 'agony',
        'ecstasy', 'bliss', 'rapture', 'delight', 'wonder', 'awe', 'admiration',
        'contempt', 'disgust', 'rage', 'fury', 'wrath', 'envy', 'jealousy', 'revenge'
    }
    emotion_count = sum(1 for word in words if word in emotion_words)
    score += emotion_count * 0.25
    
    # Penalty for overly simple language
    simple_words = {'the', 'and', 'but', 'or', 'so', 'very', 'just', 'only', 'really'}
    simple_ratio = sum(1 for word in words if word in simple_words) / len(words)
    if simple_ratio > 0.4:
        score -= 0.3
    
    # Bonus for sentence structure complexity
    if ';' in sentence or ':' in sentence:
        score += 0.2
    
    # Theme filtering
    if theme_filter:
        theme_words = get_theme_words(theme_filter)
        if any(word in words for word in theme_words):
            score += 0.5
        else:
            score *= 0.3  # Reduce score if doesn't match theme
    
    return max(0.0, score)

def is_dialogue_or_mundane(sentence):
    """Filter out dialogue and mundane statements"""
    import re
    
    # Skip obvious dialogue
    if (sentence.count('"') >= 2 or 
        sentence.count("'") >= 2 or
        re.search(r'\bsaid\b|\btold\b|\basked\b|\breplied\b', sentence, re.IGNORECASE)):
        return True
    
    # Skip mundane statements
    mundane_patterns = [
        r'\b(went to|came to|walked to|returned to)\b',
        r'\b(in the morning|in the evening|at night|yesterday|tomorrow)\b',
        r'\b(opened the door|closed the|entered the|left the)\b',
        r'\b(looked at|turned to|saw that|noticed that)\b'
    ]
    
    for pattern in mundane_patterns:
        if re.search(pattern, sentence, re.IGNORECASE):
            return True
    
    return False

def detect_quote_themes(sentence):
    """Detect thematic categories for the quote"""
    themes = []
    words = sentence.lower()
    
    theme_categories = {
        'love': ['love', 'heart', 'affection', 'devotion', 'passion', 'romance'],
        'death': ['death', 'die', 'grave', 'mortality', 'perish', 'expire'],
        'wisdom': ['wisdom', 'knowledge', 'learn', 'understand', 'truth', 'insight'],
        'nature': ['nature', 'earth', 'sky', 'sea', 'mountain', 'forest', 'flower'],
        'power': ['power', 'strength', 'force', 'control', 'command', 'authority'],
        'freedom': ['freedom', 'liberty', 'independence', 'escape', 'release'],
        'justice': ['justice', 'right', 'wrong', 'fair', 'law', 'moral', 'virtue'],
        'hope': ['hope', 'faith', 'believe', 'trust', 'optimism', 'future'],
        'fear': ['fear', 'terror', 'horror', 'dread', 'anxiety', 'worry'],
        'beauty': ['beauty', 'beautiful', 'lovely', 'elegant', 'graceful', 'sublime']
    }
    
    for theme, keywords in theme_categories.items():
        if any(keyword in words for keyword in keywords):
            themes.append(theme)
    
    return themes if themes else ['general']

def get_quote_context(sentence, full_text):
    """Get contextual information about where the quote appears"""
    # Find approximate location in text
    position = full_text.find(sentence[:50])  # Match beginning of sentence
    total_length = len(full_text)
    
    if position >= 0:
        percentage = int((position / total_length) * 100)
        if percentage < 25:
            return "early"
        elif percentage < 75:
            return "middle"
        else:
            return "late"
    
    return "unknown"

def get_theme_words(theme):
    """Get keywords for theme filtering"""
    theme_words = {
        'love': ['love', 'heart', 'affection', 'devotion', 'passion', 'romance', 'beloved'],
        'death': ['death', 'die', 'grave', 'mortality', 'perish', 'expire', 'funeral'],
        'wisdom': ['wisdom', 'knowledge', 'learn', 'understand', 'truth', 'insight', 'philosophy'],
        'nature': ['nature', 'earth', 'sky', 'sea', 'mountain', 'forest', 'flower', 'natural'],
        'power': ['power', 'strength', 'force', 'control', 'command', 'authority', 'might'],
        'freedom': ['freedom', 'liberty', 'independence', 'escape', 'release', 'free'],
        'justice': ['justice', 'right', 'wrong', 'fair', 'law', 'moral', 'virtue', 'honor'],
        'hope': ['hope', 'faith', 'believe', 'trust', 'optimism', 'future', 'dream'],
        'fear': ['fear', 'terror', 'horror', 'dread', 'anxiety', 'worry', 'afraid'],
        'beauty': ['beauty', 'beautiful', 'lovely', 'elegant', 'graceful', 'sublime', 'magnificent']
    }
    
    return theme_words.get(theme.lower(), [])

def get_random_meaningful_quote(book, min_words=8, max_words=50, theme_filter=None):
    """Get a single random meaningful quote - perfect for daily inspiration"""
    import random
    
    # Get a larger pool of quality quotes to choose from
    quotes = extract_smart_quotes(book, min_words, max_words, count=50, theme_filter=theme_filter)
    
    if not quotes:
        return None
    
    # For random selection, we want some variety in quality levels
    # Weight towards higher quality but allow some serendipity
    weights = []
    for quote in quotes:
        # Higher scores get higher weight, but even lower scores have a chance
        weight = max(1, int(quote['score'] * 10))  # Convert score to weight
        weights.append(weight)
    
    # Weighted random selection
    selected_quote = random.choices(quotes, weights=weights, k=1)[0]
    return selected_quote

def format_quote_for_display(quote_text, width=80):
    """Format a quote with proper line breaks and paragraph spacing"""
    import textwrap
    
    # Handle paragraph breaks marked with ¶
    if ' ¶ ' in quote_text:
        paragraphs = quote_text.split(' ¶ ')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                # Wrap each paragraph
                wrapped = textwrap.fill(paragraph, width=width, 
                                      break_long_words=False, 
                                      break_on_hyphens=True)
                formatted_paragraphs.append(wrapped)
        
        # Join paragraphs with double line breaks
        return '\n\n'.join(formatted_paragraphs)
    else:
        # Single paragraph - just wrap
        return textwrap.fill(quote_text, width=width, 
                           break_long_words=False, 
                           break_on_hyphens=True)

def extract_book_metadata(book):
    """Extract title, author, and other metadata from Project Gutenberg format"""
    import re
    
    metadata = {}
    
    # Extract title (look for "Title:" line)
    title_match = re.search(r'Title:\s*(.+?)(?:\n|$)', book, re.IGNORECASE)
    if title_match:
        full_title = title_match.group(1).strip()
        # Handle subtitles separated by semicolon, "or", etc.
        if ';' in full_title or ' or ' in full_title.lower():
            parts = re.split(r'[;]|\s+or\s+', full_title, 1, re.IGNORECASE)
            metadata['title'] = parts[0].strip()
            if len(parts) > 1:
                metadata['subtitle'] = parts[1].strip()
        else:
            metadata['title'] = full_title
    
    # Extract author
    author_match = re.search(r'Author:\s*(.+?)(?:\n|$)', book, re.IGNORECASE)
    if author_match:
        metadata['author'] = author_match.group(1).strip()
    
    # Extract publication year
    year_match = re.search(r'Original publication:.*?(\d{4})', book, re.IGNORECASE)
    if year_match:
        metadata['year'] = year_match.group(1)
    
    return metadata

def wrap_text_for_width(text, max_width):
    """Wrap text to fit within specified width"""
    if len(text) <= max_width:
        return [text]
    
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) <= max_width:
            current_line.append(word)
            current_length += len(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def get_book_themes(book):
    """Extract key thematic words for decorative elements"""
    # Use our existing word analysis but focus on evocative terms
    top_words = get_top_words(book, 15)  # Get more words to choose from
    
    # Filter for thematic/atmospheric words
    thematic_words = []
    atmospheric_terms = {
        'love', 'death', 'life', 'heart', 'soul', 'dark', 'light', 'night', 'day',
        'fear', 'hope', 'dream', 'mystery', 'magic', 'power', 'beauty', 'truth',
        'journey', 'adventure', 'destiny', 'fate', 'honor', 'courage', 'passion',
        'freedom', 'justice', 'revenge', 'betrayal', 'sacrifice', 'glory', 'wisdom',
        'nature', 'ocean', 'sea', 'storm', 'thunder', 'lightning', 'fire', 'water',
        'blood', 'battle', 'war', 'peace', 'victory', 'defeat', 'hero', 'villain'
    }
    
    # Words to avoid even if they're long
    avoid_words = {
        'though', 'through', 'thought', 'before', 'between', 'another', 'without',
        'within', 'during', 'because', 'however', 'therefore', 'although', 'while',
        'where', 'which', 'should', 'would', 'could', 'might', 'never', 'always',
        'something', 'nothing', 'everything', 'anything', 'someone', 'anyone',
        'everyone', 'myself', 'himself', 'herself', 'itself', 'ourselves', 'themselves'
    }
    
    for word, freq in top_words:
        word_lower = word.lower()
        # Must be atmospheric OR (long AND not a function word AND proper noun-like)
        if (word_lower in atmospheric_terms or 
            (len(word) >= 6 and 
             word_lower not in avoid_words and
             word[0].isupper())):  # Prefer proper nouns for themes
            thematic_words.append(word.upper())
            if len(thematic_words) >= 3:
                break
    
    return thematic_words

def generate_thematic_ascii_art(themes, width):
    """Generate decorative ASCII art based on book themes with beautiful motifs"""
    import random
    lines = []
    
    if not themes:
        # Beautiful default patterns - rotate through different styles
        pattern_choice = random.choice([1, 2, 3, 4])
        
        if pattern_choice == 1:
            # Elegant vine pattern
            border = "⟨" + "═" * (width-4) + "⟩"
            vine = "❦ " + "◦ ❀ ◦ " * ((width-6)//6) + " ❦"
            lines.append(border.center(width))
            lines.append(vine.center(width))
            lines.append(border.center(width))
        elif pattern_choice == 2:
            # Art deco style
            deco1 = "▼" * (width//2) + "▲" * (width//2)
            deco2 = "◆ ❖ " * (width//4)
            deco3 = "▲" * (width//2) + "▼" * (width//2)
            lines.append(deco1[:width].center(width))
            lines.append(deco2[:width].center(width))
            lines.append(deco3[:width].center(width))
        elif pattern_choice == 3:
            # Classical ornamental
            ornament_line = "❋ ◇ ❋ ◇ ❋ ◇ ❋"
            lines.append(ornament_line.center(width))
            lines.append("⬥" + "─" * (width-2) + "⬥")
            lines.append(ornament_line.center(width))
        else:
            # Flourish pattern
            lines.append("✧･ﾟ: *✧･ﾟ:* *:･ﾟ✧*:･ﾟ✧".center(width))
            lines.append("◈ ◈ ◈ ◈ ◈ ◈ ◈".center(width))
            lines.append("✧･ﾟ: *✧･ﾟ:* *:･ﾟ✧*:･ﾟ✧".center(width))
        
        return lines
    
    # Create beautiful thematic displays
    if len(themes) >= 1:
        # Choose decorative style based on theme content
        style = choose_decorative_style(themes)
        
        if style == "nature":
            lines.append("❀ ❀ ❀ ❀ ❀ ❀ ❀ ❀".center(width))
            theme_line = " 🌿 ".join(themes[:3])
            lines.append(theme_line.center(width))
            lines.append("❀ ❀ ❀ ❀ ❀ ❀ ❀ ❀".center(width))
        elif style == "maritime":
            # Simple, clean maritime pattern with manual centering
            wave_pattern = "⚓ ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ ⚓"
            lines.append(center_text_precisely(wave_pattern, width))
            theme_line = " ⚓ ".join(themes[:3])
            lines.append(center_text_precisely(theme_line, width))
            lines.append(center_text_precisely(wave_pattern, width))
        elif style == "gothic":
            lines.append("⚜ ❦ ⚜ ❦ ⚜ ❦ ⚜".center(width))
            theme_line = " ❦ ".join(themes[:3])
            lines.append(theme_line.center(width))
            lines.append("⚜ ❦ ⚜ ❦ ⚜ ❦ ⚜".center(width))
        elif style == "celestial":
            lines.append("✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧".center(width))
            theme_line = " ✦ ".join(themes[:3])
            lines.append(theme_line.center(width))
            lines.append("✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧".center(width))
        else:
            # Classic elegant
            lines.append("◆ ◇ ❖ ◇ ◆ ◇ ❖ ◇".center(width))
            theme_line = " ◆ ".join(themes[:3])
            lines.append(theme_line.center(width))
            lines.append("◆ ◇ ❖ ◇ ◆ ◇ ❖ ◇".center(width))
    
    # Add decorative frame
    frame_line = "═" * width
    lines.append(frame_line)
    
    # Beautiful ornamental footer
    footer_patterns = [
        "◊ ◈ ◊ ◈ ◊ ◈ ◊",
        "❋ ❀ ❋ ❀ ❋ ❀ ❋", 
        "⟡ ⟢ ⟡ ⟢ ⟡ ⟢ ⟡",
        "✧ ❖ ✧ ❖ ✧ ❖ ✧"
    ]
    footer = random.choice(footer_patterns)
    lines.append(footer.center(width))
    
    return lines

def center_text_precisely(text, total_width):
    """Center text with precise padding calculation to avoid shift issues"""
    text_length = len(text)
    if text_length >= total_width:
        return text[:total_width]
    
    # Calculate padding needed
    padding_needed = total_width - text_length
    left_padding = padding_needed // 2
    right_padding = padding_needed - left_padding
    
    return " " * left_padding + text + " " * right_padding

def choose_decorative_style(themes):
    """Choose decorative style based on thematic content"""
    theme_text = " ".join(themes).lower()
    
    nature_words = ["life", "nature", "forest", "tree", "flower", "garden"]
    maritime_words = ["sea", "ocean", "water", "wave", "storm", "ship"]
    gothic_words = ["death", "dark", "blood", "fear", "horror", "mystery"]
    celestial_words = ["light", "star", "heaven", "dream", "hope", "glory"]
    
    if any(word in theme_text for word in nature_words):
        return "nature"
    elif any(word in theme_text for word in maritime_words):
        return "maritime"
    elif any(word in theme_text for word in gothic_words):
        return "gothic"
    elif any(word in theme_text for word in celestial_words):
        return "celestial"
    else:
        return "classic"

