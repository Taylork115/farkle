import random
import time


def scoreDice(dice):
    #  this function will take an arbitrary list of Dice values and return a Dictionary of possible scores
    #  dict will take the form of 'scores[idx] = [points, [list_of_dice]]'
    #  so a roll of [1, 1, 2, 5, 5, 6] will return {0: [100, [1]], 1: [200, [1, 1]], 2: [50, [5]], 3: [100, [5, 5]]}

    num_dice = len(dice)
    values = [0, 0, 0, 0, 0, 0]  # number of ones, twos, threes, etc
    scores = {}  # will store list of scores & their associated die
    sidx = 0  # index for scores
    for d in range(num_dice):
        val = dice[d] - 1  # since val is an index, and indices start at 0
        values[val] += 1
    # print(values)
    no_mults = True

    if max(values) >= 3:
        no_mults = False

    if values[0] == 0 and values[4] == 0 and no_mults is True:
        return {}  # no score if no 1s, 5s, or 3+ multiples

    # look for runs, either 1,2,3,4,5, 2,3,4,5,6, or 1,2,3,4,5,6
    if values[0] > 0 and values[1] > 0 and values[2] > 0 and values[3] > 0 and values[4] > 0:
        scores[sidx] = [750, [1, 2, 3, 4, 5]]
        sidx += 1
    if values[5] > 0 and values[1] > 0 and values[2] > 0 and values[3] > 0 and values[4] > 0:
        scores[sidx] = [750, [2, 3, 4, 5, 6]]
        sidx += 1
    if len(scores) == 2:  # IE if both runs are present
        scores[sidx] = [1500, [1, 2, 3, 4, 5, 6]]
        sidx += 1

    for i in range(6):
        d = i + 1  # the number on the dice
        val = values[i]
        if d == 1:
            if val >= 1:
                scores[sidx] = [100, [d]]
                sidx += 1
            if val >= 2:
                scores[sidx] = [200, [d, d]]
                sidx += 1
            if val >= 3:
                scores[sidx] = [1000, [d, d, d]]
                sidx += 1
            if val >= 4:
                scores[sidx] = [2000, [d, d, d, d]]
                sidx += 1
            if val >= 5:
                scores[sidx] = [4000, [d, d, d, d, d]]
                sidx += 1
            if val == 6:
                scores[sidx] = [8000, [d, d, d, d, d, d]]
                sidx += 1
        elif d == 5 and val < 3:
            if val >= 1:
                scores[sidx] = [50, [d]]
                sidx += 1
            if val >= 2:
                scores[sidx] = [100, [d, d]]
                sidx += 1
        else:
            if val >= 3:
                scores[sidx] = [d*100, [d, d, d]]
                sidx += 1
            if val >= 4:
                scores[sidx] = [d*200, [d, d, d, d]]
                sidx += 1
            if val >= 5:
                scores[sidx] = [d*400, [d, d, d, d, d]]
                sidx += 1
            if val == 6:
                scores[sidx] = [d*800, [d, d, d, d, d, d]]
                sidx += 1

    return scores


def printScore(scores):
    # function to nicely print the dictionary of scores returned by scoreDice
    s = 'Choice\tScore\tDice Used\n'
    for x in scores:
        points = scores[x][0]
        dice = scores[x][1]
        if points > 999:
            s += f'{x}\t\t{points}\t{dice}\n'
        else:
            s += f'{x}\t\t{points}\t\t{dice}\n'
    print(s)


