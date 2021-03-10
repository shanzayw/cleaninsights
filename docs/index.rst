Clean Insights' Python SDK 📏🐍💡
=================================

Privacy-preserving measurement and analytics for Python.

Introduction
------------

`Clean Insights <https://cleaninsights.org/>`_ gives developers a way to plug
into a secure, private measurement platform. It is focused on assisting in
answering key questions about app usage patterns, and not on enabling invasive
surveillance of all user habits. Our approach provides programmatic levers to
pull to cater to specific use cases and privacy needs. It also provides methods
for user interactions that are ultimately empowering instead of alienating.

This Python SDK is part of the wider Clean Insights ecosystem that includes
SDKs in other languages, a consent user interface toolkit and server plugins.
All these tools can be found on the `Clean Insights Developers Page
<https://cleaninsights.org/dev>`_.

Target Audience
---------------

Both the Apple and Android SDKs are targetted at being embedded into
client-side end-user applications on those platforms. The JavaScript SDK may be
used in an end-user web application or embedded in a server-side node.js
backend. Similarly, the Python SDK is intended to be embedded into either an
end-user client-side application or a server-side backend.

The Python SDK aims to provide more features that are useful for server-side
integration, such as support for the use of a relational database for storage.
In this way, it does not provide the complete feature set for the consent
portions of the API as there is no obvious user interface to implement helpers
for. This does not preclude the use of this SDK in a client-side end-user
application but explains why some functions present in other SDKs may be
missing in this version.

Data Analysis and Visualisation
-------------------------------

This SDK does not provide tools for performing analysis of the collected data
beyond providing the ability to dump the collected data to CSV or submit the
sanitised data to a Matomo instance via a `Clean Insights Matomo Proxy
<https://gitlab.com/cleaninsights/clean-insights-matomo-proxy>`_.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   install
   quickstart
   api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
