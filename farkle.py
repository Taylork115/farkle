import random


def scoreDice(dice):
    #  this function will take an arbitrary list of Dice values and return a Dictionary of possible scores
    #  dict will take the form of 'scores[points] = [list_of_dice]'
    #  so a roll of [1, 1, 2, 5, 5, 6] will return {100: [1], 200: [1, 1], 50: [5], 100: [5, 5]}

    num_dice = len(dice)
    values = [0, 0, 0, 0, 0, 0]  # number of ones, twos, threes, etc
    scores = {}  # will store list of scores & their associated die
    for d in range(num_dice):
        val = dice[d] - 1  # since val is an index, and indices start at 0
        values[val] += 1
    print(values)
    no_mults = True

    if max(values) >= 3:
        no_mults = False

    if values[0] == 0 and values[4] == 0 and no_mults is True:
        return {0: 0}  # no score if no 1s, 5s, or 3+ multiples

    # look for runs, either 1,2,3,4,5, 2,3,4,5,6, or 1,2,3,4,5,6
    runs_score = 0
    if values[0] > 0 and values[1] > 0 and values[2] > 0 and values[3] > 0 and values[4] > 0:
        scores[750] = [1, 2, 3, 4, 5]
    if values[5] > 0 and values[1] > 0 and values[2] > 0 and values[3] > 0 and values[4] > 0:
        scores[750] = [2, 3, 4, 5, 6]
    if len(scores) == 2:  # IE if both runs are present
        scores[1500] = [1, 2, 3, 4, 5, 6]

    for i in range(6):
        d = i + 1  # the number on the dice
        val = values[i]
        if d == 1:
            if val >= 1:
                scores[100] = [d]
            if val >= 2:
                scores[200] = [d, d]
            if val >= 3:
                scores[1000] = [d, d, d]
            if val >= 4:
                scores[2000] = [d, d, d, d]
            if val >= 5:
                scores[4000] = [d, d, d, d, d]
            if val == 6:
                scores[8000] = [d, d, d, d, d, d]
        elif d == 5:
            if val >= 1:
                scores[50] = [d]
            if val >= 2:
                scores[100] = [d, d]
            if val >= 3:
                scores[d*100] = [d, d, d]
            if val >= 4:
                scores[d*200] = [d, d, d, d]
            if val >= 5:
                scores[d*400] = [d, d, d, d, d]
            if val == 6:
                scores[d*800] = [d, d, d, d, d, d]
        else:
            if val >= 3:
                scores[d*100] = [d, d, d]
            if val >= 4:
                scores[d*200] = [d, d, d, d]
            if val >= 5:
                scores[d*400] = [d, d, d, d, d]
            if val == 6:
                scores[d*800] = [d, d, d, d, d, d]

    return scores


def main():
    print('Farkle!')

    num_dice = int(input('Enter # of dice: '))
    dice = []
    for d in range(num_dice):
        dice.append(0)

    while True:
        input('Press ENTER to roll die')
        for d in range(num_dice):
            dice[d] = random.randrange(1, 7)
        dice.sort()

        print(dice)
        scores = scoreDice(dice)

        print(scores)


if __name__ == '__main__':
    main()