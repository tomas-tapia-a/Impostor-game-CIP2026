import random
from ai import call_gpt

def main():
    while True:
        print("")
        print("================================================================")
        print("                 WELCOME TO THE IMPOSTOR GAME                   ")
        print("================================================================")
        print("Select an option:\n1. Play \n2. Exit")
        option = input()
        if option == "1":
            game_data = players()
            gtopic = topic()  
            survivor_word = search(game_data, gtopic)         
            
            run(game_data, survivor_word)
        else:
            print("Thanks for playing! \nSee you later.")
            break

def run(game_data, survivor_word):
    clues1={}
    clues2={}
    while True:
        for i in range(2):
            
            print(f"\n\n\n|----------ROUND {i+1}----------|")
            
            for player in game_data.keys():
                print("\nPlease don't repeat the clue.")
                clue = input(f"{player}, write a clue: ")
                if i == 0:
                    clues1[player] = clue
                    print("\nClues for Round 1:", clues1)
                else:
                    clues2[player] = clue
                    print("\nClues for Round 2:", clues2)
                
        deleted = []
        print("\n\n\n---------------------------------------------------------------")
        print("It's time to vote for someone. Avoid ties!!")
        print("---------------------------------------------------------------")
        for voter in game_data.keys():
            vote = input(f"\n{voter}, who do you think is the impostor? ")
            if vote in game_data:
                deleted.append(vote)
            else:
                print("That player does not exist. Try again.")

        votecounter = {}
        for name in deleted:
            if name in votecounter:
                votecounter[name] +=1
            else:
                votecounter[name] = 1 
        max_votes = 0
        eliminated_player = ""
        
        for name, count in votecounter.items():
            if count > max_votes:
                max_votes = count
                eliminated_player = name
            elif count == max_votes:
                print("Try again")
                continue
                
        print(f"\n{eliminated_player} has been eliminated with {max_votes} votes.")

        updaterole = game_data[eliminated_player]

        if updaterole == "Impostor":
            
            print(f"\nYEAHH!!, {eliminated_player} was the impostor!")
            print(f"But if the impostor guesses the word or gets too close, the impostor wins.")
            trytopic = input(f"\n\n{eliminated_player}, what do you think the word is? ")
            
            ai_prompt = f"We are playing a game. The true word was '{survivor_word}'. The impostor guessed '{trytopic}'. If the guess is correct or extremely close, reply ONLY with the word 'YES'. If it is completely wrong, reply ONLY with the word 'NO'."
            responsetopic = call_gpt(ai_prompt)
            
            if "yes" == responsetopic.lower():
                print("\nTHE IMPOSTOR WINS!\n\n\n\n\n")
                break
            else:
                print("\nThey couldn't survive. The guess was wrong.")
                print("\nThe survivors win this game!\n\n\n")
                break
        else:
            print("")
            print(f"\nOh no! You have eliminated someone who was not the impostor.")
            del game_data[eliminated_player]
            
            if len(game_data) <= 2:
                print("\nOnly two players remain! The Impostor has overpowered the Survivor. THE IMPOSTOR WINS!\n\n\n")
                break
            else:
                print(f"\nThere are still {len(game_data)} players left in the game.")
                input("\n\nPress Enter to start the next round...")

def topic():
    print("\n\n\n|----CHOOSE THE TOPIC----|\nExamples:\nSoccer Players\nBasketball players\nVideogames\n...or whatever topic you want!\n")
    question = input("Select the topic: ")
    return question.lower()

def players():
    n = int(input("How many players want to play? (Minimum 3): "))
    usernames = []
    for i in range(n):
        name = input(f"Write your username Player {i+1}: ")
        usernames.append(name)

    impostor = random.choice(usernames)
    p = {}
    for name in usernames:
        if name == impostor:
            p[name] = "Impostor" 
        else:
            p[name] = "Survivor"
    
    return p

def search(p, gtopic):
    response = call_gpt(f"We are playing an impostor deduction game. The category is {gtopic.lower()}. Provide two closely related words or names in this exact format: \nSurvivor: [word] \nImpostor: [closely related word]")
    words = {}
    for line in response.strip().split("\n"):
        if "Survivor:" in line:
            words["Survivor"] = line.split(":")[1].strip()
        elif "Impostor:" in line:
            words["Impostor"] = line.split(":")[1].strip()
            
    print("\n|----------Check your role---------|\n")
    
    for player_name in p.keys():
        print(f"\nIt is time for {player_name} to check their role.")
        while True:
            inp = input("Write your username to confirm: ")
            if inp == player_name:
                role = p[inp] 
                assigned_word = words[role]
                print(f"\nYour role is: {role} ")
                print(f"Your secret word is: {assigned_word}")
                
                input("\nPress Enter to hide your role and continue...")
                for i in range(50):
                    print("")
                break 
            else:
                print("Username not found or it's not your turn.")

    print("Everyone has seen their roles. Let the game begin!")
    return words["Survivor"]

if __name__ == "__main__":
    main()
