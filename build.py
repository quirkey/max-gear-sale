import json, html, os, sys

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

REQUIRED = ('name', 'price', 'photo', 'tags', 'description', 'reverb')
OPTIONAL = ('original', 'condition')

def load_data():
    try:
        data = yaml.safe_load(open('items.yaml'))
    except yaml.YAMLError as err:
        sys.exit(f"items.yaml has a syntax error:\n{err}")
    errors = []
    for s in data['sections']:
        for k in ('id', 'title', 'blurb', 'items'):
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
            if 'photo' in it and it['photo'] not in photos:
                errors.append(f"{who}: no photo '{it['photo']}' in photos.json")
            if 'price' in it and not isinstance(it['price'], (int, float)):
                errors.append(f"{who}: price should be a number, got {it['price']!r}")
            if isinstance(it.get('tags'), str):
                it['tags'] = [it['tags']]
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
total = sum(i['price'] for s in sections for i in s['items'])
count = sum(len(s['items']) for s in sections)

def card(it):
    name, slug = it['name'], it['reverb']
    badge = '<span class="badge">Original design</span>' if it.get('original') else ''
    tg = ''.join(f'<li>{e(str(t))}</li>' for t in it['tags'])
    return f'''
      <article class="item">
        <a class="photo" href="{R}{slug}" target="_blank" rel="noopener" aria-label="{e(name)} on Reverb">
          <img src="{photos[it['photo']]}" alt="{e(name)}" loading="lazy" width="520" height="520">
          {badge}
        </a>
        <div class="body">
          <div class="row"><h3>{e(name)}</h3><p class="price">${it['price']:,}</p></div>
          <p class="desc">{e(it['description'])}</p>
          <ul class="tags">{tg}</ul>
          <a class="buy" href="{R}{slug}" target="_blank" rel="noopener">More info on Reverb <span aria-hidden="true">&#8599;</span></a>
        </div>
      </article>'''

nav = ''.join(f'<a href="#{s["id"]}">{e(s["title"])} <span>{len(s["items"])}</span></a>' for s in sections)
secs = ''.join(f'''
  <section id="{s['id']}" class="cat">
    <header class="cat-head">
      <h2>{e(s['title'])}</h2>
      <p>{e(s['blurb'])}</p>
    </header>
    <div class="grid">{''.join(card(i) for i in s['items'])}</div>
  </section>''' for s in sections)

max_photos = ''.join(f'<img src="{photos[p["photo"]]}" alt="{e(p["alt"])}" width="540" height="720">' for p in data.get('max_photos') or [])

tpl = open('template.html').read()
out = tpl.replace('{{NAV}}', nav).replace('{{SECTIONS}}', secs).replace('{{MAX_PHOTOS}}', max_photos).replace('{{INTRO}}', e(data['intro'].strip())).replace('{{COUNT}}', str(count)).replace('{{TOTAL}}', f'{total:,}')
open('index.html', 'w').write(out)
print(len(out), count, total)
