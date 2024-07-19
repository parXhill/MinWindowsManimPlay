class Solution:
   def minWindow(self, s: str, t: str) -> str:

#PRE-STEPS
# 1. Check for empty strings. 

       if not s or not t:
           return ""

# 2. Create a hashmap of the t-values

       t_counts = {}
       for char in t:
           if char in t_counts:
               t_counts[char] += 1
           else:
               t_counts[char] = 1

# 3. Set the checking conditions for the sliding window (## Explain what these are)

       required_t_count = len(t_counts)
       left, right = 0, 0
       t_in_window_count = 0
       window_counts = {}
       min_len = float('inf')
       min_window = (0, 0)


# 4. Start the sliding window loop.

#EXPANDING

 # a. Start the window by selecting the first character.
       while right < len(s):
           char = s[right]


 # b. Add the current character to the window_counts hashmap
           window_counts[char] = window_counts.get(char, 0) + 1


 # c. Check whether the current character has the same number of counts in window_counts and char_count_t. 
 
 # d. If it does, add one to the t_in_window_count
           if char in t_counts and window_counts[char] == t_counts[char]:
               t_in_window_count += 1

#CHECKING

# Check whether the current window is complete.
           while left <= right and t_in_window_count == required_t_count:

    #CONTRACTING

	# Once the current window is complete, the window will begin to contract from the left, 
    # removing character by character until it is no longer complete.
    
    # a. It selects the leftmost character.

               char = s[left]
               


	# b. Check if the current window is smaller than the previously recorded minimum.


               if right - left + 1 < min_len:


	# c. If so, set the new minimum to that size.
                   min_len = right - left + 1
	# d. And record the index coordinates of that window.
                   min_window = (left, right)


	# e. Subtracts the left character from the window counts.
               window_counts[char] -= 1


	# f. Checks if dropping this character would result in the counts no longer being complete. 
               if char in t_counts and window_counts[char] < t_counts[char]:
              # 6. if so it reduces the t_in_window_count, so the window is no longer in completion and the contraction loop will end.
                    t_in_window_count -= 1

		
		# g. and removes the leftmost character from the window by shifting along one

               left += 1

	    
        # If it is still incomplete, return to EXPANDING
           right += 1

# 5. Once the left has met the right at the end of the string, the loop ends. 

# 6. The left and right indexes are set to the minimum window found.

       left, right = min_window

    # 7. Provided that at least one complete window was found, the string is returned. 

       return s[left:right + 1] if min_len != float('inf') else ""
   

sol = Solution()
s = "ADCBECCDEBACCA"
t = "ADCBECCDEBACCA"
