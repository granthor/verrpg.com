handed = ""
s = ""
name = ""
cost = 0
shred = 0
bonus = 0
rangenum = 0
rangestr = ""

rankArray = ["Pathetic", "Lousy", "Unremarkable", "Remarkable", "Impressive", "Fantastic", "Heroic", "Legendary", "Divine", "Mythical", "Draconic"]

# Prompt function to get input
def prompt(question, choices = []):
    print(question)
    if len(choices) == 0:
        return input("> ")
    else:
        output = ""
        s = "("
        for i in range(0, len(choices)):
            s += "\"" + choices[i] + "\""
            if i == len(choices)-1:
                s += ") "
            else:
                s += "/"
        while output not in choices:
                output = input(s)
        return output

def padding(string):
    return len(str(string))

def pad(string, padding, character = " "):
    for i in range(0, padding):
        string += character
    return string

def formatter(name, bonus, shred, rangestr, cost, prevCost = 0):
    output = ""

    # Add upgrade link if there is a previous cost.
    if prevCost != 0:
        output += "Upgrades: [" + name + "](#" + name.lower().replace(" ", "-")
        output += ") (" + str(cost-prevCost) + ")\n\n"

    # Add Weapon title
    output += "## " + name + "\n\n"

    # Calculate table padding
    costPad = padding(cost)
    bonusPad = padding(bonus)
    rangePad = padding(rangestr)
    shredPad = padding(shred)
    leftPadding = max([costPad, bonusPad, rangePad])

    # Add table
    output += "| Cost: " + str(cost)
    output = pad(output, leftPadding-costPad)
    output += "  |        "
    output = pad(output, shredPad)
    output += " |\n"

    output += "|:------"
    output = pad(output, leftPadding, "-")
    output += "--|:-------"
    output = pad(output, shredPad, "-")
    output += "-|\n"

    output += "| Bonus: " + str(bonus)
    output = pad(output, leftPadding-bonusPad)
    output += " | Shred: " + str(shred) + " |\n"

    output += "| Range: " + str(rangestr)
    output = pad(output, leftPadding-rangePad)
    output += " |        "
    output = pad(output, shredPad)
    output += " |\n\n"

    return output




print("Welcome to the weapon template creator\n")

# Name of weapon
name = prompt("Name of the weapon? (e.g. Sword)")

# Handed-ness
handed = prompt("1-Handed or 2-Handed? Write either 1 or 2.", ["1", "2"])

# Cost of the weapon
s = "Around "
if handed == "1":
    s += "4"
elif handed == "2":
    s += "9"
s += " for a " + handed + "-Handed"
cost = int(prompt("Cost of the pathetic weapon in silver rings? (" + s + ")"))

# Bonus the weapon gives
bonus = int(prompt("Bonus for the lousy weapon? (Usually 1-4)"))

# Shred the weapon gives
shred = int(prompt("Shred for the pathetic weapon? (Usually 1-4)"))

# Range of the weapon
rangenum = int(prompt("Range of the weapon as an approximate number of meters? (1-150)"))
if rangenum < 6:
    rangestr = str(rangenum) + "m";
elif rangenum < 16:
    rangestr = "Near";
elif rangenum < 31:
    rangestr = "Far";
elif rangenum < 151:
    rangestr = "Distant";
else:
    print("WARN: Range is further than 150m, labeling as Distant (30m - 150m).");

prevCost = 0
rankBonus = 0
if shred == 0:
    shredGrowth = [0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3]
elif shred == 1:
    shredGrowth = [1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5]
elif shred == 2:
    shredGrowth = [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]
else:
    shredGrowth = [3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10]

f = open("weaponOutput.md", "w")

f.write("# " + name + " - " + handed + "-Handed\n\n")

for i in range(0, len(rankArray)):
    rankName = rankArray[i] + " " + name
    f.write(formatter(rankName, rankBonus, shredGrowth[i], rangestr, cost, prevCost))
    prevCost = cost
    cost = cost * 2 + (2 << i)
    rankBonus += bonus

f.close()
