# A proxy server to integrate PI and Maximo

Notifications, a feature of a PI Server that allows for the transmission of alarms to users and external systems supports several authentication methods, including Windows and Basic authentication. It does not support authentication such the one required by Maximo which uses a *MAXAUTH* custom http header.

This script is a proxy server which receives notifications from a PI Server, adds in the custom header and send it to Maximo. It does update the content of the request in any case.

# Usage

In config.json file, set in your *MAXAUTH* value, the base URL of your Maximo server and the port you wish to proxy server to use.

The details on how the PI Server's notification will be shown in a PI Square post later.