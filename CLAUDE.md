# Max's Surgery Gear Sale

A one-page static site listing gear from Aaron's Quint Guitars Reverb shop (https://reverb.com/shop/quint-guitars). The sale raises money for his cat Max's surgery. The shop is based in Kingston, NY.

## Files
- `index.html`: generated output and the deliverable. It's self-contained, with photos embedded as base64 data URIs (~400KB). Don't hand-edit it; edit the sources and rebuild.
- `items.yaml`: all listing data, meant for Aaron to edit by hand. Sections (`id`, `title`, `blurb`, `items`) and items (`name`, `price`, `photo`, `tags`, `description`, `reverb`, plus optional `original: true` for the "Original design" badge and `condition`). The header comment documents the fields. The link URL is `https://reverb.com/item/<reverb>`. Strings are quoted because names like "Esquire #04" would otherwise be cut off at `#` as a YAML comment.
- `build.py`: the generator. It reads `items.yaml`, validates it (missing or unknown fields, a photo key not in `photos.json`, a non-numeric price) and writes `index.html`. PyYAML lives in a gitignored `.venv`. If `yaml` can't be imported, build.py re-runs itself under `.venv/bin/python`, so plain `python3 build.py` works. To recreate the venv: `python3 -m venv .venv && .venv/bin/pip install pyyaml`.
- `template.html`: layout and CSS. Contains the placeholders `{{NAV}}`, `{{SECTIONS}}`, `{{INTRO}}`, `{{MAX_PHOTOS}}` and `{{COUNT}}`. It starts with a real document head (`<!doctype>`, charset, viewport, description), which the page needs now that it's hosted on its own rather than as an artifact. (`{{TOTAL}}` is still filled by build.py but the template no longer uses it.)
- `photos.json`: `{photo_key: "data:image/jpeg;base64,..."}`. Listing photos are JPEGs at 520px max and quality 0.72. The four `max-*` keys are photos of Max for the header, at 540×720 and quality 72. The originals were `~/Downloads/IMG_{4503,5162,6686,3846 2} Large.jpeg`.
- `max_photos` in `items.yaml` lists the header photos of Max (`photo` key and `alt` text) in display order. They render as a staggered 2×2 grid in a 480px column beside the intro on screens 820px and wider, as a row of four below the intro between 560 and 819px, and as a 2×2 grid below 560px.
- `intro` in `items.yaml` is the paragraph under the page title. It's plain text and gets HTML-escaped.
- **Strip metadata from any personal photo before embedding.** Aaron's iPhone photos carry GPS coordinates for his home. Re-encode them with Pillow (in `.venv`), which drops EXIF, as was done for the Max photos.
- `img/`: empty and unused.

## Build
    python3 build.py   # writes index.html, prints size / item count / total $

## Deploy
GitHub Pages from the `main` branch root of https://github.com/quirkey/max-gear-sale. Live at https://quirkey.github.io/max-gear-sale/. To update: edit `items.yaml`, `python3 build.py`, commit, `git push`. Pages rebuilds in about a minute.

## Content decisions (from Aaron)
- Categories: Guitars, Pedals. (The Pedal-building tools section, 3 drill templates, was removed on 2026-10-02 at Aaron's request; their photos are still in `photos.json` but unused.) Each card has a photo, name, price, a one-line description, effect-type tags and a link.
- No condition tags (Brand New, Excellent, etc.). The condition field is still in the data but isn't rendered.
- The link text is "More info on Reverb", not "Buy on Reverb".
- Within Pedals, the Drive Trem (Aaron's original design) comes first. The rest are "Clone Lab" builds: part-for-part clones on PedalPCB boards.

## Design
- Look: powder-coated enclosure grey with a pilot-LED amber accent. Light and dark themes are both defined as CSS tokens in `:root`, with a `prefers-color-scheme` block and `[data-theme]` overrides.
- Fonts (Google Fonts): Bricolage Grotesque for display, Atkinson Hyperlegible for body text, JetBrains Mono for labels and prices.
- Header with a stats line (item count, location, shop link; the total $ is deliberately not shown, per Aaron), then a sticky category rail and a responsive card grid.

## Data sources
- Listings come from the Reverb API: `GET https://api.reverb.com/api/listings/all?shop=quint-guitars&per_page=50` with headers `Accept: application/hal+json` and `Accept-Version: 3.0`. It returns title, price, condition, categories, photos and `_links.web.href`. This is a snapshot from 2026-10-01 with 14 active listings totaling $2,897. The page shows 11 of them ($2,860) because the drill templates were dropped.
- Photos come from `rvb-img.reverb.com`. Cloud and sandbox proxies have blocked direct downloads, so they were fetched in a browser and downscaled to data URIs. When updating listings, re-pull from the API and refresh `photos.json` for any new or changed items.
- The page is also published as a private Claude artifact ("Max's Surgery Gear Sale"). That copy is separate, and changes here don't update it.
