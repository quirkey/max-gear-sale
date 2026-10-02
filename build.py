import json, html

photos = json.load(open('photos.json'))
R = "https://reverb.com/item/"

sections = [
  ("guitars", "Guitars", "Partscasters I assembled, finished and set up in the shop.", [
    ("esquire", "Esquire #04, Daphne Blue", 900, "Brand New", ["Solid body"],
     "The first Quint partscaster I put up for sale, built with premium parts and a full setup.",
     "81891009-quint-guitars-esquire-04-2023-daphne-blue"),
    ("jazzcaster", "Jazzcaster #07, Fiesta Red", 825, "Brand New", ["Solid body"],
     "A hand-finished partscaster with premium parts and a full setup.",
     "91230133-quint-guitars-07-jazzcaster-fiesta-red"),
  ]),
  ("pedals", "Pedals", "One original design plus Clone Lab builds: part-for-part clones on PedalPCB boards with through-hole parts.", [
    ("drivetrem", "Drive Trem", 175, "Brand New", ["Overdrive", "Tremolo"],
     "My own design: a JFET overdrive and a tremolo in one enclosure.",
     "97549430-quint-guitars-drive-trem-2026-black-woodgrain", True),
    ("datacorrupter", "Data Corrupter", 175, "Excellent", ["Fuzz", "Noise"],
     "Clone of the EQD Data Corrupter, a PLL square-wave fuzz that tracks into synth chaos.",
     "99865222-quint-guitars-clone-lab-data-corrupter"),
    ("riptide", "Riptide", 175, "Excellent", ["Reverb"],
     "Clone of the Scientific Guitarist Riptide, with a real Accutronics spring tank inside.",
     "99863494-quint-guitars-clone-lab-riptide"),
    ("organizer", "Organizer", 120, "Excellent", ["Pitch", "Vibrato"],
     "Clone of the EQD Organizer, an FV-1 organ emulator with pitch-shifted voices.",
     "99862807-quint-guitars-clone-lab-organizer"),
    ("warlow", "Warlow", 120, "Excellent", ["Distortion", "Fuzz"],
     "Clone of the JPTR FX Warlow: an op-amp Big Muff with extra gain and a 3-way tone switch.",
     "99862711-quint-guitars-clone-lab-warlow"),
    ("fuzzbender", "Fuzz Bender", 100, "Excellent", ["Fuzz", "Boost"],
     "Clone of the Keeley Fuzz Bender, a Tone Bender circuit mixing silicon and germanium.",
     "99862890-quint-guitars-clone-lab-fuzz-bender"),
    ("prince", "Prince of Tone", 90, "Excellent", ["Overdrive"],
     "Clone of the Analogman Prince of Tone, with a 3-way gain switch in a compact 1590B.",
     "99868106-quint-guitars-clone-lab-prince-of-tone"),
    ("breakup", "Breakup", 90, "Excellent", ["Overdrive", "Preamp"],
     "Clone of the Danelectro Breakdown, with a smooth pot in place of the rotary switch.",
     "94491814-quint-guitars-clone-lab-breakup"),
    ("levitation", "Levitation", 90, "Very Good", ["Reverb", "Delay"],
     "Clone of the EQD Levitation, an ambient reverb built on the Belton brick.",
     "99862655-quint-guitars-clone-lab-levitation"),
  ]),
]

e = html.escape
total = sum(i[2] for s in sections for i in s[3])
count = sum(len(s[3]) for s in sections)

def card(it):
    key, name, price, cond, tags, desc, slug = it[:7]
    orig = len(it) > 7
    badge = '<span class="badge">Original design</span>' if orig else ''
    tg = ''.join(f'<li>{e(t)}</li>' for t in tags)
    return f'''
      <article class="item">
        <a class="photo" href="{R}{slug}" target="_blank" rel="noopener" aria-label="{e(name)} on Reverb">
          <img src="{photos[key]}" alt="{e(name)}" loading="lazy" width="520" height="520">
          {badge}
        </a>
        <div class="body">
          <div class="row"><h3>{e(name)}</h3><p class="price">${price:,}</p></div>
          <p class="desc">{e(desc)}</p>
          <ul class="tags">{tg}</ul>
          <a class="buy" href="{R}{slug}" target="_blank" rel="noopener">More info on Reverb <span aria-hidden="true">&#8599;</span></a>
        </div>
      </article>'''

nav = ''.join(f'<a href="#{sid}">{e(t)} <span>{len(items)}</span></a>' for sid, t, _, items in sections)
secs = ''.join(f'''
  <section id="{sid}" class="cat">
    <header class="cat-head">
      <h2>{e(t)}</h2>
      <p>{e(blurb)}</p>
    </header>
    <div class="grid">{''.join(card(i) for i in items)}</div>
  </section>''' for sid, t, blurb, items in sections)

tpl = open('template.html').read()
out = tpl.replace('{{NAV}}', nav).replace('{{SECTIONS}}', secs).replace('{{COUNT}}', str(count)).replace('{{TOTAL}}', f'{total:,}')
open('index.html', 'w').write(out)
print(len(out), count, total)
