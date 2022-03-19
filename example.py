import evalie

val = evalie.evalie()
last_val = 0
inp = ''

print('evalie - a toy eval\n'
      '------\n'
      'constants:\n'
      'e, pi, tao, phi\n'
      '------\n'
      '(1 + (5 ^ 0.5)) / 2')

while True:
    inp = str(input(f"({last_val}) -> "))

    if inp == 'exit':
        break

    last_val = val.eval(inp)

    if last_val is None:
        last_val = 0

    print(last_val)
