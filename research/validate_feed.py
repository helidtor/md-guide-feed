"""Validate the complete current feed against its declared active banlist."""
import collections, hashlib, json, pathlib, re, sys
sys.stdout.reconfigure(encoding='utf-8')
R=pathlib.Path(__file__).resolve().parent; ROOT=R.parent
def read(n): return json.loads((ROOT/n).read_text(encoding='utf-8-sig'))
decks=read('decks.json'); guides=read('guides.json'); ban=read('banlist.json'); m=read('manifest.json')
versions={x['dataVersion'] for x in [decks,guides,ban,m]}
assert len(versions)==1 and type(m['dataVersion']) is int and m['dataVersion']>=1
assert len(decks['decks'])==len(guides['guides'])==100
deck_ids=[d['id'] for d in decks['decks']]; guide_ids=[g['deckId'] for g in guides['guides']]
assert len(set(deck_ids))==100 and set(deck_ids)==set(guide_ids) and len(set(guide_ids))==100
assert [d['featuredRank'] for d in decks['decks']]==list(range(1,101))
for key,entry in m['files'].items():
    b=(ROOT/entry['url']).read_bytes()
    assert len(b)==entry['size'] and hashlib.sha256(b).hexdigest()==entry['sha256'],key
lookup={c['id']:c for c in json.loads((R/'cardinfo.json').read_text(encoding='utf-8'))['data']}
active_ids={d['banlist']['version'] for d in decks['decks']}
assert len(active_ids)==1,'mixed active banlists'
active=next(l for l in ban['lists'] if l['version'] in active_ids)
limits={e['cardId']:{'forbidden':0,'limited':1,'semi-limited':2,'unlimited':3}[e['status']] for e in active['entries']}
assert len(limits)==len(active['entries']),'duplicate banlist entries'
def norm(s): return re.sub(r'[<>]','',s).casefold()
by_id={d['id']:d for d in decks['decks']}
for d in decks['decks']:
    assert d['format']=='master-duel' and d['contentLanguage']=='vi'
    assert d['banlist']['effectiveDate']==active['effectiveDate'][:10],d['id']
    main=d['coreCards']+d['techCards']; extra=d['extraDeck']; allcards=main+extra
    assert 40<=sum(c['qty'] for c in main)<=60 and 0<=sum(c['qty'] for c in extra)<=15,d['id']
    count=collections.Counter()
    for c in allcards:
        assert type(c['qty']) is int and 1<=c['qty']<=3,(d['id'],c['name'])
        assert c['cardId'] in lookup,(d['id'],c['name'],'unknown card ID')
        assert norm(lookup[c['cardId']]['name'])==norm(c['name']),(d['id'],c['name'],'card name mismatch')
        is_extra=any(t in lookup[c['cardId']]['type'] for t in ['Fusion','Synchro','XYZ','Link'])
        assert is_extra==(c in extra),(d['id'],c['name'],'wrong zone')
        count[c['cardId']]+=c['qty']
    assert len(allcards)==len(count),(d['id'],'duplicate entry')
    assert all(q<=limits.get(i,3) for i,q in count.items()),(d['id'],'banlist limit exceeded')
for g in guides['guides']:
    d=by_id[g['deckId']]; pool={c['cardId'] for c in d['coreCards']+d['techCards']+d['extraDeck']}
    assert g['summary'] and g['strengths'] and g['weaknesses']
    assert all(g['playstyle'][k] for k in ['overview','goingFirst','goingSecond','tips'])
    for combo in g['combos']:
        assert combo['starterCardIds'] and combo['steps']
        assert [s['order'] for s in combo['steps']]==list(range(1,len(combo['steps'])+1))
        assert all(s['action'] in {'activate-card','activate-effect','fusion-summon','link-summon','normal-summon','other','ritual-summon','search','set','special-summon','synchro-summon','xyz-summon'} for s in combo['steps'])
        refs=combo['starterCardIds']+combo.get('deckCardIds',[])+combo.get('extraDeckCardIds',[])+combo['endBoard']['cardIds']+combo['endBoard'].get('graveyardCardIds',[])
        refs += [i for s in combo['steps'] for i in s['cardIds']]
        assert set(refs)<=pool,(g['deckId'],'missing combo card',set(refs)-pool)
        assert all(limits.get(i,3)>0 for i in refs),(g['deckId'],'forbidden combo card')
print(f'PASS: 100 unique decks / 100 unique guides; dataVersion={m["dataVersion"]}; active banlist={active["version"]}.')
print('PASS: all card IDs/names/zones, Main 40–60, Extra ≤15, combined copy limits and combo references.')
print('PASS: manifest SHA-256/size match exact bytes for every published data file.')
