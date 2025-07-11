def to_string(n,base):
    convert_string= "0123456789ABCDEF"
    if n<base:
        print(n)
        return convert_string[n]
    else:
        return to_string(n//base,base) + convert_string[n%base]

print(to_string(3000,16))