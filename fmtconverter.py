#! /usr/bin/env python
# coding:utf-8


if __name__ == '__main__':
    from sys import argv, stdin
    delimiter = argv[1]
    for line in stdin:
        line = ' '.join(line.rstrip())
        line = line.replace(" {} ".format(delimiter), "{}".format(delimiter))
        print(line)
