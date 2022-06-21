# What is XML?

### *XML = eXtensible Markup Language*

> -software and hardware independent way of **storing, transporting, and sharing data**
>
> -<u>carries</u> data, does NOT <u>present</u> it ()
>
> -works between any programs
>
> -uses tags **`<>`** which are not limited and <u>not predefined</u>
>
> -can create your own tags, they are <u>extendable</u>

### XML Syntax:

---

#### <u>Declaration</u>

​	An XML document can have a <u>declaration</u> as the 1st line, which shows the version and encoding type

​	A declaration must begin with: `<?xml` and end with `?>` 

​			**`<?xml version="1.0" encoding="UTF-8"?>`** 

#### <u>Element</u>

​	An <u>element</u> is: **`<element>*something*</element>`** 

​	A **<u>root element</u>** is the <u>top-most</u> element in an XML document

​					*XML documents can only have <u>one root element</u>

​	Elements are <u>case sensitive</u> so `<friendlist>` and `<friendList>` are two different elements

##### 	Comments

​		Comments can be made using this format: `<!--comment-->`

##### Example:

```xml
<?xml version="1.0" encoding="UTF-8"?>  <!--this is an XML declaration--> 
<friendsList>
    <friend>
        <name>Alex</name>
    </friend>
    <friend>
    	<name>Mary</name>
    </friend>
    <friend>
    	<name>Rachel</name>
    </friend>
    <bestFriend>
    	<name>Rachel</name>
    </bestFriend>
</friendsList>
```

Here the <u>root element</u> is `<friendsList>` and there is no other element declared on that level



#### <u>Attribute</u>

​	An <u>attribute</u> is a single property for an element using a name/value pair

​	They cannot contain multiple values or tree structures (elements can), and they are not easily expandable 

​	Attribute syntax: **`<element attributeName = "attributeValue"> `**

​										**``*elements that belong to attribute* `**										

​								**`</element>`**

##### Example:

```xml
<person gender="female">  <!--the element'person'has an attribute 'gender' which as a value "female"--> 
	<firstname>Anna</firstname>	
    <lastname>Smith</lastname>
</person>
```

##### We can do the same example but as just elements:

```xml
<person>
  <gender>female</gender>
  <firstname>Anna</firstname>
  <lastname>Smith</lastname>
</person>
```



​	Attributes are usually used for **metadata (data about data)**

​	For example, we can have a `<note>` element and have multiple of it, so to distinguish between them, we can assign it an attribute

##### Example:

```xml
<messages>
  <note id="501">
    <to>Tove</to>
    <from>Jani</from>
    <heading>Reminder</heading>
    <body>Don't forget me this weekend!</body>
  </note>
  <note id="502">
    <to>Jani</to>
    <from>Tove</from>
    <heading>Re: Reminder</heading>
    <body>I will not</body>
  </note>
</messages>
```

 Here there are multiple notes, but we can identify which is which by their `id` attributes 

---

# XML Namespaces

> Namespaces provide a method to **avoid element name conflicts**
>
>  When a namespace is defined for an element, all child elements also get the same namespace
>
> The <u>attribute</u> `xmlns` is used to declare a namespace

### Syntax:

**`<element xmlns="URI">`**

#### <u>URIs:</u>

A URI is a **Uniform Resource Identifier** 

It's a string of characters which identifies an Internet Resource

The most common URI is a **URL** (Uniform Resource Locator)

##### Example:

```xml
<f:table xmlns: f="https://www.w3schools.com/furniture">  <!--URI that contains information about piece of furniture-->
  <f:name>African Coffee Table</f:name>
  <f:width>80</f:width>
  <f:length>120</f:length>
