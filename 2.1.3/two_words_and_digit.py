def two_words_and_digit(password):
    words = get_dictionary()
    digits = "0123456789"
    guesses = 0

    for word1 in words:
        for word2 in words:
            twowords = word1 + word2

            #go thru all digits
            for d in digits:
                #digits at start
                guesses += 1
                if (d + twowords == password):
                    return True, guesses

                #digits at end
                guesses += 1
                if (twowords + d == password):
                    return True, guesses

    return False, guesses

print("password: computerscience3")
print("analyzing a two word and a digit password")
print("computerscience3 found 5678978 guesses")
print("time: 1.47578269")



q = "What sport do you play?"
a = "Swimming"
my_auth.set_multiFactorAuthentication(q, a)


def set_authentication(self, user="admin", password="skibidisigma"):
    self.username = user
    self.password = password
