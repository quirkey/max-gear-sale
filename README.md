# Max's Surgery Gear Sale

One-page sale site for Quint Guitars gear (https://reverb.com/shop/quint-guitars), raising money for Max's surgery.

## Files
- `index.html`: the finished page. It's self-contained (photos are embedded as data URIs), so you can upload it to any host.
- `items.yaml`: the listings (name, price, photo, tags, description, Reverb slug), grouped into sections. This is the file to edit; the comment at the top explains each field.
- `build.py`: generates `index.html` from `items.yaml` and checks it for mistakes such as a missing field or a photo that isn't in `photos.json`.
- `template.html`: page layout and CSS. `{{NAV}}`, `{{SECTIONS}}` and `{{COUNT}}` are placeholders that build.py fills in.
- `photos.json`: listing photos as base64 JPEG data URIs (520px max), keyed by item id (e.g. `drivetrem`, `esquire`).

## Rebuild
    python3 build.py

First time on a new machine: `python3 -m venv .venv && .venv/bin/pip install pyyaml`

## Deploy
GitHub Pages from the `main` branch root of https://github.com/quirkey/max-gear-sale. Live at https://quirkey.github.io/max-gear-sale/. To update: edit `items.yaml`, `python3 build.py`, commit, `git push`. Pages rebuilds in about a minute.

## Notes
- Photos were pulled from Reverb's image CDN (rvb-img.reverb.com) through the browser, because that host was blocked for direct downloads. If the page is hosted somewhere normal, you can hotlink the Reverb image URLs instead of embedding them.
- Listing data came from the Reverb API (`https://api.reverb.com/api/listings/all?shop=quint-guitars`, headers `Accept: application/hal+json`, `Accept-Version: 3.0`). Prices are a snapshot from Oct 1, 2026.
- Items: 2 guitars, 9 pedals (Drive Trem is an original design, the rest are Clone Lab builds). The 3 drill templates were removed from the page.