</f:table>
```

---

# XML Schema

### *XML Schema Definition (XSD)*

> An XML Schema document (**.xsd**) contains the definitions for **elements, attributes, & data types**
>
> An XSD is used to <u>describe and validate the structure and content</u> of XML data
>
> Schema element supports <u>Namespaces</u>
>
> An XML document **validated** against an XML Schema is both **"Well Formed"** and **"Valid"**



It's easier to show an example of a Schema

##### Example:

```xml
<xs:element name="note">	<!--defines the element called "note"-->

	<xs:complexType>			<!--"note" element is complex type-->
        <xs:sequence>				<!--the complex type is a sequence of elements (they're in order)-->
   			<xs:element name="to" type="xs:string"/>
  			<xs:element name="from" type="xs:string"/>      <!--these all say the element name and type-->
    		<xs:element name="heading" type="xs:string"/>
    		<xs:element name="body" type="xs:string"/>
  		</xs:sequence>
	</xs:complexType>

</xs:element>
```



### Definition Types:



#### <u>Simple Type:</u>

**String:**

```xml
<full_name>Alina Burlacu</full_name>     <!--element declaration-->

<xs:element name = "full_name" type = "xs:string" />  <!--schema-->
```

**Integer:**

```xml
<phone_number>123-456-7890</phone_number>     <!--element declaration-->

<xs:element name = "phone_number" type = "xs:integer" />  <!--schema-->
```

**Date:**

```xml
<birth_date>2000-12-11</birth_date>

<xs:element name = "birth_date" type = "xs:date" />
```

**Boolean:**

```xml
<registration>True</registration>

<xs:element name = "registration" type = "xs:boolean" />
```



#### <u>Complex Type:</u>

This is a **container** for other elements, used if an element has **child elements**

Uses different syntax than simple type:

```xml
<xs:element name="note">	
	<xs:complexType>		<!-- type is not on same line as element name-->
   			<xs:element name="to" type="xs:string"/>
```

			##### 				<u>Indicators:</u>

​						We can control **how** elements are to be used

​						In addition to complex type, we can specify what **order/occurrences** elements must have  

​						**`<xs:sequence>` .... `</xs:sequence>`**  : child elements must appear in <u>specific order</u>

​						**`<xs:choice>` ... `</xs:choice>`** :  <u>either/or</u> child element can occur

​						**`<xs:all>` ... `</xs:all>`** : child elements can appear in <u>any order</u> & must occur <u>only once</u>

---

# Parsing XML w/Python

> Using the **`xml.etree.ElementTree`** module to implement a simple **API** to parse and create XML data

### Example:

//main.py :

```python
import xml.etree.ElementTree as ET

# import data by reading from file 'sample.xml'
tree  = ET.parse('sample.xml')

# returns the root element of the XML file
root = tree.getroot()

print(root)
# print will return this statement:
# <Element 'data' at 0x00000165AC3393B0>


# As an Element, data has a tag and a dictionary of attributes
print(root.tag)  # prints: data


# It also has child nodes, which can be accessed by index since they are nested
# The .attrib method wll return a dict of attributes for the element
# Here the first element is <person id = "100" > and it only has one attribute: id
print(root[0].attrib) # prints {'id': '100'}

#since child nodes are nested, we can iterate over them to print their info
for child in root[1]:  #this will iterate over all child elements of the first element
    print(child.tag ,child.text)  #.text will return the value for a certain tag (for ex: tag is firstName, will return John)
# prints:
# firstName John
# lastName Doe
# age 25
# registered Yes

# We can also use 2d index to access specific tag of an element
# this looks at the first[0] 'person' element and the second[1] element tag 'lastName'
print(root[0][1].text) #prints: Doe

# To look for specific tags in the XML file, we can iterate using .find and .findall methods
# .find() returns the first matching element, or none
# .findall() returns a list with all matching elements
for x in root:
    age = x.find('age').text  # prints: 25   32
    names = x.findall('age')  # prints: [<Element 'age' at 0x000001AD4BAA45E0>]
    print(age,names)


```

// sample.xml 

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<data>
    <person id = "100" >
        <firstName>John</firstName>
        <lastName>Doe</lastName>
        <age>25</age>
        <registered>Yes</registered>
    </person>
    <person id = "101" >
        <firstName>Anna</firstName>
        <lastName>Smith</lastName>
        <age>32</age>
        <registered>No</registered>
    </person>

</data>
```

### Element class objects:

This class defines the Element interface, and provides a reference implementation of this interface. [HERE IS REFERENCE DOCUMENTATION](https://docs.python.org/3/library/xml.etree.elementtree.html#element-objects)

We used some of these: 

​		**.attrib** returns a dictionary containing element's attributes

​		**.tag** returns the sting identifying the data type of the element

​		**.text** returns the value for a certain tag (ex: tag is 'firstName', will return 'John')







































