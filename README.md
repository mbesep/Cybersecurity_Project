# cyberProject
Major Course Project of Cybersecurity, University of Bologna 2023-2024  
Giuseppe Pio Salcuni  
Manuel Placella

## project 1 - Nebula network
Design and implement a proof of concept for "security domains" in a Nebula network. A security domain is a set of logically related resources that can communicate and subject to the following constraints:
* A resource can have multiple security domains
*	The information related to the security domain must be present in the resource's digital certificate
*	A resource can open a connection only toward another resource that share at least one security domain otherwise it is blocked by default
### Specifications
*	There must be a single configuration file where for each resource of the network are specified its security domains
*	From this configuration files it must be possible to generate all the nebula certificates and nebula configuration files to implement the constraints of the security domain for the whole network
*	Using the generated files, manually instantiate the network and verify the relevant connections
