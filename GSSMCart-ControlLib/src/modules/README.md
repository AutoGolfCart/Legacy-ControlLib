# Hardware Modules

These are classes that correspond to the physical hardware controller modules. They contain methods that correspond to CAN messages that those modules can process. It can also check and process returned messages. The methods return the messages instead of sending them, so they will have to be placed into another method to actually be written to the bus. These hardware abstractions should be used within the Cart abstraction class "MyCart"