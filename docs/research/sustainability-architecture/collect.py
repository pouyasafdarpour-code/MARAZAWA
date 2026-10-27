"""Reproducible bibliographic collection; no full text, abstracts or client data."""
import csv, hashlib, html, json, re, time, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
CONTEXT = {
 'iran-architecture':r'architect|building|courtyard|vernacular|wind.?catch|\bthermal\b|passive|hous|urban|settlement',
 'sustainable-architecture':r'building|built environment|vernacular|architectural|architect.*(design|environment|sustainab|material)|sustainab.*architect',
 'community-participation':r'planning|design|urban|rural|settlement|housing|disaster|water|energy|land|regeneration',
 'social-sustainability':r'building|built environment|urban|rural|hous|architect|community|communit|planning|neighbo',
 'daylight':r'building|facade|façade|window|room|office|school|hous|atrium|indoor|architect|thermal|visual|lighting|daylighting design',
 'natural-ventilation':r'building|hous|room|indoor|school|office|thermal|cool|wind.?catch|passive|urban|atrium|ventilation',
 'timber-bamboo':r'building|construct|architect|structur|engineer|material|housing|timber frame|life.cycle',
 'low-carbon-materials':r'building|construct|material|cement|concrete|brick|timber|steel|bamboo|architect',
 'nature-based':r'urban|rural|communit|settlement|water|flood|climat|resilien|infrastructure|nature.based',
 'building-economics':r'building|construct|hous|retrofit|architect|energy|green roof|facade|façade',
}
TOPICS = [
 ('sustainable-development','توسعهٔ پایدار','sustainable development',r'sustainab.*develop|sustainable development'),
 ('rural-development','توسعهٔ روستایی پایدار','sustainable rural development',r'rural.*sustainab|sustainab.*rural'),
 ('community-participation','مشارکت و طراحی با مردم','participatory community planning',r'participat|co.design|community.*planning'),
 ('sustainable-livelihoods','معیشت و اقتصاد محلی','sustainable livelihoods rural',r'livelihood|rural.*econom|local.*econom'),
 ('social-sustainability','عدالت و پایداری اجتماعی','social sustainability built environment',r'social.*sustainab|sustainab.*social'),
 ('sustainable-architecture','معماری پایدار','sustainable architecture',r'sustainab.*architect|architect.*sustainab'),
 ('vernacular-architecture','معماری بومی و اقلیمی','vernacular architecture climate',r'vernacular|traditional.*architect'),
 ('iran-architecture','معماری و اقلیم ایران','Iran traditional architecture sustainable',r'iran|persian'),
 ('passive-design','طراحی غیرفعال و اقلیم','passive building design',r'passive.*(design|building|cool|heat|solar)|bioclimatic'),
 ('thermal-comfort','آسایش حرارتی','adaptive thermal comfort buildings',r'thermal comfort'),
 ('natural-ventilation','تهویهٔ طبیعی','natural ventilation buildings',r'natural ventilation|windcatch|wind.catch'),
 ('daylight','نور روز و روشنایی','daylighting buildings',r'daylight'),
 ('building-energy','انرژی ساختمان','building energy efficiency',r'building.*energ|energ.*building'),
 ('net-zero','ساختمان کم‌مصرف و صفرخالص','net zero energy buildings',r'zero.*(energ|carbon|emission)|positive.energy'),
 ('retrofit','بهسازی انرژی و احیای بنا','building energy retrofit',r'retrofit|refurbish|renovat'),
 ('adaptive-reuse','بازاستفادهٔ تطبیقی','adaptive reuse buildings',r'adaptive re.?use|building re.?use'),
 ('life-cycle-assessment','ارزیابی چرخهٔ عمر','life cycle assessment buildings',r'life.cycle.*(assess|building)|building.*life.cycle'),
 ('embodied-carbon','کربن نهفته','embodied carbon buildings',r'embodied.*(carbon|energ)|whole.life carbon'),
 ('circular-construction','ساخت‌وساز چرخشی','circular economy construction',r'circular.*(econom|construct|building)|deconstruct|design for disassembly'),
 ('construction-waste','پسماند و بازیافت ساختمانی','construction demolition waste recycling',r'construct.*waste|demolition.*waste'),
 ('earth-materials','خاک و مصالح بومی','rammed earth adobe sustainable construction',r'rammed earth|adobe|earth.*construct|earthen'),
 ('timber-bamboo','چوب و بامبو','timber bamboo sustainable buildings',r'timber|bamboo|wood.*construct'),
 ('low-carbon-materials','مصالح کم‌کربن','low carbon building materials',r'low.carbon|sustainab.*material|material.*sustainab'),
 ('water','آب و بازچرخانی','rainwater harvesting greywater buildings',r'rainwater|greywater|graywater|water.*reus'),
 ('green-roofs','بام و جدارهٔ سبز','green roofs walls buildings',r'green roof|green wall|living wall'),
 ('nature-based','راهکارهای مبتنی بر طبیعت','nature based solutions urban resilience',r'nature.based|green infrastructure'),
 ('urban-heat','گرما و سایه در سکونتگاه','urban heat island mitigation',r'urban heat|heat island|urban.*cool'),
 ('climate-resilience','تاب‌آوری اقلیمی بنا و سکونتگاه','climate resilience buildings settlements',r'climat.*resilien|resilien.*climat|flood.*resilien'),
 ('healthy-buildings','سلامت و کیفیت محیط داخلی','indoor environmental quality healthy buildings',r'indoor.*(quality|environment|air)|healthy building'),
 ('affordable-housing','مسکن استطاعت‌پذیر و پایدار','sustainable affordable housing',r'affordable hous|housing affordab|social housing'),
 ('building-economics','هزینهٔ چرخهٔ عمر و توجیه اقتصادی','life cycle costing sustainable buildings',r'life.cycle cost|economic.*(building|retrofit)|building.*economic'),
 ('post-occupancy','ارزیابی پس از بهره‌برداری','post occupancy evaluation buildings',r'post.occupancy|building performance evaluation'),
 ('renewable-energy','انرژی تجدیدپذیر محلی','renewable energy rural communities',r'rural|community.*energ|energ.*communit'),
 ('sustainable-mobility','دسترسی و جابه‌جایی پایدار','sustainable mobility accessibility settlements',r'sustainab.*(mobil|transport)|accessib'),
 ('cultural-heritage','میراث و بازآفرینی پایدار','cultural heritage sustainable regeneration',r'heritage|regenerat'),
 ('sdg-measurement','سنجش و شاخص‌های توسعه','sustainable development goals indicators',r'sustainable development goal|sdg|sustainab.*indicator'),
]

