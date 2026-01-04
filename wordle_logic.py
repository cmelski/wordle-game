def evaluate_guess(secret, guess):
    result = ["⬛"] * 5
    secret_chars = list(secret)

    # Greens
    for i in range(5):
        if guess[i] == secret[i]:
            result[i] = "G"
            secret_chars[i] = None

    # Yellows
    for i in range(5):
        if result[i] == "⬛" and guess[i] in secret_chars:
            result[i] = "Y"
            secret_chars[secret_chars.index(guess[i])] = None

    return result
