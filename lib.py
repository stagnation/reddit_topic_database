#!/bin/python3
import math
import sys


def sort_insert(inlist, inelem, sort=None):
    # TODO : binatu search
    insertflag = False
    li = inlist

    if sort:
        for idx, e in enumerate(li):
            if sort(inelem) >= sort(e):
                li.insert(idx, inelem)
                insertflag = True
                break

    # catches input that had he least sort value
    # acts as default for when no sort is given
    if not insertflag:
        li.append(inelem)

    return li


def bin_sort_rec(inlist, inelem, start, end, sort):
    start_e = inlist[start]
    end_e = inlist[end]

    if end <= start + 1:
        if sort(inelem) > sort(start_e):
            inlist.insert(start, inelem)
        elif sort(inelem) > sort(end_e):
            inlist.insert(end, inelem)
        else:
            inlist.insert(end+1, inelem)

        return inlist

    inter = end - start
    mid = end - inter / 2
    mid = math.floor(mid)
    pivote = inlist[mid]

    try:
        if sort(inelem) == sort(pivote):
            inlist.insert(mid, inelem)
            return inlist

        elif sort(inelem) > sort(pivote):
            return bin_sort_rec(inlist, inelem, start, mid, sort)
        elif sort(inelem) < sort(pivote):
            return bin_sort_rec(inlist, inelem, mid, end, sort)
    # except Exception as e:
    except IOError as e:
        print("\ncould not sort")
        print(inelem)
        print(e)
        inlist.append(inelem)
        return inlist


def bin_sort_ins(inlist, inelem, sort=None):
    if not inlist:
        return [inelem]

    if not sort:
        return inlist.append(inelem)

    if sort:
        start = 0
        end = len(inlist) - 1
        return bin_sort_rec(inlist, inelem, start, end, sort)


def quicksort(inlist, func):
    print(inlist)

    if not inlist:
        return None
    if len(inlist) <= 1:
        return inlist

    pivot = inlist[0]
    large = []
    small = []
    for x in inlist[1:]:
        if x > pivot:
            large.append(x)
        else:
            small.append(x)

    r_small = quicksort(small, func)
    r_large = quicksort(large, func)

    print("sm", r_small)
    print("lg", r_large)

    if r_small:
        if r_large:
            ret = r_small + [pivot] + r_large
        else:
            ret = r_small + [pivot]
    else:
        if r_large:
            ret = [pivot] + r_large
        else:
            ret = [pivot]

    print("ret", ret)
    return ret


def test_sort(e):
    li = [1, 2, 3, 4, 5, 6, 7, 8]
    li.reverse()
    s = None
    s = lambda x:  x
    ll = bin_sort_ins(li, e, s)
    return ll


def test_quick():
    li = [1,8,3,4,2,5,9,0]
    func = lambda x: x
    ll = quicksort(li, func)
    print(li)
    print(ll)

if __name__ == '__main__':
    test_quick()

    # for x in range(10):
    #     try:
    #         test_sort(x)
    #     except:
    #         pass
