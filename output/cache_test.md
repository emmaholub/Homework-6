# Cache comparison

I ran all 12 practice documents twice through `gpt-6-luna`. The cache-on and cache-off records below come directly from provider-reported usage in `output/cache_test.json`. The cache-off run is valid: all 12 records have `cache_read_tokens: 0`.

## Totals

| Setup | Calls | Total cost | Average per document |
|---|---:|---:|---:|
| Caching on | 12 | `$0.005487905` | `$0.000457325` |
| Caching off | 12 | `$0.033179025` | `$0.002764919` |

Savings: `($0.033179025 - $0.005487905) / $0.033179025 × 100 = 83.46%`.

## Per-document cost

| Document | Cached | Uncached |
|---|---:|---:|
| p01_bluehen_quote.html | `$0.00156347` | `$0.00276145` |
| p02_elmcity_quote.html | `$0.00035144` | `$0.00276045` |
| p03_ivyprint_catalog.html | `$0.00035670` | `$0.00274783` |
| p04_harborstitch_quote.html | `$0.00036634` | `$0.00276020` |
| p11_yorkst_quote.html | `$0.00034570` | `$0.00275295` |
| p05_maplemills_quote.pdf | `$0.00036007` | `$0.00278133` |
| p06_qtextile_quote.pdf | `$0.00036607` | `$0.00277120` |
| p07_longwharf_quote.pdf | `$0.00036819` | `$0.00278207` |
| p12_bluehen_quote.pdf | `$0.00034631` | `$0.00274983` |
| p08_chapelst_email.eml | `$0.00035283` | `$0.00276970` |
| p09_westville_email.eml | `$0.00034696` | `$0.00277195` |
| p10_eastrock_email.eml | `$0.00036383` | `$0.00277008` |

## Projection: 1,000 documents per day for 30 days

The average-document projection is:

- Caching on: `30,000 × $0.000457325 = $13.719763`
- Caching off: `30,000 × $0.002764919 = $82.947563`
- Monthly savings: **$69.227800**

## Comparison with Problem 2

Problem 2 estimated the handbook alone at `$0.0010184` for one uncached call and `$0.1030112` for 1,000 calls with one cache write and 999 cached reads. The live totals are higher because each document now requires a document-reading tool call plus a structured-answer call, with tool schemas, document content, and output tokens included. The corrected formula subtracts cache-read and cache-write tokens from the ordinary input count before applying their separate rates.

## Surprises

The cache saved **83.46%** in this run because the handbook and stable instructions are reused. The first cached document is more expensive because it creates the cache entry. The cache-off setup pays the cache-write rate (`$0.125/M`) on every call in addition to ordinary input and output costs, which is higher than the plain input rate (`$0.10/M`).