def clean(v):
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', str(v)))).strip()

def fetch(url):
    for attempt in range(4):
        try:
            req=urllib.request.Request(url, headers={'User-Agent':'MARAZAWA-ResearchLibrary/1.0 (public bibliography; metadata only)'})
            with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)
        except Exception:
            if attempt==3: raise
            time.sleep(2*(attempt+1))

def collect():
    cache=ROOT/'_cache';cache.mkdir(exist_ok=True)
    records={}; logs=[]; excluded={}; now=datetime.now(timezone.utc).isoformat()
    for slug, fa, query, pattern in TOPICS:
        params={'query.title':query,'rows':250,'filter':'type:journal-article,until-pub-date:2026-10-27','select':'DOI,title,author,publisher,container-title,published,ISSN,is-referenced-by-count,license,link,update-to,relation','sort':'relevance'}
        url='https://api.crossref.org/works?'+urllib.parse.urlencode(params)
        path=cache/(slug+'.json')
        if path.exists(): data=json.loads(path.read_text(encoding='utf-8'))
        else:
            data=fetch(url);path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');time.sleep(1)
        items=data['message']['items']; accepted=[]; rejected=0
        for rank,x in enumerate(items,1):
            title=clean((x.get('title') or [''])[0]);doi=x.get('DOI','').lower().strip()
            updates=x.get('update-to',[])
            context_ok=slug not in CONTEXT or re.search(CONTEXT[slug],title,re.I)
            off_topic=re.search(r'pursuing happiness|software architecture|service.oriented architecture|neural architecture|hardware architecture|cloud architecture|blockchain.based architecture|microprocessor',title,re.I)
            if not doi or not title or not context_ok or off_topic or not re.search(pattern,title,re.I) or re.search(r'^(retraction|withdrawal|corrigendum|erratum|correction)\b',title,re.I) or any(u.get('type') in ['retraction','withdrawal'] for u in updates):
                rejected+=1;continue
            accepted.append((rank,x,title,doi))
        # Keep a reproducible mixture of query relevance, cited literature and recent work.
        picked=accepted[:65]
        cited=sorted(accepted,key=lambda z:z[1].get('is-referenced-by-count',0),reverse=True)[:25]
        recent=sorted(accepted,key=lambda z:z[1].get('published',{}).get('date-parts',[[0]])[0],reverse=True)[:20]
        seen=set()
        for rank,x,title,doi in picked+cited+recent:
            if doi in seen:continue
            seen.add(doi)
            if doi not in records:
                date=x.get('published',{}).get('date-parts',[[]])[0]
                licenses=sorted({v['URL'] for v in x.get('license',[]) if v.get('URL')})
                records[doi]={'doi':doi,'title':title,'authors':[clean(' '.join([a.get('given',''),a.get('family','')])) for a in x.get('author',[]) if a.get('given') or a.get('family')],'year':date[0] if date else None,'journal':clean((x.get('container-title') or [''])[0]),'publisher':clean(x.get('publisher','')),'issn':x.get('ISSN',[]),'url':'https://doi.org/'+doi,'citation_count_crossref':x.get('is-referenced-by-count',0),'license_urls_deposited':licenses,'full_text_archived':False,'full_text_reviewed':False,'verification':'publisher_deposited_metadata; title_screened; not_full_text_reviewed','topics':[],'discovered_by':[],'retrieved_at':now}
            r=records[doi];r['topics'].append(slug);r['discovered_by'].append({'query':query,'rank':rank})
        logs.append({'topic':slug,'query':query,'url':url,'returned':len(items),'title_matched':len(accepted),'selected_in_topic':len(seen),'rejected':rejected,'retrieved_at':now})
        print(f'{slug}: {len(seen)} selected; {len(records)} unique total',flush=True)
    ordered=sorted(records.values(),key=lambda r:(r['topics'][0],-r['citation_count_crossref'],r['doi']))
    titlekeys={}; duplicate_titles=[]
    for r in ordered:
        key=re.sub(r'\W+','',r['title'].casefold())
        if key in titlekeys: duplicate_titles.append({'title':r['title'],'doi':r['doi'],'same_title_doi':titlekeys[key]})
        else:titlekeys[key]=r['doi']
    # Deduplicate identical normalized titles, retaining the more cited record.
    keep={}
    for r in sorted(ordered,key=lambda r:-r['citation_count_crossref']):
        key=re.sub(r'\W+','',r['title'].casefold());keep.setdefault(key,r)
    ordered=sorted(keep.values(),key=lambda r:(r['topics'][0],-r['citation_count_crossref'],r['doi']))
    for i,r in enumerate(ordered,1):r['id']=f'SA-{i:04d}';r['topics']=sorted(set(r['topics']))
    (ROOT/'catalog.json').write_text(json.dumps({'schema_version':1,'generated_at':now,'scope':'Public bibliographic metadata, not a reviewed evidence base','sources':ordered},ensure_ascii=False,indent=2),encoding='utf-8')
    with (ROOT/'catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['id','title','year','journal','publisher','authors','doi','url','topics','citation_count_crossref','license_urls_deposited','verification'])
        for r in ordered:w.writerow([r['id'],r['title'],r['year'],r['journal'],r['publisher'],'; '.join(r['authors']),r['doi'],r['url'],';'.join(r['topics']),r['citation_count_crossref'],';'.join(r['license_urls_deposited']),r['verification']])
    report={'generated_at':now,'count':len(ordered),'unique_dois':len({r['doi'] for r in ordered}),'title_duplicates_removed':len(duplicate_titles),'full_text_read_count':0,'queries':logs,'topic_counts':{slug:sum(slug in r['topics'] for r in ordered) for slug,*_ in TOPICS},'limitations':['Crossref registration does not prove peer review or correctness.','Title relevance is screened automatically; full text has not been read.','Citation counts are incomplete, time-dependent and not quality scores.','License URLs are publisher deposits, not a verified permission grant.','Retraction screening is limited to metadata returned in this snapshot.']}
    (ROOT/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('FINAL',len(ordered),flush=True)

if __name__=='__main__':collect()
