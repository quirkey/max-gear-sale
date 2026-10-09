# Max's Surgery Gear Sale

A one-page static site listing gear from Aaron's Quint Guitars Reverb shop (https://reverb.com/shop/quint-guitars). The sale raises money for his cat Max's surgery. The shop is based in Kingston, NY.

## Files
- `index.html`: generated output and the deliverable. It's self-contained, with photos embedded as base64 data URIs (~400KB). Don't hand-edit it; edit the sources and rebuild.
- `items.yaml`: all listing data, meant for Aaron to edit by hand. Sections (`id`, `title`, `blurb`, `items`) and items (`name`, `price`, `photo`, `tags`, `description`, and either `reverb` (a listing slug) or `url` (a full link for items not on Reverb), plus optional `original: true` for the "Original design" badge and `condition`). The header comment documents the fields. The link URL is `https://reverb.com/item/<reverb>` and the button reads "More info on Reverb". An item with `url` gets "More info on <domain>" instead. An item with neither gets an "Email me about this" `mailto:` button (`EMAIL` in build.py, with the item name as the subject), and its photo isn't a link. Strings are quoted because names like "Esquire #04" would otherwise be cut off at `#` as a YAML comment.
- `build.py`: the generator. It reads `items.yaml`, validates it (missing or unknown fields, a photo key not in `photos.json`, a non-numeric price) and writes `index.html`. PyYAML lives in a gitignored `.venv`. If `yaml` can't be imported, build.py re-runs itself under `.venv/bin/python`, so plain `python3 build.py` works. To recreate the venv: `python3 -m venv .venv && .venv/bin/pip install pyyaml`.
- `template.html`: layout and CSS. Contains the placeholders `{{NAV}}`, `{{SECTIONS}}`, `{{INTRO}}`, `{{MAX_PHOTOS}}` and `{{COUNT}}`. It starts with a real document head (`<!doctype>`, charset, viewport, description), which the page needs now that it's hosted on its own rather than as an artifact. (`{{TOTAL}}` is still filled by build.py but the template no longer uses it.)
- `photos.json`: `{photo_key: "data:image/jpeg;base64,..."}`. Listing photos are JPEGs at 520px max and quality 0.72. The four `max-*` keys are photos of Max for the header, at 540×720 and quality 72. The originals were `~/Downloads/IMG_{4503,5162,6686,3846 2} Large.jpeg`.
- `max_photos` in `items.yaml` lists the header photos of Max (`photo` key and `alt` text) in display order. They render as a staggered 2×2 grid in a 480px column beside the intro on screens 820px and wider, as a row of four below the intro between 560 and 819px, and as a 2×2 grid below 560px.
- A section can have an optional `more:` block (`title`, `photo`, `alt`, `note`, `list`), rendered under its cards as a wide photo next to a plain list and an "Email me about these" button. Pedals uses it with `wall-of-pedals`, a photo of Aaron's pedal shelves. It's cropped to remove framed family photos on the right, including one of a child, so keep that crop if you re-export it. Aaron fills `list` himself. Entries are a name string or `{ name, price }`, and they count toward the header and nav item counts. Don't try to identify the pedals in the photo.
- `intro` in `items.yaml` is the text under the page title, written by Aaron as a YAML folded block (`>`). A blank line starts a new `<p>`. Text is HTML-escaped, then Markdown-style `[text](url)` becomes a link (`mailto:` links open in the same tab, web links in a new one). It links Instagram (@quirkey) and aaron@quirkey.com because Aaron prefers direct sales (Venmo or PayPal) to avoid Reverb fees.
- **Strip metadata from any personal photo before embedding.** Aaron's iPhone photos carry GPS coordinates for his home. Re-encode them with Pillow (in `.venv`), which drops EXIF, as was done for the Max photos.
- `img/`: empty and unused.

## Build
    python3 build.py   # writes index.html, prints size / item count / total $

## Deploy
GitHub Pages from the `main` branch root of https://github.com/quirkey/max-gear-sale. Live at https://quirkey.github.io/max-gear-sale/. To update: edit `items.yaml`, `python3 build.py`, commit, `git push`. Pages rebuilds in about a minute.

## Content decisions (from Aaron)
- Categories: Guitars, Amps, Pedals. (Amps added 2026-10-09: Vox AC30 $400 and Fender Hot Rod Deluxe $300, photos from `~/Downloads/vox-ac-30.jpeg` (square crop, shifted left so the logo isn't clipped) and `fender-amp-front.jpeg`. Neither is listed anywhere, so their buttons email Aaron.) (The Pedal-building tools section, 3 drill templates, was removed on 2026-10-02 at Aaron's request; their photos are still in `photos.json` but unused.) Each card has a photo, name, price, a one-line description, effect-type tags and a link.
- No condition tags (Brand New, Excellent, etc.). The condition field is still in the data but isn't rendered.
- The link text is "More info on Reverb", not "Buy on Reverb".
- Within Pedals, the Drive Trem (Aaron's original design) comes first. The rest are "Clone Lab" builds: part-for-part clones on PedalPCB boards.

## Design
- Look: powder-coated enclosure grey with a pilot-LED amber accent. Light and dark themes are both defined as CSS tokens in `:root`, with a `prefers-color-scheme` block and `[data-theme]` overrides.
- Fonts (Google Fonts): Bricolage Grotesque for display, Atkinson Hyperlegible for body text, JetBrains Mono for labels and prices.
- Header with a stats line (item count, location, shop link; the total $ is deliberately not shown, per Aaron), then a sticky category rail and a responsive card grid.

## Data sources
- Listings come from the Reverb API: `GET https://api.reverb.com/api/listings/all?shop=quint-guitars&per_page=50` with headers `Accept: application/hal+json` and `Accept-Version: 3.0`. It returns title, price, condition, categories, photos and `_links.web.href`. This is a snapshot from 2026-10-01 with 14 active listings totaling $2,897. The page shows 11 of them because the drill templates were dropped. On 2026-10-06 Aaron added Jazzcaster #03 ($1,200), which isn't on Reverb: it links to https://quintguitars.com/guitars/jazzcaster-03/ and its photo is `front.jpg` from that page. On 2026-10-09 Aaron added a Fender American Performer Strat ($700) and an Epiphone Les Paul Junior ($250), with email buttons and photos `american-strat.jpeg` and `lp-jr.jpeg` from `~/Downloads`. The page now has 16 items (5 guitars, 2 amps, 9 pedals) plus whatever is in the pedals `more` list.
- Photos come from `rvb-img.reverb.com`. Cloud and sandbox proxies have blocked direct downloads, so they were fetched in a browser and downscaled to data URIs. When updating listings, re-pull from the API and refresh `photos.json` for any new or changed items.
- The page is also published as a private Claude artifact ("Max's Surgery Gear Sale"). That copy is separate, and changes here don't update it.
