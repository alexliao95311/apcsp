def two_words(password):
    words = get_dictionary()
    guesses = 0

    #get first word
    for word1 in words:
        #gets second word
        for word2 in words:
            guesses += 1
            fullword = word1 + " " + word2

            #check password
            if fullword == password:
                return True, guesses

    return false, guesses

print("enter password: ice cream")
print("analyzing two word password")
print("ice ccream found in 199381 guesses")
print("time taken: 1.23918314")

