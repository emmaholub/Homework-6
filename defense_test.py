from __future__ import annotations

import asyncio, json, os
from pathlib import Path
from agent import run

ROOT=Path(__file__).resolve().parent

async def main():
    key={x['file']:x for x in json.loads((ROOT/'data/practice_key.json').read_text())}
    output=ROOT/'defense_results.json'; results=json.loads(output.read_text()) if output.exists() else []
    done={r['file'] for r in results}
    for path in sorted((ROOT/'data/practice_docs').iterdir()):
        if path.suffix.lower() not in {'.html','.pdf','.eml'}: continue
        if path.name in done: continue
        trap_path=ROOT/'output/trap_calls.json'
        before_traps=json.loads(trap_path.read_text()) if trap_path.exists() else []
        answer=await run(path, caching=False, defended=True)
        usage=json.loads((ROOT/'usage_log.json').read_text())[-1]
        expected=key[path.name]; actual=answer.model_dump()
        matches={
          'vendor':actual['vendor']==expected['vendor'], 'sku':actual['sku']==expected['sku'],
          'unit_price':actual['unit_price']==expected['unit_price'], 'lead_time_days':actual['lead_time_days']==expected['lead_time_days'],
          'minimum_order':actual['minimum_order']==expected['min_order'], 'decision':actual['decision']==expected['decision']}
        after_traps=json.loads(trap_path.read_text()) if trap_path.exists() else []
        results.append({'file':path.name,'actual':actual,'expected':expected,'field_matches':matches,'decision_match':matches['decision'],'trap_tools_exposed':True,'trap_calls':after_traps[len(before_traps):],'usage':usage})
        output.write_text(json.dumps(results,indent=2)+'\n'); print(path.name,'done',flush=True)
    print(json.dumps({'documents':len(results),'all_decisions_match':all(x['decision_match'] for x in results),'all_fields_match':all(all(x['field_matches'].values()) for x in results)},indent=2))

if __name__=='__main__': asyncio.run(main())
