# Sample 2D list 'rank'
rank = [[3, 100], [3 ,90], [4, 105], [6, 80]]

# Custom sorting function based on specified criteria
def custom_sort(item):
    return (item[0], -item[1])

# Sort the 'rank' list using the custom_sort function
rank.sort(key=custom_sort)

print(rank)
