# DSCI-558
The assignments I finished and the material used in USC [DSCI-558 Building Knowledge Graphs](https://classes.usc.edu/term-20203/course/dsci-558) course, which brought by [USC Knowledge Graph Center](https://usc-isi-i2.github.io/home/).

## Summaries

|      | Subject                                                    | Library                                                      | Technique                                                    | Description                                                  |
| :--- | ---------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1    | Web Scraping                                               | [Scrapy](https://scrapy.org/)                                |                                                              | Using Scrapy, crawl 10k pages from IMDB, extract attributes from each page, store the outcome into Json-lines files. |
| 2    | Information Extraction                                     | [spaCy](https://spacy.io)                                    | NLP                                                          | Using spaCy, form actor's biography text, for each attribute, build one Lexical extractor and one Syntactic extractor. |
| 3    | Entity Resolution, Blocking & Knowledge Representation     | [The Record Linkage ToolKit (RLTK)](https://github.com/usc-isi-i2/rltk), [RDFLib](https://rdflib.readthedocs.io/en/stable/) |                                                              | Given two datasets of IMDB and AFI, and a dev dataset. <br />Match records from these 2 datasets (record linkage). Use Blocking to reduce the number of pairs need to compare. <br />Design a model in [RDF Schema](https://www.w3.org/TR/rdf-schema/), store the result in a [turtle](https://www.w3.org/TR/turtle/) using the designed model. |
| 4    | RDF query                                                  | [Apache Jena](https://jena.apache.org/tutorials/sparql.html) | [SPARQL](https://www.w3.org/TR/sparql11-query/), [WikiData Query](https://query.wikidata.org/) | Write SPARQL queries to solve several intricate requests.    |
| 5    | IE - Revisit<br />Weak Supervision and Distant Supervision | [Snorkel](https://www.snorkel.org/)                          | [Weak Supervision](https://dawn.cs.stanford.edu/2017/07/16/weak-supervision/),  [Distant Supervision](http://www.semantic-web-journal.net/system/files/swj742.pdf) | Hand label a small set of dev data, write label functions using Snorkel, combined with distance supervision, label training set.<br />Output a Generative Model. |
| 6    | PSL and OWL                                                | [PSL](https://github.com/linqs/psl), [Protégé](https://protege.stanford.edu/) | [Probabilistic Soft Logic](https://psl.linqs.org/), [OWL](https://www.w3.org/TR/owl-features/) | Write the PSL model to link the same paper. <br />Using Protege to build an OWL ontology and try some reasoning. |
| 7    | Tabular Data & Knowledge Graph Embedding                   | [AmpliGraph](https://github.com/Accenture/AmpliGraph)        | [RDF Data Cube](https://www.w3.org/TR/vocab-data-cube/), [KG Embedding](https://towardsdatascience.com/introduction-to-knowledge-graph-embedding-with-dgl-ke-77ace6fb60ef) |                                                              |

## Documents

The W3C documents are hard to read: poorly typography and impossible to mark up.  KG is a rapid-growing domain, lacks well-written documents. I put my organized W3C documents and other useful materials here.

