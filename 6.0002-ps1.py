###########################
# 6.0002
# Problem Set 1
# Name: James Quigley
# Collaborators: none
# Time: 5 hours
#


from ps1_partition import get_partitions
import time
import copy

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file. Assumes the file contents contain data
    in the form of comma-separated values with the weight and cow name per line.

    Parameters:
    filename _ the name of the data file as a string

    Returns:
    a dictionary containing cow names (string) as keys, and the corresponding
    weight (int) as the value, e.g. {'Matt': 3, 'Kaitlin': 3, 'Katy': 5}
    """
    #opens the file
    with open(filename) as file:
        #use read and split at the line breaks 
        read_data = file.read().split("\n")
        #initialize dictionary for the cow weights
        cow_weight_dict = {}
        for data in read_data:
            #read each line and split by commans, so I can create my weight and cow dict
            weight,cow = data.split(",")
            weight = int(weight)
            cow_weight_dict[cow] = weight
    file.close()
    return cow_weight_dict
    
# Problem 2
def greedy_cow_trips(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows _ a dictionary of names (string), weights (int)
    limit _ weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # cows.get applied to every key in cows
    cows_copy = sorted(cows, key=cows.get, reverse=True) 
    result = []
    while len(cows_copy) > 0:
        totalWeight = 0
        take = []
        for name in cows_copy[:]:
            #checks if a cow is under my limit, and if he is then we "take" him
            if cows[name] + totalWeight <= limit:
                take.append(name)
                totalWeight = totalWeight + cows[name]
                cows_copy.remove(name)
        result.append(take)
    return result

# Problem 3
def brute_force_cow_trips(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips.
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation.

    Does not mutate the given dictionary of cows.

    Parameters:
    cows _ a dictionary of names (string), and weights (int)
    limit _ weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
     # generating a list contains all possible partitions of cows
    possible_partitions = list(get_partitions(cows.keys()))
    # sorting list by the length of all partitions
    possible_partitions.sort(key=len)
    # initializing the desired list of lists that has the fewest trips
    result_partition = possible_partitions[0]
    # iterating through each possible partition
    for partition in possible_partitions:
        # initializing the empty list which will contain the weight of each trip in a partition and satisfy the required limits
        # e.g. partition = [[1,2,3,4],[5]] <=> trip_weights = [10, 5] with default limit => this is result partition
        trip_weights = []
        for trips in partition:
            weight = 0
            for trip in trips:
                weight += cows[trip]
            if weight > limit:
                break
            else:
                trip_weights.append(weight)
        # immediately returns the first desired partition in the possible partitions list
        if len(trip_weights) != 0 and len(trip_weights) == len(partition):
            result_partition = partition
            break
    return result_partition

# Problem 4
def compare_cow_trips_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_trips and brute_force_cow_trips functions here. Use the
    default weight limits of 10 for both greedy_cow_trips and
    brute_force_cow_trips.

    Print out the number of trips returned by each method and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # starting time for measuring greedy_cow_transport function
    startGreedy = time.time()
    greedy_cow_trips(load_cows("ps1_cow_data.txt"))
    # end point of measuring greedy_cow_transport function
    endGreedy = time.time()
    # output the time that needs to run greedy_cow_transport and its partition
    print("Greedy algorithm measured: ", endGreedy - startGreedy)
    print(greedy_cow_trips(load_cows("ps1_cow_data.txt")))
    
    # starting time for measuring brute_force_cow_transport function
    startBruteForce = time.time()
    brute_force_cow_trips(load_cows("ps1_cow_data.txt"))
    # end point of measuring brute_force_cow_transport function
    endBruteForce = time.time()
    # output the time that needs to run brute_force_cow_transport and its partition
    print("Brute force algorithm measured: ", endBruteForce - startBruteForce)
    print(brute_force_cow_trips(load_cows("ps1_cow_data.txt")))
compare_cow_trips_algorithms()

# Problem 5
def dp_max_cows_on_trip(cow_weights, target_weight, memo = {}):
    """
    Find largest number of cows that can be brought back. Assumes there is
    an infinite supply of cows of each weight in cow_weights.

    Parameters:
    cow_weights   _ tuple of ints, available cow weights sorted from smallest to
                    largest value (d1 < d2 < ... < dk)
    target_weight _ int, amount of weight the spaceship can carry
    memo          _ dictionary, OPTIONAL parameter for memoization (you may not
                    need to use this parameter depending on your implementation,
                    don't delete though!)

    Returns:
    int, largest number of cows that can be brought back whose weight
    equals target_weight
    None, if no combinations of weights equal target_weight
    """
    if target_weight == 0: # Trivial basecase
        return 0
 
    elif target_weight % cow_weights[0] == 0: # 2nd base case where the lowest cow weight is a factor of target weight
        return target_weight / cow_weights[0] #how many cows we can add
 
    sub_list = [] #list of subproblems
    ans = [] #list of answers
    memo_count = 0

 
    #if the target weight and cow weight difference is >0 then we add to sublist
    for w in cow_weights[1:]:
        if target_weight - w > 0:
            sub_list.append(target_weight - w)
    #if we couldnt find a cow lighter than the capacity it returns none        
    if len(sub_list) == 0:
        return None
    #now we scan our sublist
    for sub in sub_list:
        #use memoization so we dont have to check the whole sublist again each time
        if sub not in memo:
            answer = dp_max_cows_on_trip(cow_weights, sub, memo)
            memo[sub] = answer
            if answer != None:
                ans.append(answer + 1)
                for i in memo:
                    memo_count += memo_count**2
        else:
            answer = memo[sub]
            if answer != None:
                ans.append(answer + 1)
    #if no combination could equal our goal then return none            
    if len(ans) == 0:
        return None
    #otherwise returns the maximum answer from ans
    else:
        return int(max(ans))


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':

# Problem 1
    #cow_weights = load_cows('ps1_cow_data.txt')
    #print(cow_weights)
# Problem 2
    # print(greedy_cow_trips(cow_weights))
# Problem 3
    # print(brute_force_cow_trips(cow_weights))
# Problem 4
    # compare_cow_trips_algorithms()
# Problem 5
     cow_weights = (3, 5, 8, 9)
     n = 64
     print("Cow weights = (3, 5, 8, 9)")
     print("n = 64")
     print("Expected ouput: 20 (3 * 18 + 2 * 5 = 64)")
     print("Actual output:", dp_max_cows_on_trip(cow_weights, n))
     print()
    
