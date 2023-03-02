max_health = int()
damage = int()
health = int()

max_health = 100
health = 100
while health > 0:
    print("you have been attacked")
    damage = int(input("Enter damage rolled:  "))
    health = health - damage

print("GAME OVER")
