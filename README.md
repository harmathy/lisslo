What is Lisslo?
===============

Lisslo stands for "LiMux Shutdown Scheduling for Logind"

Handle users' shutdown requests and system events requiring shutdown.
    
There are two interfaces: one for processing user shutdown requests and 
one for system events to schedule a shutdown e.g. for system updates. 

A DBus interface to logind is used to get information about user sessions
and conduct actual shutdown.
