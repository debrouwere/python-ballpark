Ballpark
========

When people think of human-readable numbers, they think of rounding to
two decimal places and adding a thousands separator. 12,214.17 is
already quite an improvement over 12214.16666667. But standard formats
for human-readable numbers still have various flaws:

-  even with a thousands separator, at a glance you might easily mistake
   a billion for a trillion
-  even when rounding, an amount like 12,214.17 dollars is a lot of
   number noise for communicating 12.2K
-  scientific notation leads to exponents like ``1.22e4`` which are hard
   to interpret because we're used to working with thousands, millions
   and billions – orders of magnitudes that are multiples of three
-  when comparing multiple measurements of the same underlying variable,
   like the yearly sales numbers for 2010-2015, it's annoying to have
   some numbers in thousands and other numbers in millions – you want
   consistency so that digits in the same position are of the same
   magnitude

``python-ballpark`` introduces *business notation*, an offshoot of
`engineering
notation <https://en.wikipedia.org/wiki/Engineering_notation>`__, for
producing better human-readable numbers.

Install with ``pip install ballpark`` or ``pip3 install ballpark``.

What it looks like
~~~~~~~~~~~~~~~~~~

+---------------------+-----------------------+-----------------+-----------------+
| numbers             | rounded               | engineering     | **business      |
|                     |                       | notation        | notation**      |
+=====================+=======================+=================+=================+
| 11234.22,           | 11,234.22,            | 11.2E+3,        | 11K, 233K,      |
| 233000.55,          | 233,000.55,           | 233E+3, 1.18E+6 | 1,180K          |
| 1175125.2           | 1,175,125.2           |                 |                 |
+---------------------+-----------------------+-----------------+-----------------+
| 111, 1111.23,       | 111, 1,111.23,        | 111, 1.11E+3,   | 0.11K, 1.11K,   |
| 1175125.234         | 1,175,125.23          | 1.18E+6         | 1,180.00K       |
+---------------------+-----------------------+-----------------+-----------------+

How to use it
~~~~~~~~~~~~~

.. code:: python

    >>> from ballpark import human, scientific, engineering, business, ballpark
    >>> business([11234.22, 233000.55, 1175125.2])
    ['11K', '233K', '1,180K']
    >>>
    >>> # business notation is also aliased as `ballpark`
    >>> ballpark([11234.22, 233000.55, 1175125.2])
    ['11K', '233K', '1,180K']
    >>>
    >>> # or use the shortcut functions
    >>> from ballpark import H, S, E, B
    >>> B([11234.22, 233000.55, 1175125.2])
    ['11K', '233K', '1,180K']
    >>>
    >>> # all notations accept single numbers too, but then we can't guarantee
    >>> # that all numbers will have the same prefix (kilo, mega etc.)
    >>> [B(value) for value in [11234.22, 233000.55, 1175125.2]]
    ['11.2K', '233K', '1.18M']

How it works
~~~~~~~~~~~~

.. code:: python

    business(values, precision=3, prefix=True, prefixes=SI, statistic=median)

-  **precision:** the amount of significant digits. When necessary,
   ``business`` will round beyond the decimal sign as well: in the
   example above, ``1175125.2`` was turned into ``1,180K`` rather than
   ``1,175K`` to retain only 3 significant digits.
-  **prefix:** whether to use SI prefixes like m (milli), K (kilo) and
   so on instead of scientific exponents like E+03.
-  **prefixes:** a mapping of orders of magnitude to prefixes, e.g.
   ``{-3: 'm', 3: 'K'}``, allowing you to customize the prefixes, for
   example using B for billion instead of T for tera.
-  **statistic:** a function to produce the reference number. The
   reference number determines the order of magnitude and precision for
   the entire group of numbers, so that for example when the reference
   number is 23.3K, smaller numbers like 1.1K won't gain a decimal place
   and larger numbers like 1,180K won't jump an order of magnitude to
   1.18M. The median often works well, but if you want more precision
   for small outliers, try ``ballpark.statistics.Q1`` or even Python's
   builtin ``min``.
