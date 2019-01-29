# HTMLContentExtraction

Benchmarks the most common open-source **HTML content extractors** (on Python) :
- [Goose](https://github.com/grangier/python-goose)
- [eatiht](https://github.com/rodricios/eatiht) 
- [Dragnet](https://github.com/dragnet-org/dragnet) 
- [libextract](https://github.com/datalib/libextract) 
- [Newspaper](https://github.com/codelucas/newspaper)
- [BoilerPipe](https://github.com/misja/python-boilerpipe)

## How to use

### Prerequisites

Developed in Python 2.7

Install the requirements.txt :

```bash
pip install requirements.txt
```
Place your HTML files into *./data/htmlfiles*, or generate them from urls with **HTMLextract.py** (best is to use a urls.csv file in *./data* with 2 columns: file ID | URL)

### Files

- **HTMLextract.py** allows to generate a HTML file for each URL specified in *./data/urls.csv*.

- **benchmark.py** prints the result of the content extraction with each method, from a random HTML file in *./data/htmlfiles/*.
Results & stats for each method can be found in **[benchmarkStats.ods](./benchmarkStats.ods)** (benchmark done on a corpus of press & blog articles).

- **contentextraction.py** allows to generate a text file for each HTML file stored in *./data/htmlfiles/*, using the best method (currently Dragnet).

- **duplicates.py** allows to generate a csv file as a result, showing the url, the extracted text and if the record is a duplicate of another one. Use once the text content files are generated.

## Benchmark results

### Goose *vs* eatiht *vs* Dragnet *vs* libextract *vs* Boilerpipe

Quick comparison of these 5 common libs.
Tested on 30 random press & blog articles ([benchmark file](./benchmarkStats.ods)), each result being compared with the source page.

![](./stats.png)


### Dragnet *vs* Newspaper

Two Py3-compatible & relatively advanced tools, compared on a corpus of 60 random press & blog articles ([benchmark file](./dragnet_vs_newspaper.csv)). 

Both work pretty well, but Newspaper catches more irrelevant items liek "See also ..." and - more importantly - invariably fails on some websites (like *bfmtv.com*).

![](./dragnetvsnewspaper.png)

