array = [12, 11, 13, 5, 6, 7]






def merge_sort(array):
    if len(array) > 1:

        mid = len(array) // 2

        L = array[:mid]
        R = array[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            array[k] = R[j]
            j += 1
            k += 1
        yield i, j, k

it = merge_sort(array)
i, j, k = next(it)
