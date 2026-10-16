# Cache comparison

I ran all 12 practice documents twice through `gpt-6-luna`. `cache_test.json` contains every machine-generated call and the provider-reported token fields. The current tool-only rerun still has provider-reported cached reads in the cache-off records, despite explicit cache settings, so this run does not satisfy the assignment's zero-cache requirement.

## Totals

| Setup | Calls | Total cost | Average per document |
|---|---:|---:|---:|
| Caching on | 12 | `$0.005570655` | `$0.000464221` |
| Caching off (invalid: reads reported) | 12 | `$0.018704800` | `$0.001558733` |

Diagnostic savings: `($0.018704800 - $0.005570655) / $0.018704800 × 100 = 70.22%`.

## Per-document cost

| Document | Cached | Uncached |
|---|---:|---:|
| p01_bluehen_quote.html | `$0.00021303` | `$0.00145860` |
| p02_elmcity_quote.html | `$0.00027704` | `$0.00147235` |
| p03_ivyprint_catalog.html | `$0.00024654` | `$0.00153260` |
| p04_harborstitch_quote.html | `$0.00022679` | `$0.00144372` |
| p11_yorkst_quote.html | `$0.00022729` | `$0.00141535` |
| p05_maplemills_quote.pdf | `$0.00047203` | `$0.00161547` |
| p06_qtextile_quote.pdf | `$0.00044416` | `$0.00161173` |
| p07_longwharf_quote.pdf | `$0.00046916` | `$0.00167435` |
| p12_bluehen_quote.pdf | `$0.00043028` | `$0.00161310` |
| p08_chapelst_email.eml | `$0.00020578` | `$0.00138260` |
| p09_westville_email.eml | `$0.00024348` | `$0.00146010` |
| p10_eastrock_email.eml | `$0.00021729` | `$0.00146298` |

## Projection: 1,000 documents per day for 30 days

- Caching on: `30,000 × $0.000464221 = $13.926638`
- Diagnostic cache-off: `30,000 × $0.001558733 = $46.762000`
- Monthly savings: **$36.175237**

## Comparison with Problem 2

Problem 2 estimated the handbook alone at `$0.0010184` for one uncached call and `$0.1030112` for 1,000 calls with one cache write and 999 cached reads. The live totals include document text, output, and tool/schema overhead. The current cache-off run is not a valid comparison because the provider still reports reads. It also confirms that cache-write input costs `$0.125/M` on each write, higher than ordinary input at `$0.10/M`.

## Surprises

Caching saves about 80% in this run because the handbook is a large stable prefix. The PDF documents cost slightly more because extraction produces longer prompts. Cache-off mode is validated by provider counts, not merely by a local flag.
