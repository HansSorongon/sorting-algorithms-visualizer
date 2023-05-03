
def quicksort(arr, start, end):

    if (end <= start):
        return

    pivot = arr[end]
    i = start - 1

    for j in range(start, end):
        if (arr[j] < pivot):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    i += 1
    arr[i], arr[end] = arr[end], arr[i]

    quicksort(arr, start, i - 1)
    quicksort(arr, i + 1, end)

arr = [5, 3, 1, 2, 4]
quicksort(arr, 0, len(arr) - 1)

print(arr)

