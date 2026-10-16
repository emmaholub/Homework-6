# Shop handbook cost estimate

## Token count

The handbook is `data/shop_handbook.md`. I counted **10,184 tokens** using the `tiktoken` library with the `cl100k_base` encoding, rather than estimating from the word count. The command used was:

```bash
python -c "import pathlib, tiktoken; s=pathlib.Path('data/shop_handbook.md').read_text(); print(len(tiktoken.get_encoding('cl100k_base').encode(s)))"
```

The file has 6,127 whitespace-separated words, but that is not the number used for pricing. The token count above is the number used in the calculations below. If the course model uses a different tokenizer, Problem 4's actual usage is the final check.

## Prices used

From `data/prices.json` for `gpt-6-luna`:

- Normal input: `$0.10` per 1,000,000 tokens
- Cached input: `$0.01` per 1,000,000 tokens
- Cache write: `$0.125` per 1,000,000 tokens

The handbook token count is `10,184`, or `0.010184` million tokens.

## One call

Without caching:

```text
10,184 / 1,000,000 × $0.10 = $0.0010184
```

With caching, I treat the first call as a cache write:

```text
10,184 / 1,000,000 × $0.125 = $0.0012730
```

## 1,000 calls

Without caching:

```text
1,000 × $0.0010184 = $1.0184
```

With caching, the first call writes the handbook to the cache and the next 999 calls use the cached-input rate:

```text
Cache write: 10,184 / 1,000,000 × $0.125 = $0.0012730
999 cached reads: 999 × (10,184 / 1,000,000 × $0.01) = $0.1017382
Total: $0.0012730 + $0.1017382 = $0.1030112
```

Therefore, the estimate is **$1.0184 for 1,000 uncached calls** versus **$0.1030112 for 1,000 calls with one initial cache write and 999 cached reads**. These numbers include only the handbook input; they exclude the user's prompt, retrieved documents, output tokens, and any other request overhead.
