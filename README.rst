========
こふ語
========

このスクリプトを使うと、文字列をこふ語に変換することができます。

.. code-block:: bash

    $ python3 kov.py -h
    usage: kov.py [-h] [-v] [file]

    positional arguments:
      file           input file: if absent, reads from stdin

      optional arguments:
        -h, --help     show this help message and exit
        -v, --verbose  show probability

.. code-block:: bash

    $ echo 今日のお昼は、ステーキを食べたい。 | python3 kov.py
    今日のお昼はっｽﾃｯｷを食べたいっ


使い方
=======

python3 が必要です。 ``make`` してモデルを作成します。

.. code-block:: bash

    $ make

テストするには ``nose`` をいれて

.. code-block:: bash

    $ make test

してください。

