code = [
    '\x1f',
    '\x12',
    '\x1d',
    '(',
    '0',
    '4',
    '\x01',
    '\x06',
    '\x14',
    '4',
    ',',
    '\x1b',
    'U',
    '?',
    'o',
    '6',
    '*',
    ':',
    '\x01',
    'D',
    ';',
    '%',
    '\x13']
code = [ord(i) for i in code]

for i in range(len(code) - 1):
    code[len(code) - 2 - i] ^= code[len(code) - 1 - i]

for i in range(len(code)):
    code[i] = (code[i] - i + 128) % 128

print(''.join([chr(i) for i in code]))
