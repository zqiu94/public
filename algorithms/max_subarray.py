# Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest
# sum and return its sum.


def max_subarray(nums):
    if len(nums) == 0:
        return 0
    if len(nums) == 1:
        return nums[0]
    # a special corner case is that all numbers are negative
    all_negative = True
    highest_negative = float('-inf')
    for i in range(len(nums)):
        # at least one number is larger than 0
        if nums[i] > 0:
            all_negative = False
        else:
            # if there is no positive number then just loop throughout the list
            highest_negative = max(highest_negative, nums[i])
    if all_negative:
        return highest_negative
    # save the max value after each conquer
    value_list = []
    p = 0
    r = len(nums) - 1
    divide(nums, p, r, value_list)
    return max(value_list)


def divide(nums, p, r, value_list):
    if p < r:
        q = (p + r) // 2
        divide(nums, p, q, value_list)
        divide(nums, q + 1, r, value_list)
        value = conquer(nums, p, q, r)
        # save the max value after each conquer
        value_list.append(value)


def conquer(nums, p, q, r):
    max_left = 0
    max_right = 0
    temp_left = 0
    temp_right = 0
    # start from the right most of the left list
    for i in range(q, p - 1, -1):
        temp_left += nums[i]
        if temp_left >= max_left:
            max_left = temp_left
    # the left most of the right list
    for i in range(q + 1, r + 1):
        temp_right += nums[i]
        if temp_right >= max_right:
            max_right = temp_right
    return max_left + max_right


nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray(nums))
nums2 = [5, 4, -1, 7, 8]
print(max_subarray(nums2))
