
damage = int()
health = int()


health = int(input("enter health points:  "))
while health > 0:
    print("you have been attacked")
    damage = int(input("Enter damage rolled:  "))
    health = health - damage
    print(health)
print("GAME OVER")
