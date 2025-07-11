from collections import Counter

data = ['a', 'b', 'c', 'a', 'b', 'a']
count = Counter(data)
print(count)  # Output: Counter({'a': 3, 'b': 2, 'c': 1})