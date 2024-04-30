import idc

for i in range(0x1135, 0x3100):
    if idc.get_db_byte(i) == 0xc0:
        print(chr(idc.get_db_byte(i + 2)), end = '')
