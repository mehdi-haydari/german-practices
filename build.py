from pathlib import Path
from html import escape
import json
import os

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
DATA=json.loads((ROOT/'practices.json').read_text())
DIST.mkdir(exist_ok=True)
BASE_PATH=os.environ.get('SITE_BASE_PATH','').rstrip('/')

LESSON={
    9:{'title':'Warum rufst du nicht an?','printed':'69–76','pdf':'9–16','summary':'Communication, messages, invitations, and replies.'}
}
def e(value): return escape(str(value),quote=True)
def path(p): return BASE_PATH + (p if p.startswith('/') else '/' + p)
def url(p): return path(f'/practice/{p}/')
def date(p): return '31 October 2026' if p=='2026-10-31' else '7 November 2026'
def badge(p):
    label={'reviewed':'Reviewed','guided':'Guided practice','model':'Teacher example'}[p['status']]
    return f'<span class="badge {p["status"]}">{label}</span>'
def shell(title,body,description):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(description)}"><meta name="theme-color" content="#285b49"><title>{e(title)} · Deutsch A2</title>
<link rel="icon" href="{path('/favicon.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{path('/styles.css')}"><script defer src="{path('/app.js')}"></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="topbar"><div class="wrap">
<a class="brand" href="{path('/')}" aria-label="Deutsch A2 lesson index"><span class="brandmark" aria-hidden="true">A₂</span><span>Deutsch, Schritt für Schritt<small>My practice journal</small></span></a>
<nav class="topnav" aria-label="Main navigation"><a href="{path('/')}">Lesson index</a><button class="button" data-print type="button">Print / save PDF</button></nav></div></header>
{body}<footer class="footer"><div class="wrap"><span>Deutsch A2 · MOTIVE</span><span>Original answers preserved. Learning in progress.</span></div></footer>
<div id="announcement" class="live" role="status" aria-live="polite"></div></body></html>'''

def practice_records():
    opening=[p for p in DATA if p['group']=='Opening']
    c2=[p for p in DATA if p['group'] in ('A','B')]
    out=[]
    if opening: out.append({'id':'lesson-09-opening','code':'Opening','title':'Staying in touch','description':'A short opening question about keeping in contact.','records':opening,'count':len(opening)})
    if c2: out.append({'id':'lesson-09-c2a','code':'C2.a','title':'Invitations and guests','description':'Fragen A and B: personal answers about invitations, guests, and preparations.','records':c2,'count':len(c2)})
    return out
PRACTICES=practice_records()

def record_card(x):
    return f'''<a class="practice-card compact" href="{url(x['id'])}"><div class="card-meta"><span class="ref">Lesson 9 → {e(x['code'])}</span><span>{x['count']} question{'s' if x['count']!=1 else ''}</span></div><h3>{e(x['title'])}</h3><p>{e(x['description'])}</p><div class="card-footer"><span class="badge reviewed">Practice page</span><span class="view">Open all questions <span aria-hidden="true">↗</span></span></div></a>'''

lesson_index=f'''<main id="main" class="wrap"><section class="hero index-hero"><div><div class="eyebrow">A2 / A growing notebook</div><h1 id="page-title">My German<br>practice.</h1><p class="intro">A simple record of the lessons we have practised together. Open a lesson to find its practice pages, answers, and feedback.</p><div class="hero-actions"><a class="button primary" href="{path('/lesson/9/')}">Open lesson 9 <span aria-hidden="true">→</span></a></div></div><aside class="lesson-note"><div class="eyebrow">Current book lesson</div><h2 lang="de">Warum rufst du<br>nicht an?</h2><p>MOTIVE A2 · Lesson 9<br>{e(LESSON[9]['summary'])}</p><div class="note-bottom"><span>Written practice</span><span>Growing week by week</span></div></aside></section>
<section class="lesson-list" aria-labelledby="lessons-title"><div class="section-title"><h2 id="lessons-title">Lessons we’ve practised</h2><span class="result-count">{len(LESSON)} lesson</span></div><div class="card-grid">{''.join(f'''<a class="practice-card lesson-card" href="{path(f'/lesson/{n}/')}"><div class="card-meta"><span class="ref">MOTIVE A2 · Lesson {n}</span><span>Printed pages {e(v['printed'])}</span></div><h3 lang="de">{e(v['title'])}</h3><p>{e(v['summary'])}</p><div class="card-footer"><span class="badge reviewed">{len([x for x in PRACTICES if x['id'].startswith(f'lesson-{n:02d}-')])} practice pages</span><span class="view">Open lesson <span aria-hidden="true">↗</span></span></div></a>''' for n,v in LESSON.items())}</div></section>
<aside class="teacher-note"><div><div class="eyebrow">For my teacher</div><h2>Answers with their learning context.</h2></div><div><p>Practice pages keep my original wording, corrected teacher models, and explanations together. Follow-up answers are labelled so they are not confused with independent answers.</p><p>These are short written samples. They do not establish retained mastery, listening ability, pronunciation, speaking fluency, or an overall CEFR level.</p></div></aside></main>'''
(DIST/'index.html').write_text(shell('Lesson index',lesson_index,'Index of MOTIVE A2 lessons practised with German answers and feedback.'),encoding='utf-8')

for n,meta in LESSON.items():
    entries=[x for x in PRACTICES if x['id'].startswith(f'lesson-{n:02d}-')]
    listing=f'''<main id="main" class="wrap"><nav class="breadcrumbs"><a href="{path('/')}">Lesson index</a><span aria-hidden="true">/</span><span>Lesson {n}</span></nav>
