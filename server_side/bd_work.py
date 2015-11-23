__author__ = 'Muratov'

io = [917, 521, 756, 395, 0, 0, 0, 0, 0]  # abstract
mem = [129, 541, 870, 1340, 1245, 1294, 1311, 1178, 1252]  # in mb
cpy = [72, 45, 42, 67, 55, 13, 21, 13, 8]  # in percents


def get_stat(from_int, to_int, k, lst=None):
    if not lst:
        lst = []
    slice = lst[from_int:to_int]
    buckets = [0] * k
    counter = 0
    bucket_size = int(len(slice) / k)
    for bucket_num in range(k):
        for i in range(bucket_size):
            if counter < len(slice):
                buckets[bucket_num] += slice[counter] / bucket_size
                counter += 1
            else:
                break
    return [int(x) for x in buckets]


if __name__ == '__main__':
    print(get_stat(0, 9, 1, cpy))
