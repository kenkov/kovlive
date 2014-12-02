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


モデルのつくりかた
=====================

モデルの作成には ``jinja2`` とその依存の ``markupsafe`` が必要ですので、
あらかじめインストールしてください。

.. code-block:: bash

    $ pip install jinja2 markupsafe

次に ``Makefile`` を生成して ``make`` します。

.. code-block:: bash

    $ # Makefile を生成する
    $ python config.py
    $ make
