========
こふ語
========

このスクリプトを使うと、文字列をこふ語に変換することができます。

.. code-block:: bash

    $ echo 今日のお昼はステーキを食べたいっ | python3 kov.py
    今日のお昼はｽﾃｯｷを食べたいっ


使い方
=======

python3 が必要です。 ``make`` してモデルを作成します。

.. code-block:: bash

    $ make

テストするには ``nose`` をいれて

.. code-block:: bash

    $ make test

してください。