def playTurn(ptype, sleep_time=3):
    # This function plays one turn of Farkle. It sets up 6 dice, rolls them, and lets the player pick which dice to
    # use for scoring. Then the remaining dice can be rerolled. If there's a bust, the turn ends with 0 points scored.
    # Function returns the points scored for this turn.
    # p_type is a string representing the type of Player.
    # Will support either 'man', 'dumbAss', 'allIn', or 'playItSafe'

    dice = [0 for d in range(6)]  # initialize the dice List
    round_score = 0
    did_bust = False
    first_roll = True

    while True:
        s = ''
        if first_roll:
            if ptype == 'man':
                s = input('Press ENTER to roll die: ')
            first_roll = False
        else:
            if ptype == 'man':
                s = input('Press ENTER to roll die, or \'x\' to end turn: ')
            if ptype == 'dumbAss':
                print(f'{ptype} is ending his turn...')
                s = 'x'  # dumbAss always quits once he has any points
                time.sleep(sleep_time)

        if s == 'x':
            return round_score

        if did_bust:
            return 0
        else:
            if len(dice) == 0:  # covers case where all dice are used for score, and player gets to roll again
                num_dice = 6
            else:
                num_dice = len(dice)  # only roll remaining dice

        dice = [random.randrange(1, 7) for d in range(num_dice)]
        dice.sort()

        turn_is_over = False
        took_points = False

        while not turn_is_over:
            print(f'Dice remaining:\n{dice}')

            scores = scoreDice(dice)

            if len(scores) == 0:
                if took_points is False:
                    print('BUST!')
                    return 0
                else:
                    turn_is_over = True

            else:
                printScore(scores)

                if took_points is False and len(scores) == 1:
                    choice = 0
                    if ptype == 'man':
                        input('Selecting \'0\' since it\'s the only score (ENTER to continue) ')
                    else:
                        print('Selecting \'0\' since it\'s the only score')
                        time.sleep(sleep_time)
                else:
                    if ptype == 'man':
                        choice = input('Select one score to take, or press \'x\' to pass: ')
                    elif ptype == 'dumbAss':
                        if took_points is False:
                            point_vals = [scores[s][0] for s in scores]
                            highest_point_val = max(point_vals)
                            choice = 0
                            for s in scores:
                                if highest_point_val in scores[s]:
                                    choice = s
                            print(f'{ptype} is selecting {choice} for {highest_point_val} points')
                        else:
                            print(f'{ptype} is taking no more points...')
                            choice = 'x'
                        time.sleep(sleep_time)

                if choice == 'x':
                    turn_is_over = True

                else:
                    took_points = True
                    score = scores[int(choice)]  # get the score info from the choice selected
                    # score = [number_of_points, [die_1, die_2, ..., die_N]]
                    points = score[0]  # the number of points
                    die = score[1]  # the dice used to make those points
                    for d in die:
                        dice.remove(d)  # take the scoring dice out of play for now

                    round_score += points
                    print(f'Score = {round_score}')


def main():
    print('Farkle!')

    score_threshold_str = input('Enter score to play to (leave blank for 5000): ')
    if score_threshold_str == '':
        score_threshold = 5000
    else:
        score_threshold = int(score_threshold_str)

    print('COMPUTER PLAYERS ARE')
    print('1. dumbAss (easy)')
    print('2. allIn (med)')
    print('3. playItSafe (???)')

    print('\nEnter COMPUTER player name to play against \'AI\'')
    print('Enter HUMAN name to play against MAN')

    p1name = input('Enter name for PLAYER 1: ')
    p2name = input('Enter name for PLAYER 2: ')

    if p1name == '':
        p1name = 'Player 1'
    if p2name == '':
        p2name = 'dumbAss'

    computer_names = ['dumbAss', 'allIn', 'playItSafe']

    if p1name not in computer_names:
        p1type = 'man'
    else:
        p1type = p1name

    if p2name not in computer_names:
        p2type = 'man'
    else:
        p2type = p2name

    if not p1type == 'man' and not p2type == 'man':
        turn_delay = 0  # computers play FAST against each other
    else:
        turn_delay = 3

    player_1_score = 0
    player_2_score = 0

    player_1s_turn = bool(random.getrandbits(1))

    while True:
        if player_1s_turn:
            print(f'{p1name}\'s Turn')
            player_1_score += playTurn(p1type, turn_delay)
            print(f'{p1name} SCORE = {player_1_score}')
            print(f'{p2name} SCORE = {player_2_score}')
            if player_1_score >= score_threshold:
                print(f'{p1name} WINS')
                return
        else:
            print(f'{p2name}\'s Turn')
            player_2_score += playTurn(p2type, turn_delay)
            print(f'{p2name} SCORE = {player_2_score}')
            print(f'{p1name} SCORE = {player_1_score}')
            if player_2_score >= score_threshold:
                print(f'{p2name} WINS')
                return

        player_1s_turn = not player_1s_turn


if __name__ == '__main__':
    main()