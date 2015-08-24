#!/bin/python3
import math


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

    if sort(inelem) == sort(pivote):
        inlist.insert(mid, inelem)
        return inlist

    elif sort(inelem) > sort(pivote):
        return bin_sort_rec(inlist, inelem, start, mid, sort)
    elif sort(inelem) < sort(pivote):
        return bin_sort_rec(inlist, inelem, mid, end, sort)


def bin_sort_ins(inlist, inelem, sort=None):
    if not inlist:
        return [inelem]

    if not sort:
        return inlist.append(inelem)

    if sort:
        start = 0
        end = len(inlist) - 1
        return bin_sort_rec(inlist, inelem, start, end, sort)



def test_sort(e):
    li = [1, 2, 3, 4, 5, 6, 7, 8]
    li.reverse()
    s = None
    s = lambda x:  x
    ll = bin_sort_ins(li, e, s)
    return ll


if __name__ == '__main__':
    for x in range(10):
        try:
            test_sort(x)
        except:
            pass
