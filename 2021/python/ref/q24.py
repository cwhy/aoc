import numpy as np

test_contents = """
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
"""

with open('2021/input24.txt') as file:
    contents = file.read()


def get_program(_contents, fn_name) -> str:
    asts = []
    n_inputs = 0
    for row in _contents.strip().split('\n'):
        words = row.strip().split(" ")
        if words[0] == 'inp':
            asts.append(f"    {words[1]} = s[{n_inputs}]")
            n_inputs += 1
        elif words[0] in 'add':
            asts.append(f"    {words[1]} += {words[2]}")
        elif words[0] == 'div':
            asts.append(f"    {words[1]} //= {words[2]}")
        elif words[0] == 'mod':
            asts.append(f"    {words[1]} %= {words[2]}")
        elif words[0] == 'mul':
            asts.append(f"    {words[1]} *= {words[2]}")
        else:
            assert words[0] == 'eql'
            asts.append(f"    {words[1]} = int({words[1]} == {words[2]})")

    header = f"def {fn_name}(s):\n    x=z=x=y=0\n"
    program = header + "\n".join(asts) + "\n    return w, x, y, z"
    print(program)
    return program

exec(get_program(test_contents, 'ft'))
exec(get_program(contents, 'f'))

num = 123123
assert "{:#b}".format(num)[-4:] == "".join([str(i) for i in ft([num])])

print(f)
print(f([1, 3, 5, 7, 9, 2, 4, 6, 8, 9, 9, 9, 9, 9]))

max_digit = 8
digits = [max_digit] * 14
num = int("".join([str(i) for i in digits]), 9)

while f(digits)[-1] != 0:
    # print(f(digits))
    num -= 1
    num_repr = np.base_repr(num, 9)
    digits = [int(i) + 1 for i in num_repr]
    # print(x_pos)
