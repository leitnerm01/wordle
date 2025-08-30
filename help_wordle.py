def color_word(word, guess):
    word_nums = {letter: word.count(letter) for letter in word}

    word = word.lower()
    guess = guess.lower()

    colors = [0]*len(word)

    if word != guess:
        #Color all greens first
        for letterNum in range(len(guess)):
            if word[letterNum] == guess[letterNum]:
                colors[letterNum] = 2
        #Then color yellows
        for letterNum in range(len(guess)):
            if word[letterNum] != guess[letterNum]:
                if guess[letterNum] in word:
                    #Don't color the guess letter if that letter appears more in the guess than in the potential answer
                    if word_nums[guess[letterNum]] > len([number for number in [colors[num] for num in range(len(colors)) if guess[num] == guess[letterNum]] if number in [1,2]]):
                        colors[letterNum] = 1
    else:
        colors = [2]*len(guess)
    return colors

def sort_words(words):
    word_dict = {}
    for guess in words:
        poss_length = 0
        poss_number = 0
        for n in range(3**5):
            colors = []
            for _ in range(5):
                colors.append(n % 3)
                n //= 3
            colors.reverse()

            poss = []
            for word in words:
                word_colors = color_word(word.lower(), guess.lower())
                if word_colors == colors:
                    poss.append(word)
            poss_length += len(poss)
            if len(poss):
                poss_number += 1
        word_dict[guess] = poss_length/poss_number

    word_dict_sorted = {k: v for k, v in sorted(word_dict.items(), key=lambda item: item[1])}
    word_list = word_dict_sorted.keys()
    
    return word_list

def play_game(words):
    word_list = words
    guess_num = 0
    colors = [0,0,0,0,0]
    while colors != [2,2,2,2,2]:
        guess = input('What word did you guess: ')
        color_in = input('What colors: ')
        colors = [int(num) for num in color_in]
        poss = []
        for word in word_list:
            word_colors = color_word(word.lower(), guess.lower())
            if word_colors == colors:
                poss.append(word)
        for i in range(len(poss)):
            print(poss[i])
        word_list = poss
        guess_num += 1
    print(f'You guessed the word in {guess_num}!')

def sort_words(words):
    for n in range(3**5):
        combo = []
        x = n
        for _ in range(5):
            combo.append(x % 3)
            x //= 3
        combo.reverse()
    return words

def open_words(file_path):
    with open(file_path, 'r') as file:
        words = [word.rstrip() for word in file]
    return words

# play_game(open_words('words.txt'))
