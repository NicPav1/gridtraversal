import sys
import string

'''This method opens up a .txt file and parses through the file, adding each 
word to a list ignoring punctuation and upper case.'''
def list_shakespeare()->list:
    all_words = []
    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print('Unable to open file: {}'.format(sys.argv[1]))
        exit()
    
    # Gets rid of all special characters that could appear in the word file
    for line in f:
        for word in line.strip().split():
            low = word.replace("^", '')
            word = low.replace("/", '')
            low = word.replace("!", '')
            word = low.replace(".", '')
            low = word.replace(",", '')
            word = low.replace("?", '')
            low = word.replace("-", '')
            word = low.replace(":", '')
            low = word.replace(";", '')
            word = low.replace("]", '')
            low = word.replace("[", '')
            word = low.replace(")", '')
            low = word.replace("(", '')
            word = low.replace("{", '')
            low = word.replace("}", '')
            word = low.replace("&", '')
            low = word.replace("*", '')
            word = low.replace("%", '')
            low = word.replace("@", '')
            word = low.replace("#", '')
            low = word.replace("$", '')
            word = low.replace("_", '')
            low = word.replace("=", '')
            word = low.replace("+", '')
            low = word.replace("|", '')
            word = low.replace('"', '')
            low = word.lower()
            if low:
                all_words.append(low)

    words = set(all_words)
    return words

'''This method returns a list of all possible moves that can be made from the 
current board position, according to the movement rules of a chess knight.'''
def possible_moves(row:int, col:int)->list:
    poss = []
    if ((row - 1 >= 0) and (col + 2 < 8)):
        poss.append([row-1, col+2])
    if ((row - 1 >= 0) and (col - 2 >= 0)):
        poss.append([row-1, col-2])
    if ((row - 2 >= 0) and (col + 1 < 8)):
        poss.append([row-2, col+1])
    if ((row - 2 >= 0) and (col - 1 >= 0)):
        poss.append([row-2, col-1])
    if ((row + 1 < 8) and (col + 2 < 8)):
        poss.append([row+1, col+2])
    if ((row + 1 < 8) and (col - 2 >= 0)):
        poss.append([row+1, col-2])
    if ((row + 2 < 8) and (col + 1 < 8)):
        poss.append([row+2, col+1])
    if ((row + 2 < 8) and (col - 1 >= 0)):
        poss.append([row+2, col-1])
    
    return poss

'''This method takes in the list of words from the word list text file, 
the current index we're evaluating, and the current letter of the matrix 
that we're on. With those inputs, this method compares the current letter 
to the letter at the given index for every word in the list of words, appending
each word that satisfies those requirements to a set and returns that set.'''
def match_index(words:list, index:int, letter:chr)->set:
    valid = []
    for word in words:
        if len(word) > index:
            if word[index] == letter:
                valid.append(word)
    valid_set = set(valid)
    return valid_set

'''This method, given the current position in the grid and the current string 
built by moving around the grid, finds all other words that can be built from 
the current position and current string. It then returns a list of all possible
words from the starting grid index.'''
def match_words(curr_word:str, index:int, words:list, row:int, col:int, grid)->list:
    answers = []
    
    here = grid[row][col]
    words = match_index(words, index, here)

    if len(words) == 0: return answers
    curr_word += grid[row][col]
    if curr_word in words:
        answers.append(curr_word)
    
    moves = possible_moves(row, col)
    for row, col in moves:
        answers += match_words(curr_word, index+1, words, row, col, grid)

    return answers

def main():
    # Input handling: checks for args
    if len(sys.argv) != 3:
        print('Usage: ExtraHopPythonChallenge.py <word list filename> <grid filename>')
        exit()
    
    # Error handling for opening grid file
    try:
        f = open(sys.argv[2], 'r')
    except IOError:
        print('Unable to open file: {}'.format(sys.argv[2]))
        exit()

    # Setup grid
    grid = []
    for g in range(8):
        grid.append(f.readline().rstrip('\n').lower().split(' '))
    try:
        f.close()
    except IOError:
        print('Unable to close file: {}'.format(sys.argv[2]))

    shakespeare = list_shakespeare()  # Create the word list

    # List containing the longest word possible at each position in the grid
    longest_each_position = []
    # List of lists containing each word possible at each position in the grid
    total_each_position = []
    
    # Iterates through each position in the grid and adds the list of possible 
    # words at each position to total_each_position
    for r in range(8):
        for c in range(8):
            total_each_position.append(match_words('', 0, shakespeare, r, c, grid))

    # Checks if no words can be created in the entire grid
    if len(total_each_position) == 0:
        print("No possible words. Try again with different word list.")
        exit()
    else:
        for t in total_each_position:
            if(len(t) == 0):  # No words were found at that position
                continue
            longest = 0
            for j,a in enumerate(t): # Finds the longest word for each position
                if len(a) > len(t[longest]):
                    longest = j
            longest_each_position.append(t[longest])
        # Go through the longest words from each position and find
        # the longest word out of all positions
        longest = 0
        for k, l in enumerate(longest_each_position):
            if len(l) > len(longest_each_position[longest]):
                longest = k
        print("Longest word found with given grid and word list was: {}".format(longest_each_position[longest]))
            

if __name__ == "__main__":
    main()