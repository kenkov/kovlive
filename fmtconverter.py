#! /usr/bin/env python
# coding:utf-8


if __name__ == '__main__':
    from sys import argv
    fd = open(argv[1])
    for line in fd:
        line = ' '.join(line.rstrip())
        line = line.replace(" , ", ",")
        print(line)
