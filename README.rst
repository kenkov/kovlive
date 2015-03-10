===========
ｺﾌﾗｲﾌﾞｯ！
===========

このスクリプトを使うと、文字列をこふ語に変換することができます。

使い方
=======

Python3 が必要です。

.. code-block:: bash

    $ echo 今日のお昼は、ステーキを食べたい。 | python3 kovlive.py
    今日のお昼はっｽﾃｯｷを食べたいっ

.. code-block:: bash

    $ python3 kov.py -h
    usage: kov.py [-h] [-v] [file]

    positional arguments:
      file           input file: if absent, reads from stdin

      optional arguments:
        -h, --help     show this help message and exit
        -v, --verbose  show probability


より詳しい解説は
http://blog.kenkov.jp/pages/software/kovlive.html
をみてください。
