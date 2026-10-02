# Max's Surgery Gear Sale

A one-page static site listing gear from Aaron's Quint Guitars Reverb shop (https://reverb.com/shop/quint-guitars). The sale raises money for his cat Max's surgery. The shop is based in Kingston, NY.

## Files
- `index.html`: generated output and the deliverable. It's self-contained, with photos embedded as base64 data URIs (~400KB). Don't hand-edit it; edit the sources and rebuild.
- `build.py`: the generator. All listing data lives in the `sections` list at the top. Each item is `(photo_key, name, price, condition, tags, one_line_desc, reverb_slug[, True])`. A trailing `True` marks an original design and shows the "Original design" badge. The link URL is `https://reverb.com/item/<slug>`.
- `template.html`: layout and CSS. Contains the placeholders `{{NAV}}`, `{{SECTIONS}}` and `{{COUNT}}`. (`{{TOTAL}}` is still filled by build.py but the template no longer uses it.)
- `photos.json`: `{photo_key: "data:image/jpeg;base64,..."}`, JPEGs at 520px max and quality 0.72.
- `img/`: empty and unused.

## Build
    python3 build.py   # writes index.html, prints size / item count / total $

## Deploy
GitHub Pages from the `main` branch root of https://github.com/quirkey/max-gear-sale. Live at https://quirkey.github.io/max-gear-sale/. To update: `python3 build.py`, commit, `git push`. Pages rebuilds in about a minute.

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
