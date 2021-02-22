Getting Started
===============

Once you have added Clean Insights as a dependency of your project, you can
begin adding integration with your code.

Configuration
-------------

Initialization
--------------

.. code-block:: python

   from cleaninsights import CleanInsights
   from cleaninsights.store import Store

   ...

   store = Store("memory")
   ci = CleanInsights(config, store)

Measure your first visit
------------------------

.. code-block:: python

   ci.measure_visit("application/start", "simple")
