import argparse
import itertools
import math
import sys


OPERATORS = ['+', '-', '*', '/']
# POSITION = [0, 2, 4, 6, 8, 10, 12, 14]
POSITION_S = [0, 1, 2, 3, 4, 5, 6, 7]  # 全部可出现的位置idx/2
PLACE_HOLDER = ['a', 'b', 'c', 'd']


def gen_formula():
    base = base_formula()
    bracket_pos = get_brackets()
    formulas = []
    bs = max_brackets(bracket_pos, 7)
    for f in base:
        # 基础公式
        formulas.append(f)
        for b in bs:
            for c in b:
                # 加括号的公式
                formulas.append(concat_formula(f, c))
    return formulas


def concat_formula(f, pos):
    # 拼接公式，因为计算时用的是除以2之后的下标，所以恢复使用的时候要*2
    return f[:pos[0]*2] + '(' + f[pos[0]*2+1:pos[1]*2] + ')' + f[pos[1]*2+1:]


def base_formula():
    formulas = []
    holder = itertools.permutations(PLACE_HOLDER, 4)
    for h in holder:
        formula = ' ' + h[0] + ' %s ' + h[1] + ' %s ' + h[2] + ' %s ' + h[3] + ' '
        perm = itertools.permutations(range(4), 3)
        for p in perm:
            formulas.append(formula % (OPERATORS[p[0]], OPERATORS[p[1]], OPERATORS[p[2]]))
    return formulas


def get_brackets():
    # 括号可以放置的位置，成对出现，所以是tuple形式
    pos = []
    comb = itertools.combinations(POSITION_S, 2)
    for c in comb:
        if is_left_pos(c[0]) and is_right_pos(c[1]) and is_valid_pos(c[0], c[1]):
            # 成对出现，收录可能的放置位置
            pos.append(c)
    return pos


def max_brackets(brackets, size):
    """检查最多的括号对数，size是一对括号可以包含的最大字符个数"""
    result = []

    def check(ls):
        comb = itertools.combinations(brackets, ls)
        max_left = 0
        max_right = 0
        min_left = sys.maxsize
        min_right = sys.maxsize
        for t in comb:
            for c in t:
                max_left = c[0] if c[0] > max_left else max_left
                min_left = c[0] if c[0] < min_left else min_left
                max_right = c[1] if c[1] > max_right else max_right
                min_right = c[1] if c[1] < min_right else min_right
            # 计算最右侧(和最左侧)之间的数字个数是否过小，以后最左侧(和最右侧)之间的数字格式是否过大
            if min_right - max_left > 1 and max_right - min_left < size and len(t) > 0:
                result.append(t)
            max_left = 0
            max_right = 0
            min_left = sys.maxsize
            min_right = sys.maxsize

    for i in reversed(range(len(brackets) + 1)):
        check(i)
    return result


def is_left_pos(pos):
    """左括号出现位置"""
    return pos % 2 == 0


def is_right_pos(pos):
    """右括号出现位置"""
    return pos % 2 == 1


def is_valid_pos(l, r):
    """括号跨度，数字个数区间[2, 3]"""
    return 1 < (r - l + 1) / 2 < 4


def test(tp):
    a = tp[0]
    b = tp[1]
    c = tp[2]
    d = tp[3]
    formulas = gen_formula()
    resolved = False
    for f in set(formulas): # 去重
        try:
            r = eval(f)
            if r == 24:
                resolved = True
                new_f = f.replace('a', str(a)).replace('b', str(b)).replace('c', str(c)).replace('d', str(d))
                print('%s = %d' % (new_f, r))
        except ZeroDivisionError:
            pass
    if not resolved:
        print('不可解')
    return resolved


def unresolvable():
    """穷举不可解组合"""
    tps = itertools.combinations(range(1, 11), 4)
    for t in tps:
        if not test(t):
            print(t)


def main(argv):
    parser = argparse.ArgumentParser(
        description="crack 24 computation problem, with Python3.4+ required")
    parser.add_argument('a', type=int, help='a')
    parser.add_argument('b', type=int, help='b')
    parser.add_argument('c', type=int, help='c')
    parser.add_argument('d', type=int, help='d')
    args = parser.parse_args(argv[1:])
    test([args.a, args.b, args.c, args.d])
    # unresolvable()


if __name__ == '__main__':
    main(sys.argv)
