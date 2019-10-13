====================
Configuration Schema
====================

To add your own model to the library you have to create a yaml file with the following structure


Sample File:

.. code-block:: yaml

    commands:
      - command: "Command for Projector"
        name: "Alternate Methodname in Code"
        display_name: "Name for Humans"

        response_parameters:
          - parameter: "Projector Parameter"
            name: "Alternative name to execute projector command with parameter"
            display_name: "Display Name for humans"

        request_parameters:
          - parameter: "Command for Project"
            name: "Alternative methodname"
            display_name: "Humand Readable Value"


