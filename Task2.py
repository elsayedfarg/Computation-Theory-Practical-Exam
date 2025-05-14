class PDA:
    def __init__(self):
        # Initialize the PDA stack
        self.stack = []
    
    def is_odd_palindrome(self, input_string):
        # To handle palindromes, we need to check if the length is odd
        if len(input_string) % 2 == 0:
            return False
        
        # Step 1: Push the first half of the string onto the stack
        mid = len(input_string) // 2
        for i in range(mid):
            self.stack.append(input_string[i])
        
        # Step 2: Skip the middle character
        middle_char = input_string[mid]
        
        # Step 3: Compare the second half with the stack
        for i in range(mid + 1, len(input_string)):
            if not self.stack:
                return False  # If the stack is empty, the string is not a palindrome
            top = self.stack.pop()
            if input_string[i] != top:
                return False  # Mismatch found, not a palindrome
        
        # Step 4: If we successfully compare all the characters, accept the string
        return True


# Test the PDA with odd-length palindrome strings
pda = PDA()

test_strings = [
    "madam",      # Odd-length palindrome
    "racecar",    # Odd-length palindrome
    "abcba",      # Odd-length palindrome
    "abccba",     # Even-length (not a palindrome)
    "hello",      # Not a palindrome
]

for test in test_strings:
    if pda.is_odd_palindrome(test):
        print(f"'{test}' is an accepted odd-length palindrome.")
    else:
        print(f"'{test}' is NOT an accepted odd-length palindrome.")
