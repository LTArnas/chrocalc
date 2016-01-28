import random
import math

GREYCODE = {
    "0000" : "0",
    "0001" : "1",
    "0010" : "2",
    "0011" : "3",
    "0100" : "4",
    "0101" : "5",
    "0110" : "6",
    "0111" : "7",
    "1000" : "8",
    "1001" : "9",
    "1010" : "+",
    "1011" : "-",
    "1100" : "*",
    "1101" : "/"
}

def generate_chromosome(length=10):
    """ Returns a new list of random binary strings, 
    from GREYCODE dictionary keys. 
    Length expected to be an integer, not less than 3."""
    if length < 3: raise ValueError("Length cannot be less than 3")
    output = []
    for i in range(length):
        output.append(random.choice(list(GREYCODE.keys())))
    return output
    
def decode(chromosome):
    """ Returns a new list of decoded strings. 
    Chromosome is expected to be a list of binary strings.
    Each string is determined by the key-value association in GREYCODE. """
    output = []
    now_operator = False
    for g in chromosome:
        decoded_gene = GREYCODE[g]
        if now_operator and not decoded_gene.isdigit():
            output.append(decoded_gene)
            now_operator = False
        elif not now_operator and decoded_gene.isdigit():
            output.append(decoded_gene)
            now_operator = True
    if output and not output[len(output)-1].isdigit():
        del output[len(output)-1]
    return output

def fitness(decoded, target):
    """ Returns a simple fitness value, or math.nan for invalid computation.
        The value is an absolute number, so closer to zero is better.
        The value is determined by the formula:
        abs(target - parsed_total_value_from_decoded)
        Decoded is expected to be a decoded list of strings.
        Target is expected to be the target value for the program.
        Parsing the decoded list is performed manually. 
        It follows order of operations (multiplication and division first) and
        reads left to right, as expected.
        math.nan is used for invalid parsing scenarios, 
        such as division by zero. """
    if math.nan in decoded: return math.nan
    result = _evaluate(decoded)
    if result is math.nan: return math.nan
    difference = target - result
    return abs(difference)

def _evaluate(decoded):
    """ Reads a list of decoded strings and returns the computed total. """
    """ Note, we parse the list in [value][operator][value] chunks,
    performing the appropriate computation. For each chunk we compute, 
    we replace the chunk (in-place) with the computed value.
    This is repeated until only the final total is left in the list.
    We read left to right, and use order of operations. """
    output = decoded[:] # so we don't manipulate original
    while "*" in output or "/" in output:
        for i, x in enumerate(output):
            total = None
            if x == "*":
                total = float(output[i-1]) * float(output[i+1])
            if x == "/":
                if float(output[i+1]) == 0: return math.nan
                total = float(output[i-1]) / float(output[i+1])
            if not total == None:
                output[i] = total
                del output[i-1]
                del output[i] # previous del means we don't +1
                break
            else:
                continue
    while "+" in output or "-" in output:
        for i, x in enumerate(output):
            total = None
            if x == "+":
                total = float(output[i-1]) + float(output[i+1])
            if x == "-":
                total = float(output[i-1]) - float(output[i+1])
            if not total == None:
                output[i] = total
                del output[i-1]
                del output[i] # previous del means we don't +1
                break
            else:
                continue
    if len(output) == 1: return float(output[0])
    return output[0]

def roulette(old_pool):
    """ Roulette wheel selection of a chromosome in the old_pool.
    Returns only the chromosome (list of strings).
    Old_pool is expected to be a list of 2-element tuples,
    where each tuple is: (chromosome, fitness_value);
    where chromosome is a list of binary strings, and
    fitness_value is its fitness value. """
    total = sum(f for (c, f) in old_pool)
    selection = random.uniform(0, total)
    spinner = 0
    for c, f in old_pool:
        spinner += f
        if spinner >= selection:
            return c

def cross(c1, c2, rate=0.7):
    """ Based on rate, either returns a new crossover list of binary strings,
    or a copy of c1.
    Rate determines the chance for crossover, 
    where value of 1.0 would produce crossover every time.
    c1 and c2 expected to be lists of binary strings.
    rate is expected to be between 0.0 and 1.0 """
    output = c1[:]
    max_slice_point = len(list(zip(c1,c2)))-1
    if random.random() <= rate:
        slice_point = random.randint(1, max_slice_point)
        output = c1[:slice_point] + c2[slice_point:]
    return output
    
def mutate(c, rate=0.007):
    """ Returns a new list of binary strings; 
    where each element has a chance to be replaced with a new one,
    from GREYCODE keys.
    The chance is determined by rate, where 1.0 would mutate every time. """
    output = c[:] # We return a new chromosome
    for i in range(len(output)):
        if random.random() <= rate:
            output[i] = random.sample(list(GREYCODE.keys()), 1)[0]
    return output

if __name__ == "__main__":
    target = 1111
    chromosome_length = 50
    new_blood_count = 10
    preserve_count = 8
    crossovers_count = 8
    
    print("Target is:", target)
    answer = None
    old_pool = []
    print("Working...")
    while not answer:
        new_pool = []
        # Add new blood
        while len(new_pool) < new_blood_count:
            c = generate_chromosome(chromosome_length)
            dc = decode(c)
            # Operators-only chromosome would decode to an empty list
            if not dc: 
                continue
            f = fitness(dc, target)
            if f is math.nan:
                continue
            new_pool.append((c, f))
        # For the first iteration...
        if not old_pool:
            old_pool = new_pool[:]
        # Add crossover chromosomes
        while len(new_pool) < new_blood_count + crossovers_count:
            c1 = roulette(old_pool)
            c2 = roulette(old_pool)
            crossed = cross(c1, c2)
            decoded_crossed = decode(crossed)
            if not decoded_crossed:
                continue
            f = fitness(decoded_crossed, target)
            if f is math.nan:
                continue
            new_pool.append((crossed, f))
        # Preserve some chromosomes to the next generation, and mutate
        while len(new_pool) < new_blood_count + crossovers_count + preserve_count:
            c = roulette(old_pool)
            m = mutate(c)
            d = decode(m)
            if not d:
                continue
            f = fitness(d, target)
            if f is math.nan:
                continue
            new_pool.append((m, f))
        # Check for an answer
        for c, f in new_pool:
            if f == 0:
                answer = decode(c)
                break
        old_pool = new_pool # Prep for the next iteration
    
    if answer: 
        print()
        print("OMG YAY!", answer)
        print("Target was:", target)