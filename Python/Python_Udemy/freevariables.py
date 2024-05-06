def concat(caracter):
    final_word = caracter
    def group(value_to_group = ''):
        nonlocal final_word
        final_word += value_to_group
        return final_word
    return group


word = concat('G')

print(word('u'))
print(word('s'))
print(word('t'))