import itertools

# Load data
workers = []
rooms = []

with open("workers.txt", "r") as f:
    for x in f:
        if x[0] == '#':
            continue
        x = x.split(" ")
        person = {
            "name": x[0],
            0: int(x[1]),
            1: int(x[2]),
            2: int(x[3])
        }
        workers.append(person)

with open("rooms.txt", "r") as f:
    for x in f:
        if x[0] == '#':
            continue
        x = x.split(" ")
        location = {
            "name": x[0],
            0: int(x[1]) - int(x[4]),
            1: int(x[2]) - int(x[5]),
            2: int(x[3]) - int(x[6])
        }
        rooms.append(location)

# Precompute worker capacities
worker_capacities = [{dim: worker[dim] for dim in range(3)} for worker in workers]

# Algorithm
num_needed = len(rooms) * 3
best_score = 0
best_orient = None
best_score_offby = 0

print("Total permutations:", num_needed)

for n, i in enumerate(itertools.permutations(workers, num_needed)):
    score = 0
    score_offby = 0
    
    # Precompute sums of worker capacities for each room dimension
    room_sums = [[0, 0, 0] for _ in range(len(rooms))]
    for r, room in enumerate(rooms):
        start = r * 3
        for j in range(3):
            room_sums[r][j] = sum(i[start + k][j] for k in range(3))
    
    for r, room in enumerate(rooms):
        v1, v2, v3 = room_sums[r]
        for j in range(3):
            if v1 > room[j]:
                score += 1
            else:
                score_offby += room[j] - v1
            if v2 > room[j]:
                score += 1
            else:
                score_offby += room[j] - v2
            if v3 > room[j]:
                score += 1
            else:
                score_offby += room[j] - v3
    
    if score > best_score:
        best_score = score
        best_orient = i
        best_score_offby = score_offby
        if best_score == num_needed * 3:
            break
    elif score == best_score and score_offby < best_score_offby:
        best_score = score
        best_orient = i
        best_score_offby = score_offby
    
    if n % 10000 == 0:
        print("Progress: {}/{}".format(n, num_needed))

print("Best score:", best_score)
print("Best score offby:", best_score_offby)

# Print results
for r, room in enumerate(rooms):
    print("===" + room['name'] + "===")
    start = r * 3
    for k in range(3):
        print(best_orient[start + k]["name"])

input()