<header class="lesson-header"><div class="eyebrow">MOTIVE A2 · Book lesson {n}</div><h1 lang="de">{e(meta['title'])}</h1><p>{e(meta['summary'])}</p><div class="lesson-facts"><span>Printed pages {e(meta['printed'])}</span><span>PDF pages {e(meta['pdf'])}</span><span>{len(entries)} practice pages</span></div></header>
<section aria-labelledby="practice-pages-title"><div class="section-title"><h2 id="practice-pages-title">Practices in this lesson</h2><span class="result-count">Choose a practice</span></div><div class="card-grid">{''.join(record_card(x) for x in entries)}</div></section>
<p class="back-row"><a href="{path('/')}">← Back to all lessons</a></p></main>'''
    target=DIST/'lesson'/str(n);target.mkdir(parents=True,exist_ok=True)
    (target/'index.html').write_text(shell(f'Lesson {n}',listing,f'Practice pages for MOTIVE A2 lesson {n}, {meta["title"]}.'),encoding='utf-8')

for practice in PRACTICES:
    records=practice['records']; is_c2=practice['code']=='C2.a'
    sections=[]
    for group in (['A','B'] if is_c2 else ['Opening']):
        subset=[p for p in records if p['group']==group]
        if not subset: continue
        section_title={'A':'Fragen A','B':'Fragen B','Opening':'Opening question'}[group]
        cards=[]
        for p in subset:
            ref=p['ref'].split(' · ')[-1] if ' · ' in p['ref'] else 'opening'
            anchor=ref.lower().replace('.','-')
            prompt=(p['original'] if p['original'] is not None else '')
            raw=f'<div class="learner-answer"><div class="box-label">Your answer</div><blockquote lang="de">{e(p["original"])}</blockquote></div>' if p['original'] is not None else '<div class="learner-answer model-info"><div class="box-label">Your answer</div><p>No independent answer submitted; a teacher example is shown.</p></div>'
            strengths='<div class="good"><h4>What worked</h4>'+''.join(f'<p>{e(s)}</p>' for s in p['strengths'])+'</div>' if p['strengths'] else ''
            analysis=''.join(f'<li>{e(t)}</li>' for t in p['analysis'])
            clarifications=''.join(f'<div class="clarification"><h4>Meaning clarified by the learner</h4><blockquote>{e(c["answer"])}</blockquote><p>{e(c["explanation"])}</p></div>' for c in p.get('clarifications',[]))
            alternatives=''.join(f'<div class="alternative"><h4>{e(a["label"])}</h4><p class="de" lang="de">{e(a["text"])}</p></div>' for a in p.get('alternatives',[]))
            attempts=[]
            for a in p['attempts']:
                outcome='Successful guided step' if a['result']=='correct' else 'More practice needed'
                fixed=f'<p class="fixed" lang="de"><strong>Teacher correction:</strong> {e(a["corrected"])}</p>' if a.get('corrected') else ''
                attempts.append(f'<div class="attempt"><div class="attempt-header"><strong>{e(a["kind"])}</strong><span class="badge {"guided" if a["result"]=="correct" else "model"}">{outcome}</span></div><p class="prompt" lang="de">{e(a["prompt"])}</p><p class="raw" lang="de">{e(a["answer"])}</p>{fixed}<p class="explain">{e(a["feedback"])}</p></div>')
            attempt_block=f'<details class="attempts" open><summary>Follow-up attempts ({len(attempts)})</summary>{"".join(attempts)}</details>' if attempts else ''
            note=f'<p class="context-note">{e(p["note"])}</p>' if p.get('note') else ''
            cards.append(f'''<article class="question-review" id="{e(anchor)}"><div class="question-title"><span class="ref">{e(p['ref'])}</span>{badge(p)}</div><h3 lang="de">{e(p['question'])}</h3><p class="translation">{e(p['translation'])}</p><div class="answer-pair"><section class="answer-box original">{raw}</section><section class="answer-box corrected"><div class="box-label">{'Teacher example' if p['status']=='model' else 'Corrected answer'}</div><blockquote lang="de">{e(p['corrected'])}</blockquote><p class="meaning">{e(p['meaning'])}</p></section></div>{clarifications}{strengths}<div class="feedback"><h4>Analysis</h4><ol>{analysis}</ol></div>{alternatives}{attempt_block}{note}</article>''')
        sections.append(f'<section class="question-set" aria-labelledby="set-{group}"><div class="section-title"><h2 id="set-{group}">{section_title}</h2><span class="result-count">{len(subset)} questions</span></div>{"".join(cards)}</section>')
    lesson_title=LESSON[9]['title']
    body=f'''<main id="main" class="wrap"><nav class="breadcrumbs"><a href="{path('/')}">Lesson index</a><span aria-hidden="true">/</span><a href="{path('/lesson/9/')}">Lesson 9</a><span aria-hidden="true">/</span><span>{e(practice['code'])}</span></nav>
