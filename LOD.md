LOD (Linked Open Data) Implementation Details
===

__DRAFT DOCUMENT__

## Persistent Identifiers

Coptic Scriptorium uses [CTS URNs](http://www.homermultitext.org/hmt-docs/specifications/ctsurn/) to provide persistent, technology-independent, identifiers for the texts in its corpus. It combines these with a URL prefix and format postfixes to provide stable, Linked-Data friendly URIs for the texts.

The scheme used is as follows:

Technology-independent identifier for a text: 

`<CTSURN>`

Linked-data friendly but format-independent persistent URI for a text:

`http://copticscriptorium.org/<CTSURN>`

Visualization and Format specific identifiers for texts:

__Visualization__ | __Format__ | __URI__
--- | --- | ---
TEI  | XML | `http://copticscriptorium.org/<CTSURN>/tei/xml`
PAULA |  XML |  `http://copticscriptorium.org/<CTSURN>/paula/xml`
Diplomatic | HTML | `http://copticscriptorium.org/<CTSURN>/dipl/html`
Normalized | HTML | `http://copticscriptorium.org/<CTSURN>/norm/html`
Analytical | HTML | `http://copticscriptorium.org/<CTSURN>/ana/html`

## Versioning

Coptic Scriptorium uses the *exemplar* component of a CTS URN to identify specific versions of a text.  At the point of "publication" (exact meaning of this TBD), new URNs will be minted for the Coptic Scriptorium texts with either a datetime stamp or a Git commit hash to represent the version information.

Note that Coptic Scriptorium commits to not changing the representation of a text identified by a specific exemplar (i.e. versioned) URN, but it may not provide online access to the texts represented by those versions for perpetuity. It will however always redirect a request for a specific exemplar to a more recent version of the text, if the specifically requested exemplar is no longer available on via the Coptic Scriptorium online publication site. (See below under HTTP Responses for additional details.)

An example of a versioned exemplar URN for a Coptic Scriptorium text might be:

`urn:cts:copticLit:shenoute.A22.MONB_YA.20141108T000000Z`

## HTTP Responses

Coptic Scriptorium uses the [303 URI approach](http://linkeddatabook.com/editions/1.0/#htoc12) to resolve requests for texts identified by the persistent URIs described above.

A request for a text without reference to a specific exemplar will return an HTTP 303 response which redirects the browser or requesting client application to the most recent version of the text.  Requests for texts without specification of the format will return a list of links to the available formats and versions.

Example requests, HTTP status code and returned representation are provided below.

__URI__: `http://copticscriptorium.org/urn:cts:copticLit:shenoute.A22.MONB_YA`

__HTTP Response Status__: 303 

__Returned Representation__: a list of links to available formats and versions of this text. 

---

__URI__: `http://copticscriptorium.org/urn:cts:copticLit:shenoute.A22.MONB_YA.YYYYMMDDTHHMMSSZ`

__HTTP Response Status__: 303

__Returned Representation__: a list of links to available formats of the requested exemplar (or if no longer example, the most recent version) of the text

---

__URI__: `http://copticscriptorium.org/urn:cts:copticLit:shenoute.A22.MONB_YA.YYYYMMDDTHHMMSSZ/tei/xml`

__HTTP Response Status__: 200 or 303

__Returned Representation__: the TEI XML representation of either the requested exemplar (with status 200) or the most recent version (with status 303)

---

__URI__: `http://copticscriptorium.org/urn:cts:copticLit:shenoute.A22.MONB_YA/norm/html`

__HTTP Response Status__: 303

__Returned Representation__: Most recent version of the normalized HTML edition of the text


## CTS API and Citation/Passage Identifiers

The exact details of the CTS API implementation for Coptic Scriptorium are still TBD.  

An initial CTS text inventory can be found at https://github.com/CopticScriptorium/cts/blob/master/inventory/textinventory.xml .

## Vocabulary

Relationships between the texts in the Coptic Scriptorium corpus are described using the [LAWD Ontology](https://github.com/lawdi/LAWD).

An N3 representation of the initial CTS text inventory, using the LAWD ontology can be found at https://github.com/CopticScriptorium/cts/blob/master/inventory/textinventory.ttl .



