# Design
Shaservice is broken into three peices:
 1) API
 2) Redis
 3) Nginx

## API
API/REST services can be written in a variety of ways. In this case we are using Connexion:

Connexion is a framework on top of Flask that automagically handles HTTP requests based on OpenAPI 2.0 Specification (formerly known as Swagger Spec) of your API described in YAML format. Connexion allows you to write a Swagger specification, then maps the endpoints to your Python functions; this makes it unique, as many tools generate the specification based on your Python code. You can describe your REST API in as much detail as you want; then Connexion guarantees that it will work as you specified.

Connextion is buit on top of Flask, a well known Python web framework.

We are using gevent webserver along with PyPy to host a non blocking endpoint for concurrent requests.

## Redis
Reversing a SHA256 is nearly impossible.  We need some place to shore the hashes in order to do a reverse lookup.  You can use any store you'd like, such as Postgres, MongoDB, Dynamo, etc.  As this use case is simply a key/value store, a high performance in-memory and sclable store is desired, which Redis is.

## Nginx
While it is completely possible to directly a Flask service with HTTPs, it adds additional complexity to the API. It is preferential to have services perform what they are best at.  APIs are good at serving data it is not necessarily a high performance and optimized proxy for SSL termination, which NGINX is.

# Logging
It is typically best practice to send all necessary logs within docker containers to standard out/err rather than writing logs inside the container.  Many beginners with docker find themselves with a non responsive service and later find out their container filled with logs since there was no rotation schedule set inside the container. 

A better process is to send logs to stdout/stderr and then use a logging agent to ship the logs off to an aggrigator like Sumologic, Splunk, and CloudTrail.

# Scaling
The current architecture is a fairly decent starting point for a scalable service.  Some areas that can be considered:

Typically a docker-compose file with volume mounts requires the entire service to be hosted on a single logical machine.  If this were being deployed, all three services would be hosted in a distributed nature with multiple replicas.  Instead of hosting the NGINX container with the service the API would use service discovery to register each container with a load balancer such as NGINX or an ALB (using ECS and target groups).

If we know that there are certain use cases where some queries will occur more often than others, we can have an Last Recently Used (LRU) cache on each API instance, instead of always going out to Redis to request the SHA256 digest.