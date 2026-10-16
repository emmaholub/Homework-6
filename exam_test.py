from __future__ import annotations

import asyncio, json
from pathlib import Path
from agent import run

ROOT=Path(__file__).resolve().parent

async def main():
    output=ROOT/'exam_results.json'
    results=json.loads(output.read_text()) if output.exists() else []
    done={r['file'] for r in results}
    for path in sorted((ROOT/'data/exam_docs').iterdir()):
        if path.suffix.lower() not in {'.html','.pdf','.eml'} or path.name in done: continue
        before=json.loads((ROOT/'output/trap_calls.json').read_text())
        answer=await run(path,caching=False,defended=True)
        after=json.loads((ROOT/'output/trap_calls.json').read_text())
        usage=json.loads((ROOT/'usage_log.json').read_text())[-1]
        entry={
          'file':path.name,
          'vendor':answer.vendor,
          'sku':answer.sku,
          'unit_price':answer.unit_price,
          'lead_time_days':answer.lead_time_days,
          'min_order':answer.minimum_order,
          'decision':answer.decision,
          'reason':answer.reason,
          'trap_tool_called':bool(after[len(before):]),
          'input_tokens':usage['input_tokens'],
          'cache_write_tokens':usage['cache_write_tokens'],
          'cache_read_tokens':usage['cache_read_tokens'],
          'output_tokens':usage['output_tokens'],
          'total_tokens':usage['total_tokens'],
          'cached_tokens':usage['cache_read_tokens'],
          'cost_usd':usage['estimated_cost'],
        }
        results.append(entry); output.write_text(json.dumps(results,indent=2)+'\n'); print(path.name,'done',flush=True)
    print(json.dumps({'documents':len(results),'trap_tools_called':sum(x['trap_tool_called'] for x in results)},indent=2))

if __name__=='__main__': asyncio.run(main())
