# What is an API?

### *API = Application Programming Interface*

> API is a part of a computer program that is used by another program
>
> A web API is a type of API that is accessed through HTTP using a browser

## Terminology:

### HTTP:

#### *Hyper Text Transfer Protocol*

> A way of communicating data on the web
>
> Implements different **"methods"** which tell which direction data is moving and what should happen to it

| Method Name | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| **GET**     | Used to ***retrieve data*** from the given server using a given URI. |
| **POST**    | Used to ***send data*** to the server (i.e. file upload, customer information using HTML forms) |
| **PUT**     | Used to ***replace*** all current representations of the target resource with the uploaded content |
| **DELETE**  | Used to ***remove*** all current representations of the target resource given by a URI |

#### <u>HTTP Status Codes:</u> 

[LINK FOR FULL LIST](https://www.restapitutorial.com/httpstatuscodes.html)

**1xx = Informational**

**2xx = Success**

**3xx = Redirect**

**4xx = Client Error**

**5xx = Server Error**

| Num     | Name                      | Description                                                  |
| ------- | ------------------------- | ------------------------------------------------------------ |
| **200** | **OK**                    | The request has succeeded. Typically returned when GET or POST request succeeded. |
| **201** | **Created**               | A new resource was successfully created using POST or PUT, may contain reference URI for the new resource. |
| **301** | **Moved Permanently**     | Requested resource has been assigned a new permanent URI. New URI should be returned. |
| **400** | **Bad Request**           | The request cannot be fulfilled due to bad syntax            |
| **401** | **Unauthorized**          | The request requires user authentication; either missing or invalid authentication token given. |
| **403** | **Forbidden**             | Request was legal, but server refuses to respond. User not authorized to perform operation or resource unavailable. |
| **404** | **Not Found**             | The requested resource was not found, also used when server doesn't wish to reveal exactly why request was refused. |
| **500** | **Internal Server Error** | The general catch-all error when the server-side throws an exception. |
| **502** | **Bad Gateway**           | The server was acting as a gateway or proxy and received an invalid response from the upstream server. |



### URL:

#### *Uniform Resource Locator*

> An address for a resource on the web
>
> A URL is a type of URI (Uniform Resource Identifier)



URLs consist of a **protocol** (`http://`), a **domain** (`wikipedia.org`) and an optional **path** (`/wiki/Polar_bear`)

So all together the URL is: [http://wikipedia.org/wiki/Polar_bear]

### JSON:

#### *JavaScript Object Notation*



> A <u>text-based data storage format</u> (similar to XML) used to return data through an API

---

---

# REST API Creation with Python

## REST:

### *REpresentational State Transfer*



> Guidelines used to <u>create an API</u>

### 1. Stateless

	- Requests from client to server **must contain all information** necessary to **understand and complete the request**
	- A server **cannot take advantage of any previously stored** context information 

### 2. Client-Server

- Design pattern which enforces **separation of concerns** which helps the client and server components **evolve independently** 
- By separating the *user interface concerns* (**client**) from the *data storage concerns*(**server**) we improve **portability across multiple platforms**
- Improve **scalability** by simplifying server components
- When the client and server evolve, we must make sure that the interface between them doesn't break

### 3. Uniform Interface

	- **Identification of resources:** Interface must uniquely identify each resource involved in the interaction between client/server
	- **Manipulate resources through representations:** Resources should have uniform representation in the server response
	- **Self-descriptive messages:** Each resource representation should hold enough info to describe how to process message
	- **Hypermedia as engine of application state:** Client should only have initial URI, all other resources/interactions should be dynamically driven with hyperlinks

### 4. Cacheable 

- Response should implicitly or explicitly label itself as cacheable or non-cacheable 
- If response is cacheable; client application gets right to **reuse the response data** later for **equivalent requests** and a **specified period**

### 5. Layered System

- Allows an architecture to be composed of **hierarchical layers** by constraining component behavior
- Each component cannot see beyond the immediate layer they are interacting with

### 6. Code on Demand

- Allows client functionality to **extend by downloading and executing code** in the form of **applets** or **scripts**
- The downloaded code simplifies clients by **reducing the number of features required to be pre-implemented**
- Servers can provide part of features delivered to client in the form of code, and client only needs to execute code 

## Flask Framework

### *Microframework in Python*

> Used to create web applications and APIs in Python
>
> Light weight and modular design 
>
> Has built in development server, debugger, HTTP request handling, and more..
>
> To install: `python pip install flask`

#### Tutorials:

YouTube videos:

 ["Building a Flask REST API"](https://www.youtube.com/watch?v=GMppyAPbLYk)

["REST API With Flask & SQLAlchemy"](https://www.youtube.com/watch?v=PTZiDnuC86g)

Follow-along tutorials:

["How to Use Flask-SQLAlchemy to Interact with Databases in a Flask Application"](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)

["Creating Web APIs with Python and Flask"](https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#creating-the-api)





Video API testing on POSTMAN link:

https://charter-pt.postman.co/workspace/My-Workspace~25f5a095-bf50-4c63-806f-fa271cda304c/collection/21333392-cb7aab52-b9e8-4d0c-9e80-bd0781bc5979







