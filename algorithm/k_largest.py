# Given an integer array nums and an integer k, return the kth largest element in the array.

# Note that it is the kth largest element in the sorted order, not the kth distinct element.

def find_kth_largest(nums, k):
    # similar to selection sort
    for i in range(k):
        max_index = i
        for j in range(i + 1, len(nums)):
            if nums[j] > nums[max_index]:
                nums[max_index], nums[j] = nums[j], nums[max_index]
    return nums[k - 1]


nums = [3, 2, 1, 5, 6, 4]
k = 2
print(find_kth_largest(nums, k))

nums = [3, 2, 3, 1, 2, 4, 5, 5, 6]
k = 4
print(find_kth_largest(nums, k))
