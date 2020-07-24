# Our initial binary represented as a string
bin_string = "001011011101"

# Call int() with a base of 2 to get our decimal representation
dec_rep = int(bin_string, 2)
# Call hex() with our decimal representation to get our hex string
hex_str = hex(dec_rep)
# Print the hex string
# Should be 0x2DD
print(hex_str)

'''

'''
