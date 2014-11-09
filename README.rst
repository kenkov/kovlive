========
こふ語
========

このスクリプトを使うと、文字列をこふ語に変換することができます。

.. code-block:: bash

    usage: kov.py [-h] [-v] [infile]

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  show probability

.. code-block:: bash

    $ echo 今日のお昼はステーキを食べたい | python3 kov.py
    <s>今日のお昼はｽﾃｯｷを食べたいっ</s>


使い方
=======

python3 が必要です。 ``make`` してモデルを作成します。

.. code-block:: bash

    $ make

テストするには ``nose`` をいれて

.. code-block:: bash

    $ make test

してください。

