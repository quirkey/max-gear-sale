# Max's Surgery Gear Sale

One-page sale site for Quint Guitars gear (https://reverb.com/shop/quint-guitars), raising money for Max's surgery.

## Files
- `index.html`: the finished page. It loads photos from `img/`, so host it together with that folder.
- `items.yaml`: the listings (name, price, photo, tags, description, Reverb slug), grouped into sections. This is the file to edit. It also holds the `intro` paragraph under the page title and the `max_photos` header list. The comment at the top explains each field.
- `build.py`: generates `index.html` from `items.yaml` and checks it for mistakes such as a missing field or a photo that isn't in `img/`.
- `template.html`: page layout and CSS. `{{NAV}}`, `{{SECTIONS}}` and `{{COUNT}}` are placeholders that build.py fills in.
- `img/`: one JPEG per photo, named by its key (e.g. `img/drivetrem.jpg`), plus the `max-*` header photos.
- `add_photo.py`: adds a photo to `img/`, resized and with location data stripped: `python3 add_photo.py ~/Downloads/photo.jpeg my-key`, then use `photo: my-key` in `items.yaml`. Options: `--max 720` for a bigger image, `--crop x0,y0,x1,y1` to crop first. The `max_photos` list in `items.yaml` picks which header photos show and holds their alt text. Always add photos with `add_photo.py`, never by copying them into `img/`, because phone photos carry location data and the page is public.

## Rebuild
    python3 build.py

First time on a new machine: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`

## Deploy
GitHub Pages from the `main` branch root of https://github.com/quirkey/max-gear-sale. Live at https://quirkey.github.io/max-gear-sale/. To update: edit `items.yaml`, `python3 build.py`, commit, `git push`. Pages rebuilds in about a minute.

## Notes
- Photos were pulled from Reverb's image CDN (rvb-img.reverb.com) through the browser, because that host was blocked for direct downloads. If the page is hosted somewhere normal, you can hotlink the Reverb image URLs instead of embedding them.
- Listing data came from the Reverb API (`https://api.reverb.com/api/listings/all?shop=quint-guitars`, headers `Accept: application/hal+json`, `Accept-Version: 3.0`). Prices are a snapshot from Oct 1, 2026.
- Items: 5 guitars (Jazzcaster #03 links to quintguitars.com; the Strat and LP Junior aren't listed anywhere, so their buttons email Aaron), 2 amps (email buttons too), 9 pedals, plus a "More pedals" list under the pedal cards (the `more:` block in `items.yaml`) (Drive Trem is an original design, the rest are Clone Lab builds). The 3 drill templates were removed from the page.
