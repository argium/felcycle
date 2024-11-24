import sys
import copy

# print("x=20-(i % 20), the natural result")
# print("y=abs(x-sum) % 20, the new result not taking into account presses")
# print("z=20-<interupt>, how many numbers counted down")
# print("sum is the total numbers counted down")
# print("x' is the final final number, after all the interrupt(s)")
# print()



def decode(ciphertext, interupts):
    if len(ciphertext) != len(interupts)+1:
        raise ValueError("Number of interupts must be one less than the length of the ciphertext")

    # Sum keeps track of how many rotations (aka. numbers that have been counted down) have been made. Effectively tracks the 
    # *actual* position of the rotor which is modified when it's interrupted
    sum = 0

    # Each character of the ciphertext is shifted by a certain amount (using its ordinal value) to get the plaintext
    shifts = []
    for i in range(1,len(interupts)+2):
        # print("i=" + str(i), end="\t")

        # First determine how far the rotor wants to move. It was observed that this is 20 less the number of times the button has been pushed.
        # It it's pressed more than 20 times, it is the modulo of the number.
        x = 20 - (i % 20)
        # print("x=" + str(x), end="\t")

        y = abs(x - sum) % 20
        # print("y=" + str(y), end="\t")

        if i <= len(interupts):
            interrupt = interupts[i-1]
            if interrupt < 20-y:
                raise ValueError("Interrupt value (" + str(interrupt) + ") is less than the number it would have stopped at (" + str(20-y) + ")")
            x2 = 20-interrupt
            shifts.append(interrupt)

            # print("z=" + str(x2), end="\t")
            sum += x2
            # print("sum=" + str(sum), end="\t")
            # print("x'="+str(x2), end="\t")
        else:
            x2 = 20-abs(x-sum)%20
            # print("x'="+str(x2), end="\t")
            shifts.append(x2)
        # print()
        
    # Print how much each character must be shifted
    # print("Shifts:", end=" ")
    # for s in shifts:
    #     print(s, end=" ")
    # print()

    def new_pos(c, shift):
        d = ord(c)+shift
        # If the new position overflows past 'Z', wrap around to 'A'
        if d > ord('Z'):
            return chr(d-26)
        return chr(d)

    # Apply the shifts to the input string
    plaintext = [new_pos(c, shifts[i]) for i,c in enumerate(ciphertext)]
    plaintext = "".join(plaintext)
    print("Output:"+plaintext)
    return plaintext


# read interrupts from args
ciphertext = sys.argv[1]
print("ciphertext=" + ciphertext)
# interupts = []
# for i in range(2, len(sys.argv)):
#     interupts.append(int(sys.argv[i]))

def bruteforce(ciphertext, interupts, pos, plaintexts):
    # print("pos=" + str(pos), end="\t")
    # base case
    if pos == len(ciphertext)-1:
        try:
            plaintext = decode(ciphertext, interupts)
            plaintexts.append(plaintext)
        except ValueError as e:
            print(" ".join([str(c) for c in interupts]) + " is not valid.")
            
        # print(" ".join([str(c) for c in interupts]))
    else:
        for i in range(1, 21):
            # SORRY for this. It's LATE and I am le tired.
            next = copy.deepcopy(interupts)
            next.append(i)
            # print(" ".join([str(c) for c in interupts]))

            bruteforce(ciphertext, next, pos+1, plaintexts)

plaintexts = []
bruteforce(ciphertext, [], 0, plaintexts)

# write to file
with open("plaintexts.txt", "w") as f:
    for p in plaintexts:
        f.write(p + "\n")
# decode(ciphertext, interupts)

# SGHO EIUII ABD MOO NK GHN, EDNY, DL LLSE
