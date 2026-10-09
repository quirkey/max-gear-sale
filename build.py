import json, html, os, re, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

try:
    import yaml
except ImportError:
    # PyYAML lives in the project venv; re-run under it so `python3 build.py` just works.
    venv = os.path.join(HERE, '.venv')
    venv_py = os.path.join(venv, 'bin', 'python')
    if os.path.exists(venv_py) and os.path.realpath(sys.prefix) != os.path.realpath(venv):
        os.execv(venv_py, [venv_py, *sys.argv])
    sys.exit("PyYAML is missing. Run: python3 -m venv .venv && .venv/bin/pip install pyyaml")

photos = json.load(open('photos.json'))
R = "https://reverb.com/item/"
EMAIL = "aaron@quirkey.com"  # for items with no listing link

REQUIRED = ('name', 'price', 'photo', 'tags', 'description')
OPTIONAL = ('reverb', 'url', 'original', 'condition')

def load_data():
    try:
        data = yaml.safe_load(open('items.yaml'))
    except yaml.YAMLError as err:
        sys.exit(f"items.yaml has a syntax error:\n{err}")
    errors = []
    for s in data['sections']:
        for k in ('id', 'title', 'blurb', 'items'):  # plus optional 'more'
            if k not in s:
                errors.append(f"section {s.get('id') or s.get('title') or '?'}: missing '{k}'")
        for it in s.get('items') or []:
            who = it.get('name') or '(unnamed item)'
            for k in REQUIRED:
                if it.get(k) in (None, ''):
                    errors.append(f"{who}: missing '{k}'")
            for k in it:
                if k not in REQUIRED + OPTIONAL:
                    errors.append(f"{who}: unknown field '{k}' (typo?)")
            if it.get('reverb') and it.get('url'):
                errors.append(f"{who}: has both 'reverb' and 'url'; keep one")
            if 'photo' in it and it['photo'] not in photos:
                errors.append(f"{who}: no photo '{it['photo']}' in photos.json")
            if 'price' in it and not isinstance(it['price'], (int, float)):
                errors.append(f"{who}: price should be a number, got {it['price']!r}")
            if isinstance(it.get('tags'), str):
                it['tags'] = [it['tags']]
        more = s.get('more')
        if more:
            where = f"{s.get('id')} 'more'"
            for k in ('title', 'photo', 'alt', 'note'):
                if not more.get(k):
                    errors.append(f"{where}: missing '{k}'")
            if more.get('photo') and more['photo'] not in photos:
                errors.append(f"{where}: no photo '{more['photo']}' in photos.json")
            # Each list entry is a name, or {name, price}; normalize to dicts.
            entries = []
            for x in more.get('list') or []:
                x = {'name': x} if isinstance(x, str) else x
                if not isinstance(x, dict) or not x.get('name'):
                    errors.append(f"{where}: list entry {x!r} needs a name")
                    continue
                if x.get('price') is not None and not isinstance(x['price'], (int, float)):
                    errors.append(f"{where}: {x['name']}: price should be a number, got {x['price']!r}")
                entries.append(x)
            more['list'] = entries
    for p in data.get('max_photos') or []:
        if p.get('photo') not in photos:
            errors.append(f"max_photos: no photo '{p.get('photo')}' in photos.json")
        if not p.get('alt'):
            errors.append(f"max_photos: '{p.get('photo')}' is missing 'alt'")
    if not data.get('intro'):
        errors.append("missing 'intro' (the paragraph under the page title)")
    if errors:
        sys.exit("items.yaml problems:\n  " + "\n  ".join(errors))
    return data

data = load_data()
sections = data['sections']

e = html.escape

def linkify(text):
    # Escape plain text, then turn Markdown-style [text](url) into links.
    # mailto: links open in the same tab; web links open in a new one.
    def a(m):
        label, url = m.group(1), m.group(2)
        ext = '' if url.startswith('mailto:') else ' target="_blank" rel="noopener"'
        return f'<a href="{url}"{ext}>{label}</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', a, e(text))
def extras(s):
    return (s.get('more') or {}).get('list') or []

total = sum(i['price'] for s in sections for i in s['items']) + sum(x.get('price') or 0 for s in sections for x in extras(s))
count = sum(len(s['items']) + len(extras(s)) for s in sections)

def card(it):
    name = it['name']
    badge = '<span class="badge">Original design</span>' if it.get('original') else ''
    img = f'<img src="{photos[it['photo']]}" alt="{e(name)}" loading="lazy" width="520" height="520">{badge}'
    if it.get('reverb') or it.get('url'):
        href = R + it['reverb'] if it.get('reverb') else it['url']
        site = 'Reverb' if it.get('reverb') else re.sub(r'^www\.', '', re.sub(r'^\w+://', '', href).split('/')[0])
        photo = f'<a class="photo" href="{e(href)}" target="_blank" rel="noopener" aria-label="{e(name)} on {e(site)}">{img}</a>'
        button = f'<a class="buy" href="{e(href)}" target="_blank" rel="noopener">More info on {e(site)} <span aria-hidden="true">&#8599;</span></a>'
    else:
        # No listing to link to: the photo isn't a link and the button opens an email about the item.
        photo = f'<div class="photo">{img}</div>'
        button = f'<a class="buy" href="mailto:{EMAIL}?subject={quote(name)}">Email me about this</a>'
    tg = ''.join(f'<li>{e(str(t))}</li>' for t in it['tags'])
    return f'''
      <article class="item">
        {photo}
        <div class="body">
          <div class="row"><h3>{e(name)}</h3><p class="price">${it['price']:,}</p></div>
          <p class="desc">{e(it['description'])}</p>
          <ul class="tags">{tg}</ul>
          {button}
        </div>
      </article>'''

def more_block(s):
    m = s.get('more')
    if not m:
        return ''
    rows = ''.join(f'<li><span>{e(x["name"])}</span>' + (f'<span class="price">${x["price"]:,}</span>' if x.get('price') is not None else '') + '</li>' for x in m['list'])
    return f'''
    <div class="more">
      <img src="{photos[m['photo']]}" alt="{e(m['alt'])}" loading="lazy">
      <div class="more-body">
        <h3>{e(m['title'])}</h3>
        <p class="desc">{linkify(m['note'])}</p>
        {f'<ul class="more-list">{rows}</ul>' if rows else ''}
        <a class="buy" href="mailto:{EMAIL}?subject={quote(m['title'])}">Email me about these</a>
      </div>
    </div>'''

nav = ''.join(f'<a href="#{s["id"]}">{e(s["title"])} <span>{len(s["items"]) + len(extras(s))}</span></a>' for s in sections)
secs = ''.join(f'''
  <section id="{s['id']}" class="cat">
    <header class="cat-head">
      <h2>{e(s['title'])}</h2>
      <p>{e(s['blurb'])}</p>
    </header>
    <div class="grid">{''.join(card(i) for i in s['items'])}</div>{more_block(s)}
  </section>''' for s in sections)

max_photos = ''.join(f'<img src="{photos[p["photo"]]}" alt="{e(p["alt"])}" width="540" height="720">' for p in data.get('max_photos') or [])

tpl = open('template.html').read()
out = tpl.replace('{{NAV}}', nav).replace('{{SECTIONS}}', secs).replace('{{MAX_PHOTOS}}', max_photos).replace('{{INTRO}}', ''.join(f'<p>{linkify(p.strip())}</p>' for p in data['intro'].strip().split('\n') if p.strip())).replace('{{COUNT}}', str(count)).replace('{{TOTAL}}', f'{total:,}')
open('index.html', 'w').write(out)
print(len(out), count, total)