<header class="practice-header"><div class="eyebrow">Lesson 9 · {e(practice['code'])}</div><h1>{e(practice['title'])}</h1><p>{e(practice['description'])}</p><div class="hero-actions"><a class="button" href="{path('/lesson/9/')}">← All Lesson 9 practices</a><button class="button" data-copy-link="{url(practice['id'])}" type="button">Copy practice link ↗</button></div></header>
<div class="practice-intro"><p>All questions, your original answers, teacher corrections, and explanations for this practice are collected here.</p><span class="muted">MOTIVE A2 · printed page 75</span></div>{''.join(sections)}
<nav class="sequence"><a href="{path('/lesson/9/')}"><small>Back to this lesson</small>← Lesson 9 practices</a><a href="{path('/')}"><small>All lessons</small>Lesson index →</a></nav></main>'''
    target=DIST/'practice'/practice['id'];target.mkdir(parents=True,exist_ok=True)
    (target/'index.html').write_text(shell(f'Lesson 9 {practice["code"]} · {practice["title"]}',body,f'All answers and feedback for MOTIVE A2 lesson 9 {practice["code"]}.'),encoding='utf-8')

# Preserve the original per-question URLs as links into the combined C2.a page.
for p in DATA:
    if p['group'] not in ('A','B'): continue
    part=p['ref'].split(' · ')[-1].lower().replace('.','-')
    href=path(f'/practice/lesson-09-c2a/#{part}')
    target=DIST/'practice'/p['id'];target.mkdir(parents=True,exist_ok=True)
    (target/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={href}"><link rel="canonical" href="{href}"><title>Moved to the full C2.a practice</title></head><body><p>This question is now part of the complete <a href="{href}">Lesson 9 · C2.a practice page</a>.</p></body></html>''',encoding='utf-8')

for file in ['styles.css','app.js']:
    (DIST/file).write_text((ROOT/file).read_text(),encoding='utf-8')
(DIST/'CNAME').write_text('german-practices.mehdiheydari.dev\n',encoding='utf-8')
(DIST/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#285b49"/><text x="14" y="45" font-family="Georgia,serif" font-size="40" fill="#fffefa">A₂</text></svg>')
(DIST/'404.html').write_text(shell('Practice not found',f'<main id="main" class="wrap" style="padding-top:70px;padding-bottom:100px"><div class="eyebrow">This page is not in the notebook</div><h1>Let’s find your practice.</h1><p>The lesson index has all lessons we have practised.</p><a class="button primary" href="{path('/')}">Go to the lesson index</a></main>','Find your German lesson in the journal index.'),encoding='utf-8')
(DIST/'.nojekyll').write_text('',encoding='utf-8')
print(f'Built a lesson index, {len(LESSON)} lesson pages, {len(PRACTICES)} grouped practice pages, legacy redirects, and a 404 page.')
