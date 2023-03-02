max_health = int()
damage = int()
health = int()

max_health = 100

while health > 0:
    print("you were attacked")
    damage = int(input("Enter rolled damage  "))
    health = max_health - damage
print("Game Over Try again")
    
