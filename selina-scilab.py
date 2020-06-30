# coding:utf-8
#!/usr/bin/python3

import sys


def main():
    pass


def usages(prg_name)
    print("Usage:")
    print("  %s: <cmd> <params>", %prg_name)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usages(sys.argv[0])
        return
    main(sys.argv[1:])
