import random
import pyglet

#list of words
def wordlist(x):
    file = open(x,'r')
    wordlist = file.read()
    wordlist = wordlist.split('\n')

    return wordlist

#for saving score
def save(s):
    file = open('Scores.txt', 'a')
    saved = file.write(str(s) + '\n')
    file.close()

    return

#save highscore
def highscore():
    a = wordlist('Scores.txt')
    #print(a)
    a = [int(x) for x in a if x!= '']
    a.sort(reverse = True)
    
    h = a[0]
    
    return h

#print(highscore())
#creating a list for input files
Phi = [x.lower() for x in wordlist('province.txt')]
Ele = [y.lower() for y in wordlist('element.txt')]
Ani = [z.lower() for z in wordlist('animal.txt')]
Cou = [a.lower() for a in wordlist('country.txt')]
Col = [b.lower() for b in wordlist('color.txt')]

#yung cat is dun magrarandomize ng category tapos ung words is list within lists ng mga input file
cat = ['Philippine Provinces', 'Elements', 'Animals in the Philippines', 'Countries', 'Colors']

#function in finding random category
def category():
    cat = ['Philippine Provinces', 'Elements', 'Animals in the Philippines', 'Countries', 'Colors']
    x = random.choice(cat)
    
    return x


#function in finding random letter
def letter(category):
    let = set(['A','B','C','D','E','F','G','H','I','J','L','K','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])
    
    if category == 'Philippine Provinces':
        lett = set(['F','H','J','U','V','W','X','Y'])
        final_list= list(set(let).difference(set(lett)))
        y = random.choice(final_list)
        
    elif category == 'Elements':
        lett = set(['J','Q','W'])
        final_list= list(set(let).difference(set(lett)))
        y = random.choice(final_list)
        
    elif category == 'Animals in the Philippines':
        lett = set(['J','X','Y'])
        final_list= list(set(let).difference(set(lett)))
        y = random.choice(final_list)

    elif category == 'Countries':
        lett = set(['W','X'])
        final_list= list(set(let).difference(set(lett)))
        y = random.choice(final_list)
        
    elif category == 'Colors':
        final_list= list(let)
        y = random.choice(final_list)
     
    return y

#para lang macheck if tama ung ginagawa nung function

#checks if the player's answer is correct
def checker(player_input,category):
    cat = ['Philippine Provinces', 'Elements', 'Animals in the Philippines', 'Countries', 'Colors']
    x = player_input
    x = x.lower()

    if category == cat[0]:
        if x in Phi:
            print('Congrats!')
            return True
    
        else:
            print("Try Again!")
            return False
        
    elif category == cat[1]:
        if x in Ele:
            print('Congrats!')
            return True
    
        else:
            print("Try Again!")
            return False

    elif category == cat[2]:
        if x in Ani:
            print('Congrats!')
            return True
    
        else:
            print("Try Again!")
            return False

    elif category == cat[3]:
        if x in Cou:
            print('Congrats!')
            return True
    
        else:
            print("Try Again!")
            return False
    elif category == cat[4]:
        if x in Col:
            print('Congrats!')
            return True
    
        else:
            print("Try Again!")
            return False


#initial score
score = 0
def scoring(player_input):
    #tinawag ung function na checker ang irereturn na value nung checker ay yung word na tama so kapag mali ang irereturn nya ay empty string which will score 0
    word = player_input
    if word == '':
        score = 0

    #kapag tama, sabi nyo ung length nung word?
    else:
        score = len(word)

    return score